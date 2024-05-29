from PyQt6.QtWidgets import *
from PyQt6 import uic
import image.image_resource as image_resource
import sqlite3
from utils.utils import resource_path


class resetPasswordWindow(QWidget):
    def __init__(self):
        super(resetPasswordWindow, self).__init__()
        uic.loadUi(resource_path("interface\\reset_password_widget.ui"), self)
        self.show()

        self.resetPWButton.clicked.connect(self.reset_passwword)

        self.connection = sqlite3.connect(resource_path("db\\users.db"))
        self.cursor = self.connection.cursor()

    def run_resetPassword_and_GetVar(self, username):
        self.username = username   
        self.show()

    def reset_passwword(self):
        old_passwword = self.oldPasswordText.text().strip()
        new_password = self.newPasswordText.text().strip()
        new_password_confirm = self.newPasswordConfirmText.text().strip()

        if not old_passwword or not new_password or not new_password_confirm:
            QMessageBox.warning(self, "Perhatian!", f"Kolom username dan password tidak boleh kosong!")

        #cek password minimal 6 karakter dan harus mengandung kombinasi huruf dan angka
        elif len(new_password) < 6 or not any(char.isdigit() for char in new_password):
            QMessageBox.warning(self, "Perhatian!", f"Password minimal 6 karakter dan harus mengandung kombinasi huruf dan angka")

        # cek input password harus sama dengan confirm_password
        elif new_password != new_password_confirm:
            QMessageBox.warning(self, "Perhatian!", f"Pastikan kedua password yang Anda masukkan sama!")
        
        else:
            #Cek apakah username sudah ada sebelumnya
            self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (self.username, old_passwword))

            if not self.cursor.fetchone():
                QMessageBox.warning(self, "Perhatian!", f"Password lama yang anda masukkan salah!")
            else:
                self.cursor.execute(''' UPDATE users
                                        SET password = ?
                                        WHERE username = ?''', (new_password, self.username))
                self.connection.commit()
                QMessageBox.information(self, "Login Berhasil!", f"Password berhasil di reset!")
                self.hide()



def main():
    App = QApplication([])
    window = resetPasswordWindow()
    App.exec()

if __name__ == "__main__":
    main()