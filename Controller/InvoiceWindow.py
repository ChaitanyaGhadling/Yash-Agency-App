from PyQt6 import uic
from PyQt6.QtWidgets import QWidget
import MainWindow as mw

class InvoiceWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("Views/InvoiceWindow.ui", self)
        self.setFixedSize(1900, 980)
        self.homeButton.clicked.connect(self.goHome)

    def goHome(self):
        self.cw = mw.MainWindow()
        self.cw.show()
        self.close()