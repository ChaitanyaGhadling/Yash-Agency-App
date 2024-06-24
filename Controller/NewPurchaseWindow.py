from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QCompleter, QTableWidgetItem, QMessageBox, QApplication
import MainWindow as mw
import StockWindow as stw
import DatabaseController as dbc
import PurchaseWindow as pw
import AddSupplierWindow as asw
import EditItemPurchase as eip
import AddNewItemWindow as aniw
from PyQt6.QtCore import QDate, QEventLoop
from sqlite3 import IntegrityError

class NewPurchaseWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("Views/NewPurchaseWindow.ui", self)
        self.setFixedSize(1900, 980)
        self.dateEdit.setDate(QDate.currentDate())
        self.saveButton.clicked.connect(self.addNewPurchase)
        self.homeButton.clicked.connect(self.goHome)
        self.backButton.clicked.connect(self.goBack)
        self.addItemButton.clicked.connect(self.goToAddNewItem)
        self.addItem.clicked.connect(self.insertIntoTable)
        self.deleteItem.clicked.connect(self.deleteFromTable)
        self.addSupplier.clicked.connect(self.addNewSupplier)
        self.unit.editingFinished.connect(self.validating)
        self.quantity.editingFinished.connect(self.validating)
        self.purchasePrice.editingFinished.connect(self.validating)
        self.gst.editingFinished.connect(self.validating)
        self.shipAmount_Edit.editingFinished.connect(self.validating)
        self.amountPaid_Edit.textEdited.connect(self.validating)
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
        self.cw = asw.AddSupplierWindow()
        self.cw.show()
        newSupplier = self.cw.companyName.text()
        self.supplier_CB.addItem(newSupplier)

    def goHome(self):
        self.cw = mw.MainWindow()
        self.cw.show()
        self.close()

    def goBack(self):
        self.cw = pw.PurchaseWindow()
        self.cw.show()
        self.close()

    def goToAddNewItem(self):
        self.cw = aniw.AddNewItemWindow()
        self.cw.show()
        self.cw.productName

    def validating(self):
        if not self.unit.text().isnumeric():
            self.unit.setText('')

        if not self.purchaseId.text().isnumeric():
            self.purchaseId.setText('')

        if not self.quantity.text().isnumeric():
            self.quantity.setText('')

        if not self.purchasePrice.text().isnumeric():
            self.purchasePrice.setText('')

        if not self.gst.text().isnumeric():
            self.gst.setText('0')

        if self.purchasePrice.text() and self.gst.text():
            purchase_price = float(self.purchasePrice.text())
            gst = float(self.gst.text())
            final_amount = purchase_price + (gst * purchase_price / 100)
            self.finalAmount.setText(f"{final_amount:.2f}")

        if self.shipAmount_Edit.text() and self.subAmount_label.text():
            if self.shipAmount_Edit.text():
                totalAmount = float(self.subAmount_label.text()) + float(self.shipAmount_Edit.text())
            else:
                totalAmount = float(self.subAmount_label.text())
            self.tamount_label.setText(f"{totalAmount}")
        if self.tamount_label.text() and self.amountPaid_Edit.text():
            balanceAmount = float(self.tamount_label.text()) - float(self.amountPaid_Edit.text())
            self.balance_Edit.setText(f"{balanceAmount}")

    def deleteFromTable(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            final_amount_item = self.table.item(selected_row, 6)
            if final_amount_item:
                final_amount = float(final_amount_item.text())
                current_amount = float(self.subAmount_label.text()) if self.subAmount_label.text() else 0
                new_amount = current_amount - final_amount
                self.subAmount_label.setText(f"{new_amount:.2f}")

                if self.shipAmount_Edit.text():
                    totalAmount = new_amount + float(self.shipAmount_Edit.text())
                else:
                    totalAmount = new_amount
                self.tamount_label.setText(f"{totalAmount:.2f}")
                if self.tamount_label.text():
                    if not self.amountPaid_Edit.text():
                        self.amountPaid_Edit.setText('0')
                    balanceAmount = float(self.tamount_label.text()) - float(self.amountPaid_Edit.text())
                    self.balance_Edit.setText(f"{balanceAmount}")

            self.table.removeRow(selected_row)

            for row in range(selected_row, self.table.rowCount()):
                self.table.setItem(row, 0, QTableWidgetItem(f"{row + 1}"))

        else:
            QMessageBox.warning(self, "Selection Error", "Please select a row to delete.")

    def insertIntoTable(self):
        item_name = self.itemName.text()
        quantity = self.quantity.text()
        unit = self.unit.text()
        purchase_price = self.purchasePrice.text()
        gst = self.gst.text()
        final_amount = self.finalAmount.text()

        if not item_name or not quantity or not unit or not purchase_price or not gst or not final_amount:
            QMessageBox.warning(self, "Input Error", "Please ensure all fields are filled in correctly.")
            return
        # self.EditItemPurchase = eip.EditItemPurchase(item_name, quantity, unit, purchase_price, gst)
        # self.EditItemPurchase.show()
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(f"{row_position + 1}"))
        self.table.setItem(row_position, 1, QTableWidgetItem(item_name))
        self.table.setItem(row_position, 2, QTableWidgetItem(quantity))
        self.table.setItem(row_position, 3, QTableWidgetItem(unit))
        self.table.setItem(row_position, 4, QTableWidgetItem(purchase_price))
        self.table.setItem(row_position, 5, QTableWidgetItem(gst))
        self.table.setItem(row_position, 6, QTableWidgetItem(final_amount))
        try:
            # Check if subAmount_label is empty, if so, set current_amount to 0
            if self.subAmount_label.text():
                current_amount = float(self.subAmount_label.text())
            else:
                current_amount = 0

            final_amount = float(self.finalAmount.text())  # Ensure final_amount is a float
            new_amount = current_amount + final_amount  # Perform the addition

            self.subAmount_label.setText(f"{new_amount:.2f}")  # Set the new amount with 2 decimal places
            if self.shipAmount_Edit.text():
                totalAmount = float(self.subAmount_label.text()) + float(self.shipAmount_Edit.text())
            else:
                totalAmount = float(self.subAmount_label.text())
            self.tamount_label.setText(f"{totalAmount}")
            if self.tamount_label.text():
                if not self.amountPaid_Edit.text():
                    self.amountPaid_Edit.setText('0')
                balanceAmount = float(self.tamount_label.text()) - float(self.amountPaid_Edit.text())
                self.balance_Edit.setText(f"{balanceAmount}")
        except ValueError:
            # Handle the error if the text is not a valid number
            QMessageBox.warning(self, "Input Error", "Invalid number format in subAmount_label or finalAmount")

    def addNewPurchase(self):
        try:
            conn = dbc.getConnection()
            cursor = conn.cursor()
            _purchaseId = self.purchaseId.text()
            _orderType = self.orderType_CB.currentText()
            _supplierName = self.supplier_CB.currentText()
            _date = self.dateEdit.date().toString("yyyy-MM-dd")
            _contactNo = self.contact_Edit.text()
            _place_of_supply = self.place_Edit.text()
            _transportCost = self.shipAmount_Edit.text()
            _remarks = self.remarksTextEdit.toPlainText()
            _paymentMode = self.paymode_CB.currentText()
            _amountPaid = self.amountPaid_Edit.text()
            _transactionId = self.transactionId_Edit.text()
            _balance = self.balance_Edit.text()
            _totalAmount = self.tamount_label.text()
            cursor.execute(
                "INSERT INTO purchase_list (purchase_id, order_type, supplier_name, date, contactno, place_of_supply, "
                "transport_cost, remarks, paymentmode, amount_paid, transactionId, balance, total_amount) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (_purchaseId, _orderType, _supplierName, _date, _contactNo, _place_of_supply, _transportCost, _remarks,
                 _paymentMode, _amountPaid, _transactionId, _balance, _totalAmount))

            for row in range(self.table.rowCount()):
                _purchaseId = self.purchaseId.text()
                _itemName = self.table.item(row, 1).text()
                _quantity = self.table.item(row, 2).text()
                _unit = self.table.item(row, 3).text()
                _purchasePrice = self.table.item(row, 4).text()
                _gst = self.table.item(row, 5).text()
                _finalAmount = self.table.item(row, 6).text()
                _transportPrice = round((float(_finalAmount)/float(_totalAmount))*float(_transportCost), 2)
                cursor.execute(
                    "INSERT INTO purchase_item_list (purchase_id, item_name, quantity, unit, gst, price) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (_purchaseId, _itemName, _quantity, _unit, _gst, _finalAmount))
                conn.commit()

                self.EditItemPurchase = eip.EditItemPurchase(_itemName, _quantity, _unit, _purchasePrice, _gst,
                                                             _transportPrice)

                self.EditItemPurchase.show()
                while self.EditItemPurchase.isVisible():
                    QApplication.processEvents()
            QMessageBox.information(self, "Success", "Purchase and items added successfully.")
            self.goBack()
        except IntegrityError as e:
            print("UNIQUE constraint failed:", e)
            QMessageBox.warning(self, "Duplicate ID", "PurchaseID already exists.")
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "Error", f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()





