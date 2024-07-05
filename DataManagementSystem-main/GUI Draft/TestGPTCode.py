from PySide6.QtWidgets import QMessageBox, QPushButton, QMainWindow, QLabel, QApplication
from PySide6.QtGui import QPixmap

class NewWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Window")
        self.setGeometry(100, 100, 300, 200)
        self.label = QLabel("This is the new window", self)
        self.label.move(50, 50)

class MessageBox(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(700, 200)
        self.setWindowTitle("Error Message")
        self.setText("Incorrect File Format")
        self.setInformativeText("Please input the correct file format (.xlsx/.vsdx)")
        self.setIconPixmap(QPixmap("Lesson7.MessageBox/ErrorMessage.png"))
        self.setStandardButtons(QMessageBox.Ok)
        self.setDefaultButton(QMessageBox.Ok)
        
        # Add custom button
        self.customButton = self.addButton("View Errors", QMessageBox.ActionRole)
        self.customButton.clicked.connect(self.open_new_window)
        
        # Initialize the new window
        self.new_window = NewWindow()

    def open_new_window(self):
        self.new_window.show()

if __name__ == "__main__":
    app = QApplication([])
    message_box = MessageBox()
    message_box.exec()
    app.exec()
