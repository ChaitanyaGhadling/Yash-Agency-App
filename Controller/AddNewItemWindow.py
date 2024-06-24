from PyQt6 import uic
from PyQt6.QtGui import QIntValidator, QDoubleValidator, QValidator
from PyQt6.QtWidgets import QWidget, QCompleter, QTableWidgetItem, QMessageBox
import MainWindow as mw
import DatabaseController as dbc
from datetime import datetime
from sqlite3 import IntegrityError


class AddNewItemWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("Views/AddNewItemWindow.ui", self)
        self.setFixedSize(1000, 900)
        self.saveButton.clicked.connect(self.insertProduct_AddNewItemWindow)
        self.productUnit.setText('1')
        self.productId.editingFinished.connect(self.validating)
        self.productQuantity.editingFinished.connect(self.validating)
        self.productUnit.textEdited.connect(self.validating)
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
            self.productUnit.setText('1')

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
            self.productGSTRate.setText('0')
        if all([self.productPurchasePrice.text(), self.productTransportPrice.text(), self.productUnit.text(),
                self.productQuantity.text()]):
            total_cost_price = float(self.productPurchasePrice.text()) + float(self.productTransportPrice.text()) + \
                               float(self.productPurchasePrice.text())* (float(self.productGSTRate.text())/100)
            cost_per_unit = total_cost_price / int(self.productQuantity.text())
            self.TCP_label.setText(str(total_cost_price))
            self.CPU_label.setText(str(cost_per_unit))

        # Calculate Wholesale Profit
        if all([self.CPU_label.text(), self.productWholeSalePrice.text()]):
            try:
                wholesaleProfit = (float(self.productWholeSalePrice.text()) - float(
                    self.CPU_label.text())) * 100 / float(self.CPU_label.text())
                self.WProfit_label.setText(f"{wholesaleProfit:.2f}")
            except Exception as e:
                print("Error calculating wholesale profit:", e)

        # Calculate Retail Profit
        if all([self.CPU_label.text(), self.productRetailPrice.text()]):
            try:
                retailProfit = (float(self.productRetailPrice.text()) - float(self.CPU_label.text())) * 100 / float(
                    self.CPU_label.text())
                self.RProfit_label.setText(f"{retailProfit:.2f}")
            except Exception as e:
                print("Error calculating retail profit:", e)

    def insertProduct_AddNewItemWindow(self):
        conn = dbc.getConnection()
        cursor = conn.cursor()
        try:
            _productId = int(self.productId.text())
            _productName = self.productName.text()
            _productType = str(self.productType.currentText())
            _productCategory = str(self.productCategory.currentText())
            _productQuantity = int(self.productQuantity.text() or 0)
            _productUnit = int(self.productUnit.text() or 0)
            _productRetailPrice = float(self.productRetailPrice.text() or 0)
            _productWholeSalePrice = float(self.productWholeSalePrice.text() or 0)
            _productPurchasePrice = float(self.productPurchasePrice.text() or 0)
            _productTransportPrice = float(self.productTransportPrice.text() or 0)
            _productGSTRate = float(self.productGSTRate.text() or 0)
            _productLowWarningLimit = int(self.productLowWarningLimit.text() or 0)
            _productDetails = self.productDetails.toPlainText()
            current_date = datetime.now().date()
            _lastModifiedDate = current_date.strftime("%Y-%m-%d")
        except Exception as e:
            print(e)
        try:
            cursor.execute("insert into stock values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                           (_productId, _productName, _productType,
                            _productCategory, _productQuantity, _productUnit, _productRetailPrice,
                            _productWholeSalePrice,
                            _productPurchasePrice, _productTransportPrice, _productGSTRate, _productDetails,
                            _productLowWarningLimit, _lastModifiedDate))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "Product Added successfully")
            self.productId.setText('')
            self.productName.setText('')
            self.productQuantity.setText('')
            self.productUnit.setText('')
            self.productPurchasePrice.setText('')
            self.productRetailPrice.setText('')
            self.productWholeSalePrice.setText('')
            self.productTransportPrice.setText('')
            self.productLowWarningLimit.setText('')
            self.productGSTRate.setText('')
            self.productType.setCurrentIndex(0)
            self.productCategory.setCurrentIndex(0)
            self.productDetails.setText('')
            self.close()
        except IntegrityError as e:
            print("UNIQUE constraint failed:", e)
            QMessageBox.warning(self, "Duplicate ID", "A product with the same ID already exists.")
