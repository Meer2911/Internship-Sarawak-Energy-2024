from PySide6.QtWidgets import QToolBar
from PySide6.QtGui import QAction,QIcon
from PySide6.QtCore import QSize

class ToolBar(QToolBar):
    def __init__(self, mainMenu):
        super().__init__("Main Toolbar", mainMenu)
        self.mainMenu = mainMenu
        self.setIconSize(QSize(16,16))
        
        viewInconsistency = QAction(QIcon("Lesson6\ViewIcon.png"),"View", self)
        viewInconsistency.setStatusTip("View Inconsistencies Between Files")
        viewInconsistency.triggered.connect(self.view)

        self.addAction(viewInconsistency)


    def view(self):
        print("View Inconsistency Button Has Been Triggered!")
        self.mainMenu.statusBar.showMessage("Viewing Inconsistencies!")
