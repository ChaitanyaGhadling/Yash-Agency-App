from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QCompleter
import MainWindow as mw
import StockWindow as stw
import DatabaseController as dbc
from PyQt6.QtCore import QDate

class SetReminderWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("Views/SetReminderWindow.ui", self)
        self.setFixedSize(950, 500)
        self.dateEdit.setDate(QDate.currentDate())