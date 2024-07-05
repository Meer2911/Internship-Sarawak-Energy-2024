from PySide6.QtWidgets import QToolBar
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QSize
from messageBox import MessageBox

class ToolBar(QToolBar):
    def __init__(self, mainMenu):
        super().__init__("Main Toolbar", mainMenu)
        
        self.mainMenu = mainMenu
        self.errorMessage = MessageBox()

        self.setIconSize(QSize(16,16))

        viewInconsistencies = QAction(QIcon("Lesson7.MessageBox\ViewIcon.png"), "View", self)
        viewInconsistencies.setStatusTip("View Inconsistencies Between Files")
        viewInconsistencies.triggered.connect(self.view)

        self.addAction(viewInconsistencies)


    def view(self):
        print("View Inconsistencies Action Has Been Triggered")
        self.mainMenu.statusBar.showMessage("Processing Inconsistencies")
        self.errorMessage.exec()
