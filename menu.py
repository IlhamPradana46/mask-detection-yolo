from PyQt6.QtWidgets import *
from PyQt6 import uic
from utils.utils import resource_path


class MenuWindow(QWidget):
    def __init__(self):
        super(MenuWindow, self).__init__()
        self.username = ""

        uic.loadUi(resource_path("interface\\menu_widget.ui"), self)
        self.show()

        self.cameraButton.clicked.connect(self.run_camera)
        self.resetPWButton.clicked.connect(self.reset_password)

    def run_camera(self):
        self.hide()
        from camera import CameraWindow
        self.cameraWindow = CameraWindow()
        self.cameraWindow.showMaximized()

    def run_menu_and_getVar(self, username):
        self.username = username    
        self.show()

    def reset_password(self):
        from reset_password import resetPasswordWindow
        self.resetPassword = resetPasswordWindow()
        self.resetPassword.run_resetPassword_and_GetVar(self.username)


def main():
    App = QApplication([])
    window = MenuWindow()
    App.exec()

if __name__ == "__main__":
    main()