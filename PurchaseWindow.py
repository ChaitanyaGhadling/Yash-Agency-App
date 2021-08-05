from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QCompleter
import MainWindow as mw
import StockWindow as stw
import DatabaseController as dbc


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
        self.cw = mw.MainWindow()
        self.cw.show()
        self.close()

    def goToTransport(self):
        self.cw = TransportWindow()
        self.cw.show()


class NewPurchaseWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("NewPurchaseWindow.ui", self)
        self.setFixedSize(1900, 980)
        self.homeButton.clicked.connect(self.goHome)
        self.backButton.clicked.connect(self.goBack)
        self.addItemButton.clicked.connect(self.goToAddNewItem)
        self.addSupplier.clicked.connect(self.addNewSupplier)
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 650)
        self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(3, 200)
        self.table.setColumnWidth(4, 200)
        self.table.setColumnWidth(5, 200)
        self.table.setColumnWidth(6, 195)
        try:
            conn = dbc.getConnection()
            cursor = conn.cursor()
            cursor.execute("select company_name from supplier_info")
            supplier_list = cursor.fetchall()
            conn.close()
        except Exception as e:
            print(e)
        try:
            for item in supplier_list:
                self.supplier_CB.addItem(item[0])
        except Exception as e:
            print(e)
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
        self.itemName.setCompleter(completer)

    def addNewSupplier(self):
        self.cw = mw.AddSupplierWindow()
        self.cw.show()
        newSupplier = self.cw.companyName.text()
        self.supplier_CB.addItem(newSupplier)

    def addNewPurchase(self):
        conn = dbc.getConnection()
        cursor = conn.cursor()

    def goHome(self):
        self.cw = mw.MainWindow()
        self.cw.show()
        self.close()

    def goBack(self):
        self.cw = PurchaseWindow()
        self.cw.show()
        self.close()

    def goToAddNewItem(self):
        self.cw = stw.AddNewItemWindow()
        self.cw.show()

class TransportWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("TransportWindow.ui", self)
        self.setFixedSize(1100, 650)
