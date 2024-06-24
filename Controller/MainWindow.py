from PyQt6.QtCore import QDate, QTime, QTimer
from PyQt6.QtWidgets import *
from PyQt6 import uic
import DatabaseController as dbc

import SalesWindow as sw
import PurchaseWindow as pw
import InvoiceWindow as iw
import QuotationWindow as qw
import AddClientWindow as acw
import AddSupplierWindow as asw
import AddExpenseWindow as aew
import SetReminderWindow as srw
import PaymentInWindow as piw
import PaymentOutWindow as pow
import PointOfSaleWindow as posw
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Views/MainWindow.ui", self)
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
        self.cw = posw.PointOfSaleWindow()
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
        self.cw = acw.AddClientWindow()
        self.cw.show()

    def goToAddSupplier(self):
        self.cw = asw.AddSupplierWindow()
        self.cw.show()

    def goToAddExpense(self):
        self.cw = aew.AddExpenseWindow()
        self.cw.show()

    def goToSetReminder(self):
        self.cw = srw.SetReminderWindow()
        self.cw.show()

    def goToPaymentIn(self):
        self.cw = piw.PaymentInWindow()
        self.cw.show()

    def goToPaymentOut(self):
        self.cw = pow.PaymentOutWindow()
        self.cw.show()


if __name__ == "__main__":

    app = QApplication([])
    window_1 = MainWindow()
    window_1.show()
    app.exec()
