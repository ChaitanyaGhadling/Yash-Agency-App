from PyQt6 import uic
from PyQt6.QtGui import QIntValidator, QDoubleValidator, QValidator
from PyQt6.QtWidgets import QWidget, QCompleter, QTableWidgetItem, QMessageBox
import MainWindow as mw
import DatabaseController as dbc

class NewTypeWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("Views/NewTypeWindow.ui", self)
        self.setFixedSize(1000, 900)
        self.saveButton.clicked.connect(self.updateType)
        self.updateTable()

    def updateTable(self):
        conn = dbc.getConnection()
        cursor = conn.cursor()

        try:
            cursor.execute("select * from type")
            self.tableWidget.setColumnCount(2)
            self.tableWidget.setRowCount(len(cursor.fetchall()))
            cursor.execute("select * from type")
            for i, row in enumerate(cursor):
                self.tableWidget.setItem(i, 0, QTableWidgetItem(f"{i + 1}"))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(row[0]))
            conn.close()
        except Exception as e:
            print(e)

    def updateType(self):
        conn = dbc.getConnection()
        cursor = conn.cursor()
        _type = self.type_Edit.text()
        if self.Add_RB.isChecked():
            try:
                cursor.execute(
                    "insert or ignore into type values(?)", (_type,))
                conn.commit()
                conn.close()
                self.type_Edit.setText("")
                self.updateTable()
            except Exception as e:
                print(e)
        elif self.Remove_RB.isChecked():
            try:
                cursor.execute(
                    "delete from type where type=?", (_type,))
                conn.commit()
                conn.close()
                self.type_Edit.setText("")
                self.updateTable()
            except Exception as e:
                print(e)
