from PySide6.QtWidgets import QMenuBar
from PySide6.QtGui import QAction
from displayData import MergeDisplayData, ViewDisplayData

class MenuBar(QMenuBar):
    def __init__(self, mainMenu):
        super().__init__(mainMenu)

        self.mainMenu = mainMenu

        fileMenu = self.addMenu("File")

        self.export = QAction("Export")
        self.export.triggered.connect(self.exportActionTriggered)
        self.export.setStatusTip("Exports the file you are viewing right now")

        fileMenu.addAction(self.export)

        actionMenu = self.addMenu("Action")

        self.mergeFiles = QAction("Merge Files")
        self.mergeFiles.triggered.connect(self.mergeFilesActionTriggered)
        self.mergeFiles.setStatusTip("Merges several excel files to view")

        self.viewInconsistencies = QAction("View Inconsistencies")
        self.viewInconsistencies.triggered.connect(self.viewInconsistenciesActionTriggered)
        self.viewInconsistencies.setStatusTip("View inconsistencies between an excel file and a visio file")

        actionMenu.addAction(self.mergeFiles)
        actionMenu.addAction(self.viewInconsistencies)


    def exportActionTriggered(self):
        print("Exporting files...")
        self.mainMenu.statusBar.showMessage("Exporting files...")

    def mergeFilesActionTriggered(self):
        print("Merging Files...")
        self.mainMenu.statusBar.showMessage("Merging Files...")
        self.mainMenu.setCentralWidget(MergeDisplayData(self.mainMenu))

    def viewInconsistenciesActionTriggered(self):
        print("Changing windows...")
        self.mainMenu.statusBar.showMessage("Changing windows...")
        self.mainMenu.setCentralWidget(ViewDisplayData(self.mainMenu))
