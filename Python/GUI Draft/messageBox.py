from PySide6.QtWidgets import QMessageBox, QMainWindow
from PySide6.QtGui import QPixmap

class ExcelFileErrorsMessage(QMessageBox):
    def __init__(self, numberOfErrors):
        super().__init__()
        self.setMinimumSize(700, 200)
        self.setWindowTitle("Error Message")
        self.setText("File Errors")
        self.setInformativeText(f"There are {numberOfErrors} errors in this file.")
        self.setIcon(QMessageBox.Critical)  # Use default error icon
        self.setStandardButtons(QMessageBox.Ok)
        self.setDefaultButton(QMessageBox.Ok)
        
        # Add custom button
        self.customButton = self.addButton("View Errors", QMessageBox.ActionRole)
        self.customButton.clicked.connect(self.open_new_window)
        
        # Initialize the new window
        self.new_window = QMainWindow()

    def open_new_window(self):
        self.new_window.setWindowTitle("Error Details")
        self.new_window.setGeometry(100, 100, 400, 300)  # Set size and position
        self.new_window.show()

# Example usage
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication([])
    message_box = ExcelFileErrorsMessage(5)
    message_box.exec()
    app.exec()
