from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QPixmap

class MessageBox(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(700,200)
        self.setWindowTitle("Error Message")
        self.setText("Incorrect File Format")
        self.setInformativeText("Please input the correct file format(.xlsx/.vsdx)")
        self.setIconPixmap(QPixmap("Lesson7.MessageBox\ErrorMessage.png"))
        self.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.setDefaultButton(QMessageBox.Ok)