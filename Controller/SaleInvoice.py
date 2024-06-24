from PyQt6 import uic
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QDialog, QMessageBox
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
import DatabaseController as dbc


class SaleInvoice(QWidget):
    def __init__(self, pos_window, customer_name, table_values, total, payment, amount_due, parent=None):
        super().__init__(parent)
        try:
            uic.loadUi("Views/SaleInvoiceWindow.ui", self)
            self.setFixedSize(1000, 870)
            self.pos_window = pos_window
            self.table_values = table_values
            self.invoiceTable.setColumnWidth(0, 150)
            self.invoiceTable.setColumnWidth(1, 250)
            self.invoiceTable.setColumnWidth(2, 175)
            self.invoiceTable.setColumnWidth(3, 175)
            self.invoiceTable.setColumnWidth(4, 100)
            self.invoiceTable.setColumnWidth(5, 100)
            # Check if elements exist
            self.printButton.clicked.connect(self.print_invoice)
            self.saveWithoutPrintingButton.clicked.connect(self.sell_without_printing)
            # Set the text of the labels
            self.customerNameLabel.setText(customer_name)
            self.grandTotalLabel.setText(total)
            self.paymentLabel.setText(payment)
            self.amountDueLabel.setText(amount_due)
            self.dateLabel.setText(QDate.currentDate().toString("yyyy-MM-dd"))
            # Populate the table
            self.invoiceTable.setRowCount(len(self.table_values))
            self.invoiceTable.setColumnCount(len(self.table_values[0]))
            for row_num, row_data in enumerate(self.table_values):
                for col_num, col_data in enumerate(row_data):
                    self.invoiceTable.setItem(row_num, col_num, QTableWidgetItem(col_data))
            conn = dbc.getConnection()
            cursor = conn.cursor()
            cursor.execute("SELECT saleId FROM sales ORDER BY saleId DESC LIMIT 1;")
            self.saleId = cursor.fetchone()  # Fetch the first column of the first row
            if not self.saleId:
                self.saleId = 1
            print(self.saleId)
            self.invoiceNoLabel.setText(str(self.saleId+1))
        except Exception as e:
            print("An error occurred during initialization:", e)

    def print_invoice(self):
        try:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            print_dialog = QPrintDialog(printer, self)
            if print_dialog.exec() == QDialog.DialogCode.Accepted:
                painter = QPainter(printer)

                # Calculate the scale factor
                rect = painter.viewport()
                size = self.size()
                scale_factor = min(rect.width() / size.width(), rect.height() / size.height())
                painter.scale(scale_factor, scale_factor)
                # Render the widget
                self.render(painter)
                painter.end()
                self.sell_without_printing()
        except Exception as e:
            print("An error occurred while printing the invoice:", e)

    def sell_without_printing(self):
        conn = dbc.getConnection()
        cursor = conn.cursor()
        try:
            sale_data = (
                int(self.invoiceNoLabel.text()),
                self.customerNameLabel.text(),
                self.dateLabel.text(),
                float(self.grandTotalLabel.text()),
                float(self.paymentLabel.text()),
                float(self.amountDueLabel.text())
            )
            # Insert into sales table
            cursor.execute("""
                INSERT INTO sales (saleId, customerName, date, grandTotal, payment, amountDue)
                VALUES (?, ?, ?, ?, ?, ?)
            """, sale_data)

            sale_id = self.saleId
            # Insert into itemSales table
            for row_data in self.table_values:
                product_id = int(row_data[0])  # Assuming the product ID is the first column
                quantity_sold = int(row_data[3])  # Assuming the quantity sold is the fourth column
                unit_price = float(row_data[2])  # Assuming the unit price is the fifth column
                total_amount = float(row_data[4])

                item_sale_data = (sale_id, product_id, quantity_sold, unit_price, total_amount)
                cursor.execute("""
                    INSERT INTO itemSales (saleId, productId, quantitySold, unitPrice, totalAmount)
                    VALUES (?, ?, ?, ?, ?)
                """, item_sale_data)

            conn.commit()  # Commit the transaction
            # Update stock quantities
            for row_data in self.table_values:
                product_id = int(row_data[0])  # Assuming the product ID is the first column
                quantity_sold = int(row_data[3])  # Assuming the quantity sold is the fourth column

                # Update the stock quantity
                cursor.execute(
                    "UPDATE stock SET quantity = quantity - ? WHERE id = ?",
                    (quantity_sold, product_id)
                )
            conn.commit()  # Commit the transaction
            self.close()
            self.pos_window.clear()
        except Exception as e:
            print(f"Error selling without printing: {e}")
            QMessageBox.critical(self, "Database Error", f"Failed to sell without printing: {e}")
            conn.rollback()  # Rollback changes
        finally:
            conn.close()
