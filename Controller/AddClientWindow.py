from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QCompleter
import MainWindow as mw
import StockWindow as stw
import DatabaseController as dbc


class AddClientWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("Views/AddClientWindow.ui", self)
        self.setFixedSize(1000, 900)
        self.saveButton.clicked.connect(self.saveClient)
        self.contactNo.editingFinished.connect(self.validating)
        self.pin.editingFinished.connect(self.validating)

    def saveClient(self):
        conn = dbc.getConnection()
        cursor = conn.cursor()
        try:
            _fullName = self.fullName.text()
            _bAddress = self.bAddress.toPlainText()
            _city = self.city.text()
            _state = self.state.text()
            _pin = self.pin.text()
            _contactNo = self.contactNo.text()
            _panNo = self.panNo.text()
            _gstin = self.gstin.text()
            if _pin is None:
                pass
            else:
                _pin = int(_pin)

            if _contactNo is None:
                pass
            else:
                _contactNo = int(_contactNo)

        except Exception as e:
            print(e)

        try:
            cursor.execute("insert into client_info values(?,?,?,?,?,?,?,?)",
                           (_fullName, _bAddress, _city, _state, _pin, _contactNo, _panNo, _gstin))
            conn.commit()
        except Exception as e:
            print(e)

        self.close()

    def validating(self):
        if self.contactNo.text().isnumeric():
            pass
        else:
            self.contactNo.setText("")

        if self.pin.text().isnumeric():
            pass
        else:
            self.pin.setText("")