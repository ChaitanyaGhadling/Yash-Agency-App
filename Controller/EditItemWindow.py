from PyQt6 import uic
from PyQt6.QtGui import QIntValidator, QDoubleValidator, QValidator
from PyQt6.QtWidgets import QWidget, QCompleter, QTableWidgetItem, QMessageBox
import MainWindow as mw
import DatabaseController as dbc
from datetime import datetime


class EditItemWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("Views/EditItemWindow.ui", self)
        self.setFixedSize(1000, 900)
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
        self.saveButton.clicked.connect(self.updateProduct_EditItemWindow)

        self.initComboBox()
        items = []
        completer = QCompleter(items)
        self.searchbar.setCompleter(completer)
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
        self.searchbar.setCompleter(completer)

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

        if self.productPurchasePrice.text().isnumeric() and int(self.productPurchasePrice.text()) != 0:
            pass
        else:
            self.productPurchasePrice.setText('')

        if self.productRetailPrice.text().isnumeric() and int(self.productRetailPrice.text()) != 0:
            pass
        else:
            self.productRetailPrice.setText('')

        if self.productWholeSalePrice.text().isnumeric() and int(self.productWholeSalePrice.text()) != 0:
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
            total_cost_price = float(self.productPurchasePrice.text()) + float(self.productTransportPrice.text())
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
            _productRetailPrice = float(self.productRetailPrice.text())
            _productWholeSalePrice = float(self.productWholeSalePrice.text())
            _productPurchasePrice = float(self.productPurchasePrice.text())
            _productTransportPrice = float(self.productTransportPrice.text())
            _productGSTRate = float(self.productGSTRate.text())
            _productLowWarningLimit = int(self.productLowWarningLimit.text())
            _productDetails = self.productDetails.toPlainText()
            current_date = datetime.now().date()
            _lastModifiedDate = current_date.strftime("%Y-%m-%d")
        except Exception as e:
            print(e)

        try:
            cursor.execute("insert or replace into stock values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                           (_productId, _productName, _productType,
                            _productCategory, _productQuantity, _productUnit, _productRetailPrice,
                            _productWholeSalePrice,
                            _productPurchasePrice, _productTransportPrice, _productGSTRate, _productDetails,
                            _productLowWarningLimit, _lastModifiedDate))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "Product updated successfully")
            self.productId.setText('')
            self.productName.setText('')
            self.productQuantity.setText('')
            self.productUnit.setValue(0)
            self.productPurchasePrice.setText('')
            self.productRetailPrice.setText('')
            self.productWholeSalePrice.setText('')
            self.productTransportPrice.setText('')
            self.productLowWarningLimit.setText('')
            self.productGSTRate.setText('0')
            self.RProfit_label.setText('')
            self.WProfit_label.setText('')
            self.TCP_label.setText('')
            self.CPU_label.setText('')
            self.productType.setCurrentIndex(0)
            self.productCategory.setCurrentIndex(0)
            self.close()
        except Exception as e:
            print(e)

    def initComboBox(self):
        conn = dbc.getConnection()
        cursor = conn.cursor()
        typeList = ['']
        categoryList = ['']

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

    def searchStock(self):
        conn = dbc.getConnection()
        cursor = conn.cursor()
        _searchItem = self.searchbar.text()
        try:
            cursor.execute("select * from stock where name =" +
                           "\"" + _searchItem + "\"")
            row = cursor.fetchone()
            self.productId.setText(f"{row[0]}")
            self.productName.setText(f"{row[1]}")
            self.productType.setCurrentText(f"{row[2]}")
            self.productCategory.setCurrentText(f"{row[3]}")
            self.productQuantity.setText(f"{row[4]}")
            self.productUnit.setValue(row[5])
            self.productRetailPrice.setText(f"{row[6]}")
            self.productWholeSalePrice.setText(f"{row[7]}")
            self.productPurchasePrice.setText(f"{row[8]}")
            self.productTransportPrice.setText(f"{row[9]}")
            self.productGSTRate.setText(f"{row[10]}")
            self.productDetails.setText(f"{row[11]}")
            self.productLowWarningLimit.setText(f"{row[12]}")
            self.date_label.setText(f"{row[13]}")
            total_cost_price = float(self.productPurchasePrice.text()) + float(self.productTransportPrice.text())
            cost_per_unit = total_cost_price / int(self.productQuantity.text())
            self.TCP_label.setText(str(total_cost_price))
            self.CPU_label.setText(str(cost_per_unit))
            retailProfit = (float(self.productRetailPrice.text()) - float(self.CPU_label.text())) * 100 / float(
                self.CPU_label.text())
            self.RProfit_label.setText(f"{retailProfit:.2f}")
            wholesaleProfit = (float(self.productWholeSalePrice.text()) - float(
                self.CPU_label.text())) * 100 / float(self.CPU_label.text())
            self.WProfit_label.setText(f"{wholesaleProfit:.2f}")
            conn.close()
        except Exception as e:
            print(e)