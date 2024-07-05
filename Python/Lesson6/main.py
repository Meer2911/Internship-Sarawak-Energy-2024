from PySide6.QtWidgets import QApplication, QMainWindow, QStatusBar
from menuBar import MenuBar
from toolBar import ToolBar
from button1 import Button1
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        menu_bar = MenuBar()
        self.setMenuBar(menu_bar)

        self.toolBar = ToolBar(self)
        self.addToolBar(self.toolBar)
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        self.button1 = Button1(self)
        self.setCentralWidget(self.button1)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

