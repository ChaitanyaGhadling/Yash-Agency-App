from PyQt5.QtCore import QDate, QTime, QTimer
from PyQt5.QtWidgets import *
from PyQt5 import uic
import DatabaseController as dbc

import SalesWindow as sw
import PurchaseWindow as pw
import InvoiceWindow as iw
import QuotationWindow as qw
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("MainWindow.ui", self)
        self.setFixedSize(1900, 980)
        self.stockButton.clicked.connect(self.goToStock)
        self.salesButton.clicked.connect(self.goToSales)
        self.purchaseButton.clicked.connect(self.goToPurchase)
        self.invoiceButton.clicked.connect(self.goToInvoices)
        self.quotationButton.clicked.connect(self.goToQuotations)
        # self.homeButton.clicked.connect()
        self.addClientButton.clicked.connect(self.goToAddClient)
        self.addSupplierButton.clicked.connect(self.goToAddSupplier)
        self.addExpenseButton.clicked.connect(self.goToAddExpense)
        self.setReminderButton.clicked.connect(self.goToSetReminder)
        self.paymentInButton.clicked.connect(self.goToPaymentIn)
        self.paymentOutButton.clicked.connect(self.goToPaymentOut)

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.timeout.connect(self.showDate)
        timer.start(1000)

        date = QDate.currentDate().toString()
        self.date_label.setText(date)

    def showTime(self):
        time = QTime.currentTime().toString()
        self.time_label.setText(time)

    def showDate(self):
        date = QDate.currentDate().toString()
        self.date_label.setText(date)

    def goToStock(self):
        import StockWindow as stw
        self.cw = stw.StockWindow()
        self.cw.show()
        self.close()

    def goToSales(self):
        self.cw = sw.SalesWindow()
        self.cw.show()
        self.close()

    def goToPurchase(self):
        self.cw = pw.PurchaseWindow()
        self.cw.show()
        self.close()

    def goToInvoices(self):
        self.cw = iw.InvoiceWindow()
        self.cw.show()
        self.close()

    def goToQuotations(self):
        self.cw = qw.QuotationWindow()
        self.cw.show()
        self.close()

    def goToAddClient(self):
        self.cw = AddClientWindow()
        self.cw.show()

    def goToAddSupplier(self):
        self.cw = AddSupplierWindow()
        self.cw.show()

    def goToAddExpense(self):
        self.cw = AddExpenseWindow()
        self.cw.show()

    def goToSetReminder(self):
        self.cw = SetReminderWindow()
        self.cw.show()

    def goToPaymentIn(self):
        self.cw = PaymentInWindow()
        self.cw.show()

    def goToPaymentOut(self):
        self.cw = PaymentOutWindow()
        self.cw.show()


class AddClientWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("AddClientWindow.ui", self)
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

    def validating(self):
        if self.contactNo.text().isnumeric():
            pass
        else:
            self.contactNo.setText("")

        if self.pin.text().isnumeric():
            pass
        else:
            self.pin.setText("")


class AddSupplierWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("AddSupplierWindow.ui", self)
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

    def validating(self):
        if self.contactNo.text().isnumeric():
            pass
        else:
            self.contactNo.setText("")

        if self.pin.text().isnumeric():
            pass
        else:
            self.pin.setText("")


class AddExpenseWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("AddExpenseWindow.ui", self)
        self.setFixedSize(1100, 550)


class SetReminderWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("SetReminderWindow.ui", self)
        self.setFixedSize(950, 500)


class PaymentInWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("PaymentInWindow.ui", self)
        self.setFixedSize(1100, 650)


class PaymentOutWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("PaymentOutWindow.ui", self)
        self.setFixedSize(1100, 650)


if __name__ == "__main__":

    app = QApplication([])
    window_1 = MainWindow()
    window_1.show()
    app.exec()
