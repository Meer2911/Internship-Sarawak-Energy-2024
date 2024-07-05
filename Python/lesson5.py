from PySide6.QtWidgets import QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QApplication
import sys
class rockWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RockWidget")

        self.button1 = QPushButton("Button1")
        self.button1.clicked.connect(self.button1Clicked)
        self.button2 = QPushButton("Button2")
        self.button2.clicked.connect(self.button2Clicked)

        # widgetLayout = QHBoxLayout() #Horizontal
        widgetLayout = QVBoxLayout()
        widgetLayout.addWidget(self.button1)
        widgetLayout.addWidget(self.button2)
        self.setLayout(widgetLayout)

    def button1Clicked(self):
        print("Button 1 has been clicked")
        return
    
    def button2Clicked(self):
        print("Button 2 has been clicked")
        return
    
app = QApplication(sys.argv)
widget = rockWidget()
widget.show()

app.exec()