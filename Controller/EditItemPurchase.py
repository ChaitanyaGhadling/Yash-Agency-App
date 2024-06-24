from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QCompleter, QTableWidgetItem, QMessageBox
from PyQt6.QtCore import pyqtSignal
import DatabaseController as dbc
from datetime import datetime


class EditItemPurchase(QWidget):
    closed = pyqtSignal()  # Signal emitted when the window is closed

    def __init__(self, item_name, quantity, unit, purchase_price, gst, transport_price, parent=None):
        super().__init__(parent)
        uic.loadUi("Views/EditItemPurchase.ui", self)
        self.setFixedSize(1000, 900)
        self.item_name = item_name
        self.quantity = quantity
        self.unit = unit
        self.purchase_price = purchase_price
        self.transport_price = transport_price
        self.saveButton.clicked.connect(self.save)
        self.gst = gst
        self.productRetailPrice.textEdited.connect(self.validating)
        self.productWholeSalePrice.textEdited.connect(self.validating)
        self.initUI()

    def validating(self):
        cpu_text = self.CPU_label.text()
        wholesale_price_text = self.productWholeSalePrice.text()
        retail_price_text = self.productRetailPrice.text()

        if cpu_text and wholesale_price_text:
            try:
                wholesaleProfit = (float(wholesale_price_text) - float(cpu_text)) * 100 / float(cpu_text)
                self.WProfit_label.setText(f"{wholesaleProfit:.2f}")
            except ValueError as e:
                print("Error calculating wholesale profit:", e)

        if cpu_text and retail_price_text:
            try:
                retailProfit = (float(retail_price_text) - float(cpu_text)) * 100 / float(cpu_text)
                self.RProfit_label.setText(f"{retailProfit:.2f}")
            except ValueError as e:
                print("Error calculating retail profit:", e)

    def initUI(self):
        conn = dbc.getConnection()
        cursor = conn.cursor()
        try:
            cursor.execute("select * from stock where name = ?", (self.item_name,))
            result = cursor.fetchone()
            if result:
                self.productId.setText(str(result[0]))
                self.productName.setText(str(result[1]))
                self.productType.setText(str(result[2]))
                self.productCategory.setText(str(result[3]))
                self.prevQuantity.setText(str(result[4]))
                self.productUnit.setValue(result[5])
                self.productRetailPrice.setText(str(result[6]))
                self.productWholeSalePrice.setText(str(result[7]))
                self.prevPurchasePrice.setText(str(result[8]))
                self.prevTransportPrice.setText(str(result[9]))
                self.prevGSTRate.setText(str(result[10]))
                self.productDetails.setText(str(result[11]))
                self.productLowWarningLimit.setText(str(result[12]))
                self.date_label.setText(str(result[13]))
                self.newQuantity.setText(str(int(self.prevQuantity.text()) + int(self.quantity)))
                self.newGSTRate.setText(str(self.gst))
                self.newPurchasePrice.setText(str(self.purchase_price))
                self.newTransportPrice.setText(str(self.transport_price))
                total_cost_price = float(self.newPurchasePrice.text()) + float(self.newTransportPrice.text())
                cost_per_unit = total_cost_price / float(self.quantity)
                self.TCP_label.setText(f"{total_cost_price:.2f}")
                self.CPU_label.setText(f"{cost_per_unit:.2f}")

                retailProfit = (float(self.productRetailPrice.text()) - float(self.CPU_label.text())) * 100 / float(
                    self.CPU_label.text())
                self.RProfit_label.setText(f"{retailProfit:.2f}")
                wholesaleProfit = (float(self.productWholeSalePrice.text()) - float(
                    self.CPU_label.text())) * 100 / float(self.CPU_label.text())
                self.WProfit_label.setText(f"{wholesaleProfit:.2f}")
            conn.close()
        except Exception as e:
            print(f"Error updating table: {e}")
            QMessageBox.critical(self, "Database Error", f"Failed to update table: {e}")
        finally:
            if conn:
                conn.close()

    def save(self):
        conn = dbc.getConnection()
        cursor = conn.cursor()
        try:
            _productId = int(self.productId.text())
            _productName = self.productName.text()
            _productType = str(self.productType.text())
            _productCategory = str(self.productCategory.text())
            _productQuantity = int(self.newQuantity.text())
            _productUnit = int(self.productUnit.text())
            _productRetailPrice = float(self.productRetailPrice.text())
            _productWholeSalePrice = float(self.productWholeSalePrice.text())
            _productPurchasePrice = float(self.newPurchasePrice.text())
            _productTransportPrice = float(self.newTransportPrice.text())
            _productGSTRate = float(self.newGSTRate.text())
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
        except Exception as e:
            print(e)
        self.close()

    def closeEvent(self, event):
        self.closed.emit()  # Emit the closed signal
        event.accept()
