from PySide6.QtWidgets import QMenuBar
from PySide6.QtGui import QAction
class MenuBar(QMenuBar):
    def __init__(self):
        super().__init__()

        #File menu bar
        self.fileMenu = self.addMenu("File")

        export = QAction("&Export", self)
        export.triggered.connect(self.exportActionTriggered)

        save = QAction("&Save", self)
        save.triggered.connect(self.saveActionTriggered)

        self.fileMenu.addAction(export)
        self.fileMenu.addAction(save)
        
        #Edit menu bar
        self.editMenu = self.addMenu("Edit")

        undo = QAction("%Undo", self)
        undo.triggered.connect(self.undoActionTriggered)

        redo = QAction("%Redo", self)
        redo.triggered.connect(self.redoActionTriggered)

        copy = QAction("&Copy", self)
        copy.triggered.connect(self.copyActionTriggered)

        paste = QAction("%Paste", self)
        paste.triggered.connect(self.pasteActionTriggered)

        self.editMenu.addAction(undo)
        self.editMenu.addAction(redo)
        self.editMenu.addAction(copy)
        self.editMenu.addAction(paste)
    
    
    def undoActionTriggered(self):
        print("Undo Action Has Been Triggered")

    def redoActionTriggered(self):
        print("Redo Actino Has Been Triggered")

    def copyActionTriggered(self):
        print("Copy Action Has Been Triggered")

    def pasteActionTriggered(self):
        print("Paste Actino Has Been Triggered")

    def exportActionTriggered(self):
        print("Export Action Has Been Triggered")

    def saveActionTriggered(self):
        print("Save Action Has Been Triggered")