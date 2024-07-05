from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget

class RockWidget(QWidget):
    def __init__(self):
        super().__init__()  # Corrected superclass initialization
        self.button1 = QPushButton("Button 1")
        self.button1.clicked.connect(self.button1Clicked)
        self.button2 = QPushButton("Button 2")
        self.button2.clicked.connect(self.button2Clicked)

        rockWidgetLayout = QVBoxLayout()
        rockWidgetLayout.addWidget(self.button1)
        rockWidgetLayout.addWidget(self.button2)

        self.setLayout(rockWidgetLayout)
    
    def button1Clicked(self):
        print("Button 1 has been clicked")

    def button2Clicked(self):
        print("Button 2 has been clicked") 
