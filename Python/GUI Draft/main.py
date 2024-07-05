from PySide6.QtWidgets import QApplication, QMainWindow, QStatusBar, QWidget, QVBoxLayout
from menuBar import MenuBar
from displayData import MergeDisplayData
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(700, 500)
        self.menuBar = MenuBar(self)
        self.setMenuBar(self.menuBar)
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        self.mergeDisplayData = MergeDisplayData(self)
        self.setCentralWidget(self.mergeDisplayData)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())