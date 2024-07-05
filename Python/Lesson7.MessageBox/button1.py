from PySide6.QtWidgets import QPushButton, QMessageBox

class Button1(QPushButton):
    def __init__(self, mainMenu):
        super().__init__("Button1", mainMenu)

        self.mainMenu = mainMenu
        self.setText("Button 1")
        self.clicked.connect(self.button1Clicked)

    def button1Clicked(self):
        print("Button 1 Has Been Clicked")

        ret = QMessageBox.information(self, "Informatino", "Button 1 has been clicked", QMessageBox.Ok | QMessageBox.Cancel)

        if ret == QMessageBox.Ok:
            print("User Chooses Ok")
        else: 
            print("User Chooses Cancel")
