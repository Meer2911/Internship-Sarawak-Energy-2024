from PySide6.QtWidgets import QPushButton

class Button1(QPushButton):
    def __init__(self, mainMenu):
        super().__init__("button1", mainMenu)
        self.mainMenu = mainMenu
        self.setText("Press Me!")
        self.clicked.connect(self.buttonClicked)
    
    def buttonClicked(self):
        print("Button 1 Has Been Clicked")
        self.mainMenu.statusBar.showMessage("Proccessing Button Click")
