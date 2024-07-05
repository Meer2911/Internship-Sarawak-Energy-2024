from PySide6.QtWidgets import QGridLayout, QPushButton, QLabel, QHBoxLayout, QLineEdit, QWidget
from PySide6.QtGui import QAction, QIcon, Qt
from displayData import MergeDisplayData
from messageBox import ExcelFileErrorsMessage
from backEnd import ExcelProcessor

class MergeToolBar(QWidget):
    def __init__(self, mainMenu, mergeDisplayData):
        super().__init__()
        self.mainMenu = mainMenu
        self.mergeDisplayData = mergeDisplayData
        self.excelProcessor = ExcelProcessor()

        toolBar = QGridLayout()

        # Creating the select file button
        selectFileButton = QPushButton("Select Files")
        selectFileButton.setIcon(QIcon("GUI Draft/Images/ToolBarIcons/AddFileIcon.png"))
        selectFileButton.setStatusTip("Select Files to View")
        selectFileButton.clicked.connect(self.selectFileButtonClicked)

        selectFileLabel = QLabel("Select Files")

        # Add the button and the label to a HBox and put the spacing really small
        selectFileHBox = QHBoxLayout()
        selectFileHBox.addWidget(selectFileButton)
        selectFileHBox.addWidget(selectFileLabel)
        selectFileHBox.setSpacing(3)

        sortButton = QPushButton("Sort")
        sortButton.setIcon(QIcon("GUI Draft/Images/ToolBarIcons/SortIcon.png"))
        sortButton.setStatusTip("Sort Data either Ascending or Descending")
        sortButton.clicked.connect(self.sortButtonClicked)

        sortLabel = QLabel("Sort")

        # Add the button and the label to a HBox and put the spacing really small
        sortHBox = QHBoxLayout()
        sortHBox.addWidget(sortButton)
        sortHBox.addWidget(sortLabel)
        sortHBox.setSpacing(3)

        filterButton = QPushButton("Filter")
        filterButton.setIcon(QIcon("GUI Draft/Images/ToolBarIcons/FilterIcon.png"))
        filterButton.setStatusTip("Apply Filters to the Data")
        filterButton.clicked.connect(self.filterButtonClicked)

        filterLabel = QLabel("Filter")

        filterHBox = QHBoxLayout()
        filterHBox.addWidget(filterButton)
        filterHBox.addWidget(filterLabel)
        filterHBox.setSpacing(3)

        searchButton = QPushButton("Search")
        searchButton.setIcon(QIcon("GUI Draft/Images/ToolBarIcons/SearchIcon.png"))
        searchButton.setStatusTip("Search for Specific Data")
        searchButton.clicked.connect(self.searchButtonClicked)

        searchLineEdit = QLineEdit("Search")

        searchHBox = QHBoxLayout()
        searchHBox.addWidget(searchButton)
        searchHBox.addWidget(searchLineEdit)
        searchHBox.setSpacing(3)

        toolBar.addWidget(selectFileHBox.itemAt(0).widget(), 0, 0, 1, 1)  # Span 1 row and 4 columns
        toolBar.setColumnStretch(1, 1)  # Stretch column 1 to take up empty space
        toolBar.setColumnStretch(2, 1)  # Stretch column 2 to take up empty space
        toolBar.setColumnStretch(3, 1)  # Stretch column 3 to take up empty space

        toolBar.addWidget(sortHBox.itemAt(0).widget(), 0, 4, 1, 1)       # Place in the next available column (column 4)
        toolBar.addWidget(filterHBox.itemAt(0).widget(), 0, 5, 1, 1)     # Place in the next available column (column 5)
        toolBar.addWidget(searchHBox.itemAt(0).widget(), 0, 6, 1, 1)     # Place in the next available column (column 6)
        self.setLayout(toolBar)
 
    def selectFileButtonClicked(self):
        print("Opening folder...")
        self.mainMenu.statusBar.showMessage("Opening folder...")
        excelFilePath = self.excelProcessor.openExcelFile()
        df = self.excelProcessor.createDataframe(excelFilePath)
        self.mergeDisplayData.populateTable(df.values.tolist())
        errorMessage = ExcelFileErrorsMessage(self.excelProcessor.wong)
        errorMessage.exec()

    def sortButtonClicked(self):
        print("Sorting data...")
        self.mainMenu.statusBar.showMessage("Sorting data...")

    def filterButtonClicked(self):
        print("Filtering data...")
        self.mainMenu.statusBar.showMessage("Filtering data...")

    def searchButtonClicked(self):
        print("Searching for item...")
        self.mainMenu.statusBar.showMessage("Searching for item...")
