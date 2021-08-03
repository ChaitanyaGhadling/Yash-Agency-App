from PyQt5.QtCore import QDate, QTime, QTimer
from PyQt5.QtWidgets import *
from PyQt5 import uic

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


class AddSupplierWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("AddSupplierWindow.ui", self)
        self.setFixedSize(1200, 900)


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
