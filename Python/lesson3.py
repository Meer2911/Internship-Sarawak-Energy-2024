#Version 1
"""
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

import sys
app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Our First MainWindow App!")

button = QPushButton()
button.setText("Press Me")

window.setCentralWidget(button)

window.show()
app.exec()

"""

#Version 2
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

class mainWindow(QMainWindow) :

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Button Holder App")
        self.button = QPushButton("Press Me!")
        self.button.clicked.connect(self.buttonClicked)
        self.setCentralWidget(self.button)
    
    #Button Function Method
    def buttonClicked(self):
        self.button.setText("I Have Been Pressed")
        
        

app = QApplication(sys.argv)
window = mainWindow()
window.show()
app.exec()

#Version 3 would be when you do it in a file