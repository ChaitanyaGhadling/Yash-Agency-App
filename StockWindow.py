from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QCompleter
import MainWindow as mw
import DatabaseController as dbc


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
        self.cw = mw.MainWindow()
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

        self.saveButton.clicked.connect(self.insertProduct_AddNewItemWindow)

    def insertProduct_AddNewItemWindow(self):
        conn = dbc.getConnection()
        productId = self.productId.text
        productName = self.productName.text()
        productType = str(self.productType.currentText())
        productCategory = str(self.productCategory.currentText())
        productQuantity = self.productQuantity.text()
        productUnit = self.productUnit.text()
        productRetailPrice = self.productRetailPrice.text()
        productWholeSalePrice = self.productWholeSalePrice.text()
        productPurchasePrice = self.productPurchasePrice.text()
        productTransportPrice = self.productTransportPrice.text()
        productGSTRate = self.productGSTRate.text()
        productLowWarningLimit = self.productLowWarningLimit.text()

        conn.execute(f"INSERT INTO stock \
        VALUES ({productId},{productName},{productType},{productCategory},{productQuantity},{productUnit} \
        ,{productRetailPrice},{productWholeSalePrice},{productPurchasePrice},{productTransportPrice} \
        ,{productGSTRate},{productLowWarningLimit})")

        conn.close()


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
