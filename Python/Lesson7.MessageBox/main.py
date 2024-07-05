from PySide6.QtWidgets import QApplication, QMainWindow, QStatusBar
import sys

from menuBar import MenuBar
from toolBar import ToolBar
from layout import Layout1

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        menuBar = MenuBar()
        toolbar = ToolBar(self)
        layout1 = Layout1()

        self.setMenuBar(menuBar)
        self.addToolBar(toolbar)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.setCentralWidget(layout1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
