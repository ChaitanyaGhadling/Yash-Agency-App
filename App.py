from PyQt5.QtCore import QDate,QTime,QTimer
from PyQt5.QtWidgets import *
from PyQt5 import uic
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
        #self.homeButton.clicked.connect()
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
        self.cw = StockWindow()
        self.cw.show()
        self.close()
    def goToSales(self):
        self.cw = SalesWindow()
        self.cw.show()
        self.close()
    def goToPurchase(self):
        self.cw = PurchaseWindow()
        self.cw.show()
        self.close()
    def goToInvoices(self):
        self.cw = InvoiceWindow()
        self.cw.show()
        self.close()
    def goToQuotations(self):
        self.cw = QuotationWindow()
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


class StockWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("StockWindow.ui", self)
        self.setFixedSize(1900, 980)
        self.homeButton.clicked.connect(self.goHome)
        self.categoryButton.clicked.connect(self.goToCategory)
        self.typeButton.clicked.connect(self.goToType)
        self.newItemButton.clicked.connect(self.goToAddNewItem)
        self.editItemButton.clicked.connect(self.goToEditItem)
        self.defectiveItemButton.clicked.connect(self.goToDefectiveItem)
        self.updateQuantityButton.clicked.connect(self.goToUpdateQuantity)
        items = []
        completer = QCompleter(items)
        self.searchbar.setCompleter(completer)
        self.stockTable.setColumnWidth(0, 130)
        self.stockTable.setColumnWidth(1, 580)
        self.stockTable.setColumnWidth(2, 210)
        self.stockTable.setColumnWidth(3, 210)
        self.stockTable.setColumnWidth(4, 100)
        self.stockTable.setColumnWidth(5, 125)
        self.stockTable.setColumnWidth(6, 125)
        self.stockTable.setColumnWidth(7, 165)

    def goHome(self):
        self.cw = MainWindow()
        self.cw.show()
        self.close()

    def goToCategory(self):
        self.cw = NewCategoryWindow()
        self.cw.show()

    def goToType(self):
        self.cw = NewTypeWindow()
        self.cw.show()

    def goToEditItem(self):
        self.cw = EditItemWindow()
        self.cw.show()

    def goToDefectiveItem(self):
        self.cw = DefectiveItemsWindow()
        self.cw.show()

    def goToAddNewItem(self):
        self.cw = AddNewItemWindow()
        self.cw.show()

    def goToUpdateQuantity(self):
        self.cw = UpdateQuantityWindow()
        self.cw.show()

class SalesWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("SalesWindow.ui", self)
        self.setFixedSize(1900, 980)
        self.homeButton.clicked.connect(self.goHome)

    def goHome(self):
        self.cw = MainWindow()
        self.cw.show()
        self.close()

class PurchaseWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("PurchaseWindow.ui", self)
        self.setFixedSize(1900, 980)
        self.homeButton.clicked.connect(self.goHome)
        self.newPurchaseButton.clicked.connect(self.goToNewPurchase)
        self.transportButton.clicked.connect(self.goToTransport)
        self.purchaseTable.setColumnWidth(0, 100)
        self.purchaseTable.setColumnWidth(1, 125)
        self.purchaseTable.setColumnWidth(2, 150)
        self.purchaseTable.setColumnWidth(3, 150)
        self.purchaseTable.setColumnWidth(4, 250)
        self.purchaseTable.setColumnWidth(5, 200)
        self.purchaseTable.setColumnWidth(6, 160)
        self.purchaseTable.setColumnWidth(7, 200)
        self.purchaseTable.setColumnWidth(8, 135)
        self.purchaseTable.setColumnWidth(9, 145)

    def goToNewPurchase(self):
        self.cw = NewPurchaseWindow()
        self.cw.show()
        self.close()

    def goHome(self):
        self.cw = MainWindow()
        self.cw.show()
        self.close()

    def goToTransport(self):
        self.cw = TransportWindow()
        self.cw.show()

class InvoiceWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("InvoiceWindow.ui", self)
        self.setFixedSize(1900, 980)
        self.homeButton.clicked.connect(self.goHome)

    def goHome(self):
        self.cw = MainWindow()
        self.cw.show()
        self.close()

class QuotationWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("QuotationWindow.ui", self)
        self.setFixedSize(1900, 980)
        self.homeButton.clicked.connect(self.goHome)

    def goHome(self):
        self.cw = MainWindow()
        self.cw.show()
        self.close()

class NewCategoryWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("NewCategoryWindow.ui", self)
        self.setFixedSize(1000, 900)

class NewTypeWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("NewTypeWindow.ui", self)
        self.setFixedSize(1000, 900)

class AddNewItemWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("AddNewItemWindow.ui", self)
        self.setFixedSize(1000, 900)


class EditItemWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("EditItemWindow.ui", self)
        self.setFixedSize(1000, 900)
        items = []
        completer = QCompleter(items)
        self.searchbar.setCompleter(completer)

class DefectiveItemsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("DefectiveItemsWindow.ui", self)
        self.setFixedSize(1000, 900)

class UpdateQuantityWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("UpdateQuantityWindow.ui", self)
        self.setFixedSize(1000, 900)
        items = []
        completer = QCompleter(items)
        self.searchbar.setCompleter(completer)

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

class NewPurchaseWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("NewPurchaseWindow.ui", self)
        self.setFixedSize(1900, 980)
        self.homeButton.clicked.connect(self.goHome)
        self.backButton.clicked.connect(self.goBack)

    def goHome(self):
        self.cw = MainWindow()
        self.cw.show()
        self.close()

    def goBack(self):
        self.cw = PurchaseWindow()
        self.cw.show()
        self.close()

class TransportWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("TransportWindow.ui", self)
        self.setFixedSize(1100, 650)



app = QApplication([])
window_1 = MainWindow()
window_1.show()
app.exec()
