from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QCompleter
import MainWindow as mw
import StockWindow as stw
import DatabaseController as dbc

class AddSupplierWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("Views/AddSupplierWindow.ui", self)
        self.setFixedSize(1200, 900)
        self.saveButton.clicked.connect(self.saveSupplier)

        self.contactNo.editingFinished.connect(self.validating)
        self.pin.editingFinished.connect(self.validating)

    def saveSupplier(self):
        conn = dbc.getConnection()
        cursor = conn.cursor()
        try:
            _companyName = self.companyName.text()
            _address = self.address.toPlainText()
            _city = self.city.text()
            _state = self.state.text()
            _contactPerson = self.contactPerson.text()
            _email = self.email.text()
            _bankName = self.bankName.text()
            _accountNo = self.accountNo.text()
            _ifsc = self.ifsc.text()
            _panNo = self.panNo.text()
            _gstin = self.gstin.text()
            _taxState = self.taxState.text()
            _pin = self.pin.text()
            _contactNo = self.contactNo.text()
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
            cursor.execute("insert into supplier_info values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                           (_companyName, _address, _city, _state, _pin, _contactNo, _contactPerson, _email, _bankName,
                            _accountNo, _ifsc, _panNo, _gstin, _taxState))
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