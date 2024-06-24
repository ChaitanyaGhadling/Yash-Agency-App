from PyQt6 import uic
from PyQt6.QtGui import QIntValidator, QDoubleValidator, QValidator
from PyQt6.QtWidgets import QWidget, QCompleter, QTableWidgetItem, QMessageBox
import MainWindow as mw
import DatabaseController as dbc
from PyQt6.QtCore import Qt
from datetime import datetime


class UpdateQuantityWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("Views/UpdateQuantityWindow.ui", self)
        self.setFixedSize(1000, 900)
        self.searchButton.clicked.connect(self.searchStock)
        self.updateQuantity_Edit.textEdited.connect(self.validating)
        self.saveButton.clicked.connect(self.updateQuantity)
        #self.Add_CB.stateChanged.connect(self.validating)
        #self.Remove_CB.stateChanged.connect(self.validating)
        items = []
        completer = QCompleter(items)
        self.searchbar.setCompleter(completer)
        item_list = []
        try:
            conn = dbc.getConnection()
            cursor = conn.cursor()
            cursor.execute("select name from stock")
            items = cursor.fetchall()
            for item in items:
                item_list.append(item[0])
            conn.close()
        except Exception as e:
            print(e)
        completer = QCompleter(item_list)
        self.searchbar.setCompleter(completer)


    def searchStock(self):
        conn = dbc.getConnection()
        cursor = conn.cursor()
        _searchItem = self.searchbar.text()
        try:
            cursor.execute("select * from stock where name =" +
                           "\"" + _searchItem + "\"")
            row = cursor.fetchone()
            self.productId.setText(f"{row[0]}")
            self.productName.setText(f"{row[1]}")
            self.productType.setCurrentText(f"{row[2]}")
            self.productCategory.setCurrentText(f"{row[3]}")
            self.productQuantity.setText(f"{row[4]}")
            self.productUnit.setText(f"{row[5]}")
            conn.close()
        except Exception as e:
            print(e)

    def validating(self):
        if self.updateQuantity_Edit.text() != None and (self.Add_CB.isChecked() or self.Remove_CB.isChecked()):
            try:
                updatedValue = int(self.updateQuantity_Edit.text())
                currentQuantity = int(self.productQuantity.text())

                if self.Add_CB.isChecked():
                    newQuantity = currentQuantity + updatedValue
                elif self.Remove_CB.isChecked():
                    newQuantity = currentQuantity - updatedValue
                    if newQuantity < 0:
                        QMessageBox.warning(self, "Invalid Operation", "Quantity cannot be negative")
                        self.updatedQuantity.setText("")
                        return
                else:
                    QMessageBox.warning(self, "Selection Error", "Please select Add or Remove")
                    return

                self.updatedQuantity.setText(str(newQuantity))
            except ValueError:
                QMessageBox.warning(self, "Input Error", "Please enter a valid number")
                self.updatedQuantity.setText("")
        else:
            self.updatedQuantity.setText("")

    def updateQuantity(self):
        newQuantity = self.updatedQuantity.text()
        current_date = datetime.now().date()
        lastModifiedDate = current_date.strftime("%Y-%m-%d")
        conn = dbc.getConnection()
        cursor = conn.cursor()
        cursor.execute("UPDATE stock SET quantity = ?, last_modified = ? WHERE id = ?", (newQuantity, lastModifiedDate,
                                                                                         self.productId.text()))
        conn.commit()
        conn.close()
        self.updatedQuantity.setText("")
        self.updateQuantity_Edit.setText("")
        self.productQuantity.setText(newQuantity)
        QMessageBox.information(self, "Success", "Quantity updated successfully")

