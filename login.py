from PyQt6.QtWidgets import *
from PyQt6 import uic
import sqlite3
from utils.utils import resource_path  

class LoginWindow(QWidget):
    def __init__(self):
        super(LoginWindow, self).__init__()
        uic.loadUi(resource_path("interface\\login_widget.ui"), self)
        self.show()

        self.loginButton.clicked.connect(self.login)

        print("Conecting to DB user.db")
        self.connection = sqlite3.connect(resource_path("db\\users.db"))
        if self.connection:
            print("DB Connected!")

        self.cursor = self.connection.cursor()

        # Create table if not exists
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY,
                   username TEXT NOT NULL,
                   password TEXT NOT NULL,
                   last_login TIMESTAMP
            )"""
        )

        self.cursor.execute("SELECT * FROM users WHERE username = ?", ("admin",))
        if not self.cursor.fetchone():
            # Insert sample user (admin, password)
            self.cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("admin", "admin123"))
            self.connection.commit()


    def login(self):
        self.username = self.usernameText.text()
        password = self.passwordText.text()

        if not self.username or not password:
            QMessageBox.warning(self, "Perhatian!", f"Kolom username dan password tidak boleh kosong!")

        else:
            # Query the database for the user
            self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (self.username, password))
            user = self.cursor.fetchone()

            self.cursor.execute('''UPDATE users
                                    SET last_login = CURRENT_TIMESTAMP
                                    WHERE username = ?''', (self.username,))
            
            self.connection.commit()
            
            if user:
                QMessageBox.information(self, "Info", f"Selamat Datang, {self.username}!")
                if user[1].lower() == "admin":
                    self.run_menu_admin()
                else:
                    self.run_menu()
            else:
                QMessageBox.critical(self, "Login Gagal!", "Username atau Password salah!")


    def run_menu(self):
        self.hide()
        from menu import MenuWindow 
        self.menuWindow = MenuWindow()
        self.menuWindow.run_menu_and_getVar(self.username)


    def run_menu_admin(self):
        self.hide()
        from menu_admin import AdminMenuWindow
        self.menuAdminWindow = AdminMenuWindow()
        self.menuAdminWindow.run_menu_admin_and_getVar(self.username)

def main():
    App = QApplication([])
    window = LoginWindow()
    App.exec()

if __name__ == "__main__":
    main()