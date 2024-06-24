from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QCompleter, QMessageBox, QTableWidgetItem, QPushButton
import MainWindow as mw
import DatabaseController as dbc
import SaleInvoice as si

class PointOfSaleWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("Views/PointOfSale.ui", self)
        self.setFixedSize(1900, 980)

        self.homeButton.clicked.connect(self.goHome)
        self.completeSaleButton.clicked.connect(self.completeSale)
        self.clearButton.clicked.connect(self.clear)
        self.initComboBox()
        self.productsTable.setColumnWidth(0, 150)
        self.productsTable.setColumnWidth(1, 250)
        self.productsTable.setColumnWidth(2, 175)
        self.productsTable.setColumnWidth(3, 175)
        self.productsTable.setColumnWidth(4, 100)
        self.productsTable.setColumnWidth(5, 100)
        self.initTable()
        self.productsTable.itemDoubleClicked.connect(self.transferToCart)
        self.searchButton.clicked.connect(self.updateTable)
        self.productCategory.currentIndexChanged.connect(self.updateTable)
        self.productType.currentIndexChanged.connect(self.updateTable)
        self.cartTable.cellChanged.connect(self.updateAmount)
        self.paymentLineEdit.textEdited.connect(self.validating)

    def goHome(self):
        self.cw = mw.MainWindow()
        self.cw.show()
        self.close()

    def validating(self):
        payment_text = self.paymentLineEdit.text()
        if not payment_text or payment_text == '0':
            self.paymentLineEdit.setText('0')
        else:
            try:
                amount_due = float(self.grandTotal.text()) - float(payment_text)
                self.amountDue.setText(str(amount_due))
            except ValueError:
                self.amountDue.setText(self.grandTotal.text())

    def clear(self):
        self.cartTable.setRowCount(0)
        self.grandTotal.setText('0')
        self.amountDue.setText('0')
        self.paymentLineEdit.setText('0')
        self.customerName.setText('')
        self.updateTable()

    def completeSale(self):
        customer_name = self.customerName.text()
        table_values = []
        for row in range(self.cartTable.rowCount()):
            row_data = []
            for column in range(self.cartTable.columnCount()-1):
                item = self.cartTable.item(row, column)
                if item is not None:
                    row_data.append(item.text())
            table_values.append(row_data)
        total = self.grandTotal.text()
        amount_due = self.amountDue.text()
        payment = self.paymentLineEdit.text()
        self.siw = si.SaleInvoice(self, customer_name, table_values, total, payment, amount_due)
        self.siw.show()

    def initComboBox(self):
        conn = dbc.getConnection()
        cursor = conn.cursor()
        typeList = ["All"]
        categoryList = ["All"]
        items = []

        try:
            # Populate type combo box
            cursor.execute("SELECT type FROM type")
            typeList.extend([row[0] for row in cursor])
            self.productType.addItems(typeList)

            # Populate category combo box
            cursor.execute("SELECT category FROM category")
            categoryList.extend([row[0] for row in cursor])
            self.productCategory.addItems(categoryList)

            # Populate search bar completer
            cursor.execute("SELECT name FROM stock")
            items.extend([row[0] for row in cursor])
            completer = QCompleter(items)
            self.searchbar.setCompleter(completer)
        except Exception as e:
            print(f"Error initializing combo boxes: {e}")
            QMessageBox.critical(self, "Error", f"Failed to initialize combo boxes: {e}")
        finally:
            conn.close()

    def initTable(self):

        conn = dbc.getConnection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, name, type, category, retail_price, quantity FROM stock")
            rows = cursor.fetchall()

            self.productsTable.setRowCount(len(rows))
            self.productsTable.setColumnCount(6)

            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    self.productsTable.setItem(i, j, QTableWidgetItem(str(value)))
        except Exception as e:
            print(f"Error updating table: {e}")
            QMessageBox.critical(self, "Database Error", f"Failed to update table: {e}")
        finally:
            conn.close()

    def updateTable(self):
        conn = dbc.getConnection()
        cursor = conn.cursor()
        try:
            searchItem = "%" + self.searchbar.text() + "%"
            selectedCategory = self.productCategory.currentText()
            selectedType = self.productType.currentText()
            if selectedCategory == "All":
                selectedCategory = None
            if selectedType == "All":
                selectedType = None

            query = """
                SELECT id, name, type, category, retail_price, quantity
                FROM stock
                WHERE name LIKE ?
            """
            params = [searchItem]

            if selectedCategory:
                query += " AND category = ?"
                params.append(selectedCategory)

            if selectedType:
                query += " AND type = ?"
                params.append(selectedType)

            cursor.execute(query, params)
            results = cursor.fetchall()
            self.productsTable.setColumnCount(6)
            self.productsTable.setRowCount(len(results))
            for i, row in enumerate(results):
                for j, value in enumerate(row):
                    self.productsTable.setItem(i, j, QTableWidgetItem(str(value)))
        except Exception as e:
            print(f"Error updating table: {e}")
            QMessageBox.critical(self, "Database Error", f"Failed to update table: {e}")
        finally:
            conn.close()

    def transferToCart(self, item):
        row = item.row()
        cart_row = []
        transfer_index = [0, 1, 4]  # Indices for id, name, retail_price
        for i in transfer_index:
            cart_row.append(self.productsTable.item(row, i).text())
        # Calculate amount
        unit_price = float(cart_row[2])
        quantity = 1  # Default quantity
        amount = unit_price * quantity
        cart_row.extend([str(quantity), str(amount), "Delete"])
        self.addToCartTable(cart_row)

    def addToCartTable(self, row_data):
        row_position = self.cartTable.rowCount()
        self.cartTable.insertRow(row_position)
        for i, data in enumerate(row_data):
            self.cartTable.setItem(row_position, i, QTableWidgetItem(data))

        # Add delete button
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda: self.removeCartItem(delete_button))
        self.cartTable.setCellWidget(row_position, 5, delete_button)

    def removeCartItem(self, button):
        row = self.cartTable.indexAt(button.pos()).row()
        item = self.cartTable.item(row, 4)
        if item:
            amount = float(item.text())
            self.cartTable.removeRow(row)
            grand_total = float(self.grandTotal.text()) - amount
            self.grandTotal.setText(str(grand_total))
            self.amountDue.setText(str(grand_total))
        else:
            print("No item found in row:", row)

    def updateAmount(self, row, column):
        if column == 3:  # Check if the edited cell is in the quantity column
            quantity_item = self.cartTable.item(row, 3)
            unit_price_item = self.cartTable.item(row, 2)
            if quantity_item and unit_price_item:
                try:
                    quantity = int(quantity_item.text())
                    unit_price = float(unit_price_item.text())
                    amount = quantity * unit_price
                    amount_item = QTableWidgetItem(str(amount))
                    self.cartTable.setItem(row, 4, amount_item)
                except ValueError:
                    QMessageBox.critical(self, "Input Error", "Please enter a valid number for quantity.")

        # Update grandTotal
        grand_total = 0.0
        for row in range(self.cartTable.rowCount()):
            amount_item = self.cartTable.item(row, 4)
            if amount_item:
                grand_total += float(amount_item.text())
        self.grandTotal.setText(str(grand_total))
        try:
            amount_due = grand_total - float(self.paymentLineEdit.text())
            self.amountDue.setText(str(amount_due))
        except ValueError:
            self.amountDue.setText(str(grand_total))

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = PointOfSaleWindow()
    window.show()
    sys.exit(app.exec())
