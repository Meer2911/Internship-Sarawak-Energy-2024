from PySide6.QtWidgets import QWidget, QPushButton, QMenuBar, QStatusBar
from PySide6.QtGui import QAction

class MenuBar(QMenuBar):
    def __init__(self, mainMenu):
        super().__init__("MenuBar", mainMenu)
        self.mainMenu = mainMenu
        
        fileMenu = self.addMenu("&File")

        fileMenu.addAction("Export")

        editMenu = self.addMenu("&Edit")

        copy = QAction("&Copy", self)
        copy.triggered.connect(self.copyActionPressed)
        
        editMenu.addAction(copy)

        self.addMenu("&Window")
        self.addMenu("&Setting")
        self.addMenu("&Help")

    def copyActionPressed(self):
        print("Copy was pressed")

