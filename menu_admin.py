from PyQt6.QtWidgets import *
from PyQt6 import uic
from utils.utils import resource_path 

class AdminMenuWindow(QWidget):
    def __init__(self):
        self.username = ""
        
        super(AdminMenuWindow, self).__init__()
        uic.loadUi(resource_path("interface\\menu_widget_admin.ui"), self)
        self.show()

        self.cameraButton.clicked.connect(self.run_camera)
        self.userListButton.clicked.connect(self.run_userList)
        self.resetPasswordButton.clicked.connect(self.reset_password)
        self.createUserButton.clicked.connect(self.run_create_user)


    def run_menu_admin_and_getVar(self, username):
        self.username = username    
        self.show()


    def reset_password(self):
        from reset_password import resetPasswordWindow
        self.resetPassword = resetPasswordWindow()
        self.resetPassword.run_resetPassword_and_GetVar(self.username)
 

    def run_userList(self):
        from show_user import showUserWindow
        self.showUserWindow = showUserWindow()
        self.showUserWindow.show()


    def run_camera(self):
        self.hide()
        from camera import CameraWindow
        self.cameraWindow = CameraWindow()
        self.cameraWindow.showMaximized()

     
    def run_create_user(self):
        from signup import SignUpWindow
        self.signUpWindow = SignUpWindow()
        self.signUpWindow.show()


def main():
    App = QApplication([])
    window = AdminMenuWindow()
    App.exec()

if __name__ == "__main__":
    main()