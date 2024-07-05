from PySide6.QtWidgets import QApplication, QMainWindow
import sys
from rockWidget import RockWidget 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setCentralWidget(RockWidget())
        self.setWindowTitle("Main Window Example")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
