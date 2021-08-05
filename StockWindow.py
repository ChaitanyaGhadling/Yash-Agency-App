from PyQt5 import uic
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QValidator
from PyQt5.QtWidgets import QWidget, QCompleter, QTableWidgetItem
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
        self.saveButton.clicked.connect(self.updateCategory)
        self.updateTable()

    def updateTable(self):
        conn = dbc.getConnection()
        cursor = conn.cursor()

        try:
            cursor.execute("select * from category")
            self.tableWidget.setColumnCount(2)
            self.tableWidget.setRowCount(len(cursor.fetchall()))
            cursor.execute("select * from category")
            for i, row in enumerate(cursor):
                self.tableWidget.setItem(i, 0, QTableWidgetItem(f"{i+1}"))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(row[0]))
            conn.close()
        except Exception as e:
            print(e)

    def updateCategory(self):
        conn = dbc.getConnection()
        cursor = conn.cursor()
        _category = self.category_Edit.text()
        if self.Add_RB.isChecked():
            try:
                cursor.execute(
                    "insert or ignore into category values(?)", (_category,))
                conn.commit()
                conn.close()
                self.category_Edit.setText("")
                self.updateTable()
            except Exception as e:
                print(e)
        elif self.Remove_RB.isChecked():
            try:
                cursor.execute(
                    "delete from category where category=?", (_category,))
                conn.commit()
                conn.close()
                self.category_Edit.setText("")
                self.updateTable()
            except Exception as e:
                print(e)


class NewTypeWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("NewTypeWindow.ui", self)
        self.setFixedSize(1000, 900)
        self.saveButton.clicked.connect(self.updateCategory)
        self.updateTable()

    def updateTable(self):
        conn = dbc.getConnection()
        cursor = conn.cursor()

        try:
            cursor.execute("select * from type")
            self.tableWidget.setColumnCount(2)
            self.tableWidget.setRowCount(len(cursor.fetchall()))
            cursor.execute("select * from type")
            for i, row in enumerate(cursor):
                self.tableWidget.setItem(i, 0, QTableWidgetItem(f"{i+1}"))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(row[0]))
            conn.close()
        except Exception as e:
            print(e)

    def updateCategory(self):
        conn = dbc.getConnection()
        cursor = conn.cursor()
        _type = self.type_Edit.text()
        if self.Add_RB.isChecked():
            try:
                cursor.execute(
                    "insert or ignore into type values(?)", (_type,))
                conn.commit()
                conn.close()
                self.type_Edit.setText("")
                self.updateTable()
            except Exception as e:
                print(e)
        elif self.Remove_RB.isChecked():
            try:
                cursor.execute(
                    "delete from type where type=?", (_type,))
                conn.commit()
                conn.close()
                self.type_Edit.setText("")
                self.updateTable()
            except Exception as e:
                print(e)


class AddNewItemWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("AddNewItemWindow.ui", self)
        self.setFixedSize(1000, 900)
        self.saveButton.clicked.connect(self.insertProduct_AddNewItemWindow)

        self.productId.editingFinished.connect(self.validating)
        self.productQuantity.editingFinished.connect(self.validating)
        self.productUnit.editingFinished.connect(self.validating)
        self.productRetailPrice.editingFinished.connect(self.validating)
        self.productWholeSalePrice.editingFinished.connect(self.validating)
        self.productPurchasePrice.editingFinished.connect(self.validating)
        self.productTransportPrice.editingFinished.connect(self.validating)
        self.productGSTRate.editingFinished.connect(self.validating)
        self.productLowWarningLimit.editingFinished.connect(self.validating)
        self.initComboBox()

    def initComboBox(self):
        conn = dbc.getConnection()
        cursor = conn.cursor()
        typeList = []
        categoryList = []

        try:
            cursor.execute("select * from type")
            for row in cursor:
                typeList.append(row[0])
            self.productType.addItems(typeList)

            cursor.execute("select * from category")
            for row in cursor:
                categoryList.append(row[0])
            self.productCategory.addItems(categoryList)
            conn.close()
        except Exception as e:
            print(e)

    def validating(self):

        if self.productId.text().isnumeric():
            pass
        else:
            self.productId.setText('')

        if self.productQuantity.text().isnumeric():
            pass
        else:
            self.productQuantity.setText('')

        if self.productUnit.text().isnumeric():
            pass
        else:
            self.productUnit.setText('')

        if self.productPurchasePrice.text().isnumeric():
            pass
        else:
            self.productPurchasePrice.setText('')

        if self.productRetailPrice.text().isnumeric():
            pass
        else:
            self.productRetailPrice.setText('')

        if self.productWholeSalePrice.text().isnumeric():
            pass
        else:
            self.productWholeSalePrice.setText('')

        if self.productTransportPrice.text().isnumeric():
            pass
        else:
            self.productTransportPrice.setText('')

        if self.productLowWarningLimit.text().isnumeric():
            pass
        else:
            self.productLowWarningLimit.setText('')

        if self.productGSTRate.text().isnumeric():
            pass
        else:
            self.productGSTRate.setText('')

    def insertProduct_AddNewItemWindow(self):

        conn = dbc.getConnection()
        cursor = conn.cursor()

        try:
            _productId = int(self.productId.text())
            _productName = self.productName.text()
            _productType = str(self.productType.currentText())
            _productCategory = str(self.productCategory.currentText())
            _productQuantity = int(self.productQuantity.text())
            _productUnit = int(self.productUnit.text())
            _productRetailPrice = int(self.productRetailPrice.text())
            _productWholeSalePrice = int(self.productWholeSalePrice.text())
            _productPurchasePrice = int(self.productPurchasePrice.text())
            _productTransportPrice = int(self.productTransportPrice.text())
            _productGSTRate = int(self.productGSTRate.text())
            _productLowWarningLimit = int(self.productLowWarningLimit.text())
            _productDetails = self.productDetail.toPlainText()
        except Exception as e:
            pass

        try:
            cursor.execute("insert into stock values(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                           (_productId, _productName, _productType,
                            _productCategory, _productQuantity, _productUnit, _productRetailPrice,
                            _productWholeSalePrice,
                            _productPurchasePrice, _productTransportPrice, _productGSTRate, _productDetails,
                            _productLowWarningLimit))
            conn.commit()
            conn.close()
        except Exception as e:
            print(e)


class EditItemWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("EditItemWindow.ui", self)
        self.setFixedSize(1000, 900)
        items = []
        completer = QCompleter(items)
        self.searchbar.setCompleter(completer)
        self.searchButton.clicked.connect(self.searchStock)
        self.productId.editingFinished.connect(self.validating)
        self.productQuantity.editingFinished.connect(self.validating)
        self.productUnit.editingFinished.connect(self.validating)
        self.productRetailPrice.editingFinished.connect(self.validating)
        self.productWholeSalePrice.editingFinished.connect(self.validating)
        self.productPurchasePrice.editingFinished.connect(self.validating)
        self.productTransportPrice.editingFinished.connect(self.validating)
        self.productGSTRate.editingFinished.connect(self.validating)
        self.productLowWarningLimit.editingFinished.connect(self.validating)
        self.initComboBox()
        self.saveButton.clicked.connect(self.updateProduct_EditItemWindow)

    def validating(self):

        if self.productId.text().isnumeric():
            pass
        else:
            self.productId.setText('')

        if self.productQuantity.text().isnumeric():
            pass
        else:
            self.productQuantity.setText('')

        if self.productUnit.text().isnumeric():
            pass
        else:
            self.productUnit.setText('')

        if self.productPurchasePrice.text().isnumeric():
            pass
        else:
            self.productPurchasePrice.setText('')

        if self.productRetailPrice.text().isnumeric():
            pass
        else:
            self.productRetailPrice.setText('')

        if self.productWholeSalePrice.text().isnumeric():
            pass
        else:
            self.productWholeSalePrice.setText('')

        if self.productTransportPrice.text().isnumeric():
            pass
        else:
            self.productTransportPrice.setText('')

        if self.productLowWarningLimit.text().isnumeric():
            pass
        else:
            self.productLowWarningLimit.setText('')

        if self.productGSTRate.text().isnumeric():
            pass
        else:
            self.productGSTRate.setText('')

    def updateProduct_EditItemWindow(self):

        conn = dbc.getConnection()
        cursor = conn.cursor()

        try:
            _productId = int(self.productId.text())
            _productName = self.productName.text()
            _productType = str(self.productType.currentText())
            _productCategory = str(self.productCategory.currentText())
            _productQuantity = int(self.productQuantity.text())
            _productUnit = int(self.productUnit.text())
            _productRetailPrice = int(self.productRetailPrice.text())
            _productWholeSalePrice = int(self.productWholeSalePrice.text())
            _productPurchasePrice = int(self.productPurchasePrice.text())
            _productTransportPrice = int(self.productTransportPrice.text())
            _productGSTRate = int(self.productGSTRate.text())
            _productLowWarningLimit = int(self.productLowWarningLimit.text())
            _productDetails = self.productDetail.toPlainText()
        except Exception as e:
            print(e)

        try:
            cursor.execute("insert or replace into stock values(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                           (_productId, _productName, _productType,
                            _productCategory, _productQuantity, _productUnit, _productRetailPrice,
                            _productWholeSalePrice,
                            _productPurchasePrice, _productTransportPrice, _productGSTRate, _productDetails,
                            _productLowWarningLimit))
            conn.commit()
            conn.close()
        except Exception as e:
            print(e)

    def initComboBox(self):
        conn = dbc.getConnection()
        cursor = conn.cursor()
        typeList = []
        categoryList = []

        try:
            cursor.execute("select * from type")
            for row in cursor:
                typeList.append(row[0])
            self.TypeBox.addItems(typeList)

            cursor.execute("select * from category")
            for row in cursor:
                categoryList.append(row[0])
            self.categoryBox.addItems(categoryList)
            conn.close()
        except Exception as e:
            print(e)

    def searchStock(self):
        conn = dbc.getConnection()
        cursor = conn.cursor()
        _searchItem = self.searchbar.text()
        try:
            cursor.execute("select * from stock where name =" +
                           "\"" + _searchItem + "\"")
            row = cursor.fetchone()
            self.productName_Edit.setText(f"{row[1]}")
            self.ProductID_Edit.setText(f"{row[0]}")
            self.categoryBox.setCurrentText(f"{row[3]}")
            self.TypeBox.setCurrentText(f"{row[2]}")
            self.PurchasePrice_Edit.setText(f"{row[8]}")
            self.TransportPrice_Edit.setText(f"{row[9]}")
            self.GST_Edit.setText(f"{row[10]}")
            self.spinBox.setValue(row[4])
            self.Quantity_Edit.setText(f"{row[5]}")
            self.LowQuantity_Edit.setText(f"{row[12]}")
            self.textEdit.setText(f"{row[11]}")
            self.WPrice_Edit.setText(f"{row[7]}")
            self.RPrice_Edit.setText(f"{row[6]}")

            conn.close()
        except Exception as e:
            print(e)


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
