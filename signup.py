from PyQt6.QtWidgets import *
from PyQt6 import uic
import sqlite3
from utils.utils import resource_path


class SignUpWindow(QWidget):
    def __init__(self):
        super(SignUpWindow, self).__init__()
        uic.loadUi(resource_path("interface\\signup_widget.ui"), self)
        self.show()

        self.signUpButton.clicked.connect(self.signup)

        self.connection = sqlite3.connect(resource_path("db\\users.db"))
        self.cursor = self.connection.cursor()


    def signup(self):
        username = self.usernameText.text().strip()
        password = self.passwordText.text().strip()
        password_confirm = self.passwordConfirmText.text().strip()

        if not username or not password or not password_confirm:
            QMessageBox.warning(self, "Perhatian!", f"Kolom username dan password tidak boleh kosong!")

        #cek password minimal 6 karakter dan harus mengandung kombinasi huruf dan angka
        elif len(password) < 6 or not any(char.isdigit() for char in password):
            QMessageBox.warning(self, "Perhatian!", f"Password minimal 6 karakter dan harus mengandung kombinasi huruf dan angka")

        # cek input password harus sama dengan confirm_password
        elif password != password_confirm:
            QMessageBox.warning(self, "Perhatian!", f"Pastikan kedua password yang Anda masukkan sama!")
        
        else:
            #Cek apakah username sudah ada sebelumnya
            self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))

            if self.cursor.fetchone():
                QMessageBox.warning(self, "Perhatian!", f"Username '{username}' sudah digunakan!")
            else:
                self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                self.connection.commit()
                QMessageBox.information(self, "Info", f"User dengan nama '{username}' berhasil dibuat!")
                
                self.usernameText.clear()
                self.passwordText.clear()
                self.passwordConfirmText.clear()

def main():
    App = QApplication([])
    window = SignUpWindow()
    App.exec()

if __name__ == "__main__":
    main()