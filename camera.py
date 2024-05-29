import sys
from ultralytics import YOLO
from preprocessing import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import cv2
from utils.utils import resource_path 
import numpy as np
from pygame import mixer   

model = YOLO(resource_path("models\\best_new.pt"))
class_list = model.model.names
scale_show = 100
status_detect = True

class CameraWindow(QWidget):
    def __init__(self):
        super(CameraWindow, self).__init__()

        self.VBL = QVBoxLayout()

        self.setWindowTitle("Aplikasi Pendeteksi Makser - Deteksi Kamera")

        self.FeedLabel = QLabel()
        self.VBL.addWidget(self.FeedLabel)

        self.Worker1 = Worker1()
        self.Worker1.start()
        self.Worker1.ImageUpdate.connect(self.image_update_slot)

        self.Worker2 = Worker2()
        self.Worker2.start()

        self.setLayout(self.VBL)

    def image_update_slot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))
    

class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)
    status_detect = pyqtSignal(str)

    def running_detection(self, frame, results, class_list, scale_show):
        labeled_frame = draw_box(frame, results[0], class_list)
        display_frame = resize_image(labeled_frame, scale_show)
        Image = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
        return Image
    
    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                results = model.predict(frame)

                class_id = results[0].boxes.cls.cpu().numpy().astype(int)

                check_no_mask = np.isin(0, class_id)

                if check_no_mask :
                    global status_detect
                    status_detect = False
                elif not check_no_mask:
                    status_detect = True
                
                Image = self.running_detection(frame, results, class_list, scale_show)

                FlippedImage = Image
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(1510, 780)

                self.ImageUpdate.emit(Pic)
    
                
    def stop(self):
        self.ThreadActive = False
        self.quit()


class Worker2(QThread):
    msg_audio = pyqtSignal(str)    

    def run(self):
        while True:
            global status_detect
            if not status_detect:
                mixer.init()
                mixer.music.load(resource_path('audio\\harap_gunakan_masker.mp3'))  # Ganti dengan path ke file audio yang ingin diputar
                mixer.music.play()
            time.sleep(2.2)


def main():
    App = QApplication(sys.argv)
    Root = CameraWindow()
    Root.showMaximized()
    sys.exit(App.exec())


if __name__ == "__main__":
    main()

