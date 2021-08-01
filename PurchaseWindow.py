from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QCompleter
import MainWindow as mw

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

    def goHome(self):
        self.cw = mw.MainWindow()
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
