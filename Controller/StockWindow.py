from PyQt6 import uic
from PyQt6.QtGui import QIntValidator, QDoubleValidator, QValidator
from PyQt6.QtWidgets import QWidget, QCompleter, QTableWidgetItem, QMessageBox
import MainWindow as mw
import NewCategoryWindow as ncw
import NewTypeWindow as ntw
import UpdateQuantityWindow as uqw
import DefectiveItemWindow as diw
import EditItemWindow as eiw
import AddNewItemWindow as aniw
import DatabaseController as dbc



class StockWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("Views/StockWindow.ui", self)
        self.setFixedSize(1900, 980)
        self.homeButton.clicked.connect(self.goHome)
        self.categoryButton.clicked.connect(self.goToCategory)
        self.typeButton.clicked.connect(self.goToType)
        self.newItemButton.clicked.connect(self.goToAddNewItem)
        self.editItemButton.clicked.connect(self.goToEditItem)
        self.defectiveItemButton.clicked.connect(self.goToDefectiveItem)
        self.updateQuantityButton.clicked.connect(self.goToUpdateQuantity)
        self.searchButton.clicked.connect(self.updateTable)
        self.productCategory.currentIndexChanged.connect(self.updateTable)
        self.productType.currentIndexChanged.connect(self.updateTable)
        self.stockTable.setColumnWidth(0, 130)
        self.stockTable.setColumnWidth(1, 580)
        self.stockTable.setColumnWidth(2, 210)
        self.stockTable.setColumnWidth(3, 210)
        self.stockTable.setColumnWidth(4, 100)
        self.stockTable.setColumnWidth(5, 125)
        self.stockTable.setColumnWidth(6, 125)
        self.stockTable.setColumnWidth(7, 165)
        self.initTable()
        self.initComboBox()

    def initComboBox(self):
        conn = dbc.getConnection()
        cursor = conn.cursor()
        typeList = ["All"]
        categoryList = ["All"]
        items = []

        try:
            # Populate type combo box
            cursor.execute("SELECT type FROM type")
            for row in cursor:
                typeList.append(row[0])
            self.productType.addItems(typeList)

            # Populate category combo box
            cursor.execute("SELECT category FROM category")
            for row in cursor:
                categoryList.append(row[0])
            self.productCategory.addItems(categoryList)

            # Populate search bar completer
            cursor.execute("SELECT name FROM stock")
            for row in cursor:
                items.append(row[0])
            completer = QCompleter(items)
            self.searchbar.setCompleter(completer)
        except Exception as e:
            print(f"Error initializing combo boxes: {e}")
            QMessageBox.critical(self, "Error", f"Failed to initialize combo boxes: {e}")
        finally:
            conn.close()

    def goHome(self):
        self.cw = mw.MainWindow()
        self.cw.show()
        self.close()

    def goToCategory(self):
        self.cw = ncw.NewCategoryWindow()
        self.cw.show()

    def goToType(self):
        self.cw = ntw.NewTypeWindow()
        self.cw.show()

    def goToEditItem(self):
        self.cw = eiw.EditItemWindow()
        self.cw.show()

    def goToDefectiveItem(self):
        self.cw = diw.DefectiveItemsWindow()
        self.cw.show()

    def goToAddNewItem(self):
        self.cw = aniw.AddNewItemWindow()
        self.cw.show()

    def goToUpdateQuantity(self):
        self.cw = uqw.UpdateQuantityWindow()
        self.cw.show()

    def initTable(self):
        conn = dbc.getConnection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, name, type, category, unit, wholesale_price, retail_price, quantity FROM stock")
            rows = cursor.fetchall()

            self.stockTable.setRowCount(len(rows))
            self.stockTable.setColumnCount(8)

            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    self.stockTable.setItem(i, j, QTableWidgetItem(str(value)))

            conn.close()
        except Exception as e:
            print(f"Error updating table: {e}")
            QMessageBox.critical(self, "Database Error", f"Failed to update table: {e}")
        finally:
            if conn:
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
                SELECT id, name, type, category, unit, wholesale_price, retail_price, quantity
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
            self.stockTable.setColumnCount(8)
            self.stockTable.setRowCount(len(results))
            for i, row in enumerate(results):
                self.stockTable.setItem(i, 0, QTableWidgetItem(str(row[0])))
                self.stockTable.setItem(i, 1, QTableWidgetItem(row[1]))
                self.stockTable.setItem(i, 2, QTableWidgetItem(row[2]))
                self.stockTable.setItem(i, 3, QTableWidgetItem(row[3]))
                self.stockTable.setItem(i, 4, QTableWidgetItem(str(row[4])))
                self.stockTable.setItem(i, 5, QTableWidgetItem(str(row[5])))
                self.stockTable.setItem(i, 6, QTableWidgetItem(str(row[6])))
                self.stockTable.setItem(i, 7, QTableWidgetItem(str(row[7])))
            conn.close()
        except Exception as e:
            print(e)