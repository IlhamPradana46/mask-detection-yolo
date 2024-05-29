from PyQt6.QtWidgets import *   
from PyQt6 import uic
import sqlite3
import image.image_resource as image_resource
from utils.utils import resource_path


class showUserWindow(QWidget):
    def __init__(self):
        super(showUserWindow, self).__init__()
        uic.loadUi(resource_path("interface\\show_user.ui"), self)
        
        self.show()

        self.deleteButton.clicked.connect(self.delete_user)
        
        self.userTableWidget.setColumnWidth(0, 40)
        self.userTableWidget.setColumnWidth(1, 200)
        self.userTableWidget.setColumnWidth(2, 200)
        self.userTableWidget.setColumnWidth(3, 178)

        self.connection = sqlite3.connect(resource_path("db\\users.db"))
        self.cursor = self.connection.cursor()
         
        self.cursor.execute("SELECT * FROM users")
        data = self.cursor.fetchall()

        self.userTableWidget.setRowCount(len(data))
        self.userTableWidget.verticalHeader().setVisible(False)

        for row_num, row_data in enumerate(data):
            for col_num, col_data in enumerate(row_data):
                self.userTableWidget.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))

    
    def query_delete(self):
        msg_box = QMessageBox()
        msg_box.information(self, "Info", f"Anda berhasil menghapus data!")
        self.cursor.execute("DELETE FROM users WHERE id = ?", (self.id_to_delete,))
        self.connection.commit()
        self.userTableWidget.removeRow(self.selected_row)

    
    def delete_user(self):
        self.selected_row = self.userTableWidget.currentRow()
        if self.selected_row >= 0:

            self.id_to_delete = self.userTableWidget.item(self.selected_row, 0).text()

            if self.id_to_delete == '1':
                QMessageBox.critical(self, "Perhatian!", "Tidak bisa menghapus akun Admin!")
            else:
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Information")
                
                msg_box.setText("Apakah Anda yakin ingin menghapus data?")
                msg_box.setIcon(QMessageBox.Icon.Question)

                button_yes = msg_box.addButton(QMessageBox.StandardButton.Yes)
                button_no = msg_box.addButton(QMessageBox.StandardButton.No)

                button_yes.setObjectName("buttonYes")
                button_no.setObjectName("buttonNo")

                msg_box.setStyleSheet("QPushButton#buttonYes { background-color: blue; color: white;}"
                                      "QPushButton#buttonNo { background-color: red; color: white; }"
                                      "QMessageBox { background-color: rgb(0, 23, 37); }"
                                      "QLabel{ color: white; }")

                button_yes.clicked.connect(self.query_delete)
                msg_box.exec()

def main():
    App = QApplication([])
    window = showUserWindow()
    App.exec()

if __name__ == "__main__":
    main()