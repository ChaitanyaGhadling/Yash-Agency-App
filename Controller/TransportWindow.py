from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QCompleter
import MainWindow as mw
import StockWindow as stw
import DatabaseController as dbc
import NewPurchaseWindow as npw
from PyQt6.QtCore import QDate

class TransportWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("Views/TransportWindow.ui", self)
        self.setFixedSize(1100, 650)
        self.dateEdit.setDate(QDate.currentDate())
