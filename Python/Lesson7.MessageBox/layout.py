from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QApplication
import sys

class Layout1(QWidget):
    def __init__(self):
        super().__init__()

        label = QLabel("Staff ID: ")
        self.lineEdit = QLineEdit("Insert ID Here")
        self.lineEdit.editingFinished.connect(self.lineEditAction)

        self.staffID = QLabel("")

        idInput = QHBoxLayout()
        idInput.addWidget(label)
        idInput.addWidget(self.lineEdit)

        layOutVBox = QVBoxLayout()
        layOutVBox.addLayout(idInput)
        layOutVBox.addWidget(self.staffID)

        self.setLayout(layOutVBox)

    def lineEditAction(self):
        self.staffID.setText(self.lineEdit.text())
