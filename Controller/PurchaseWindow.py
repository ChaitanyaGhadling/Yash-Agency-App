from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QCompleter,QMessageBox, QTableWidgetItem
import MainWindow as mw
import StockWindow as stw
import DatabaseController as dbc
import NewPurchaseWindow as npw
import TransportWindow as tw


class PurchaseWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("Views/PurchaseWindow.ui", self)
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
        self.initTable()

    def goToNewPurchase(self):
        self.cw = npw.NewPurchaseWindow()
        self.cw.show()
        self.close()

    def goHome(self):
        self.cw = mw.MainWindow()
        self.cw.show()
        self.close()

    def goToTransport(self):
        self.cw = tw.TransportWindow()
        self.cw.show()

    def initTable(self):
        conn = dbc.getConnection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT date,purchase_id, item_name, supplier_name, contactno, place_of_supply, balance, "
                           "total_amount FROM purchase_list natural join purchase_item_list")
            rows = cursor.fetchall()

            self.purchaseTable.setRowCount(len(rows))
            self.purchaseTable.setColumnCount(9)
            for i, row in enumerate(rows):
                if row[6] > 0:
                    status = 'Pending'
                else:
                    status = 'Completed'
                self.purchaseTable.setItem(i, 0, QTableWidgetItem(f"{i + 1}"))
                self.purchaseTable.setItem(i, 1, QTableWidgetItem(status))
                self.purchaseTable.setItem(i, 2, QTableWidgetItem(row[0]))
                self.purchaseTable.setItem(i, 3, QTableWidgetItem(row[1]))
                self.purchaseTable.setItem(i, 4, QTableWidgetItem(str(row[2])))
                self.purchaseTable.setItem(i, 5, QTableWidgetItem(str(row[3])))
                self.purchaseTable.setItem(i, 6, QTableWidgetItem(str(row[4])))
                self.purchaseTable.setItem(i, 7, QTableWidgetItem(str(row[5])))
                self.purchaseTable.setItem(i, 8, QTableWidgetItem(str(row[7])))
            conn.close()
        except Exception as e:
            print(f"Error updating table: {e}")
            QMessageBox.critical(self, "Database Error", f"Failed to update table: {e}")
        finally:
            if conn:
                conn.close()


