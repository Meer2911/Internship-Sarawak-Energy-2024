from PySide6.QtWidgets import (
    QTableWidget, QTableWidgetItem, QWidget, QPushButton, QVBoxLayout, QSpacerItem,
    QSizePolicy, QGridLayout, QHBoxLayout, QLabel, QLineEdit
)
from PySide6.QtGui import Qt, QIcon
from backEnd import ExcelProcessor
from messageBox import ExcelFileErrorsMessage

class MergeDisplayData(QWidget):
    def __init__(self, mainMenu):
        super().__init__()
        # Initialization
        self.excelProcessor = ExcelProcessor(self)
        self.tableWidget = QTableWidget()
        self.mainMenu = mainMenu
        
        # Creating the tool bar
        self.toolBar = QGridLayout()

        # Creating the select file button
        selectFileButton = QPushButton("Select Files")
        selectFileButton.setIcon(QIcon("GUI Draft/Images/ToolBarIcons/AddFileIcon.png"))
        selectFileButton.setStatusTip("Select Files to View")
        selectFileButton.clicked.connect(self.selectFileButtonClicked)

        sortButton = QPushButton("Sort")
        sortButton.setIcon(QIcon("GUI Draft/Images/ToolBarIcons/SortIcon.png"))
        sortButton.setStatusTip("Sort Data either Ascending or Descending")
        sortButton.clicked.connect(self.sortButtonClicked)

        # Add the filter button
        filterButton = QPushButton("Filter")
        filterButton.setIcon(QIcon("GUI Draft/Images/ToolBarIcons/FilterIcon.png"))
        filterButton.setStatusTip("Apply Filters to the Data")
        filterButton.clicked.connect(self.filterButtonClicked)

        # Add the search button
        searchButton = QPushButton("")
        searchButton.setIcon(QIcon("GUI Draft/Images/ToolBarIcons/SearchIcon.png"))
        searchButton.setStatusTip("Search for Specific Data")
        searchButton.clicked.connect(self.searchButtonClicked)

        searchLineEdit = QLineEdit("Search")
    
        searchHBox = QHBoxLayout()
        searchHBox.addWidget(searchButton)
        searchHBox.addWidget(searchLineEdit)
        searchHBox.setSpacing(3)

        # Setting up the spacing in the toolbar
        self.toolBar.addWidget(selectFileButton, 0, 0, 1, 1)
        self.toolBar.setColumnStretch(1, 1)  # Stretch column 1 to take up empty space
        self.toolBar.setColumnStretch(2, 1)  # Stretch column 2 to take up empty space
        self.toolBar.setColumnStretch(3, 1)  # Stretch column 3 to take up empty space

        self.toolBar.addWidget(sortButton, 0, 4, 1, 1)
        self.toolBar.addWidget(filterButton, 0, 5, 1, 1)
        self.toolBar.addLayout(searchHBox, 0, 6, 1, 1)

        # Declaring the clear table button
        self.clearTableButton = QPushButton("Clear Table")
        self.clearTableButton.clicked.connect(self.clearTableButtonClicked)

        # Declaring the enter files button
        enterFilesButton = QPushButton("Enter Files")
        enterFilesButton.clicked.connect(self.enterFilesButtonClicked)

        # Creates a container for the borders
        self.containerWidget = QWidget()
        self.containerWidget.setStyleSheet("border: 1px solid lightgray;")  # Add a border to the container widget

        # The actual main display of the table
        self.mainDisplay = QVBoxLayout(self.containerWidget)
        self.spacer_top = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.mainDisplay.addItem(self.spacer_top)

        # Add the button to the layout
        self.mainDisplay.addWidget(enterFilesButton, alignment=Qt.AlignCenter)

        # Add a spacer item after the button to push it up
        self.spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.mainDisplay.addItem(self.spacer_bottom)
        
        # Setting up the layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.containerWidget)

        self.mergeLayout = QVBoxLayout()
        self.mergeLayout.addLayout(self.toolBar)
        self.mergeLayout.addLayout(self.mainLayout)
        self.mergeLayout.setStretch(0,1)
        self.mergeLayout.setStretch(0,10)
        
        self.setLayout(self.mergeLayout)
    
    def populateTable(self, data):
        # Clears the tableWidget first
        self.tableWidget.clear()

        # Set the number of rows and columns
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(data[0]))  # Assuming all rows have the same number of columns

        # Populate the table with data
        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.tableWidget.setItem(row_idx, col_idx, item)
    
    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    # Define the enter files button function
    def enterFilesButtonClicked(self):
        print("Enter Files button clicked.")
        try:
            self.clearLayout(self.mainDisplay)
            print("Layout cleared.")
            self.mainDisplay.addWidget(self.tableWidget)
            print("Table widget added to main display.")
            self.mainLayout.addWidget(self.clearTableButton)
            print("Clear table button added to main layout.")
            self.selectFileButtonClicked()
            print("File selection button clicked.")
        except Exception as e:
            print(f"Error occurred in enterFilesButtonClicked: {e}")
            self.selectFileButtonClicked()
     
    # Define the clear table button
    def clearTableButtonClicked(self):
        self.clearLayout(self.mainDisplay)

    # *************************************
    # Tool bar Functions
    # *************************************

    # Define the select file button function
    def selectFileButtonClicked(self):
        print("Opening folder...")
        if hasattr(self.mainMenu, 'statusBar'):
            self.mainMenu.statusBar.showMessage("Opening folder...")
        try:
            excelFilePath = self.excelProcessor.openExcelFile()
            df = self.excelProcessor.createDataframe(excelFilePath)
            self.populateTable(df.values.tolist())
            errorMessage = ExcelFileErrorsMessage(self.excelProcessor.wong)
            errorMessage.exec()
            print("Excel file processed successfully.")
        except Exception as e:
            print(f"Error occurred in selectFileButtonClicked: {e}")


    # Define the sort button function
    def sortButtonClicked(self):
        print("Sorting data...")
        if hasattr(self.mainMenu, 'statusBar'):
            self.mainMenu.statusBar.showMessage("Sorting data...")

    # Define the filter button function
    def filterButtonClicked(self):
        print("Filtering data...")
        if hasattr(self.mainMenu, 'statusBar'):
            self.mainMenu.statusBar.showMessage("Filtering data...")

    # Define the search button function
    def searchButtonClicked(self):
        print("Searching for item...")
        if hasattr(self.mainMenu, 'statusBar'):
            self.mainMenu.statusBar.showMessage("Searching for item...")

    # *************************************
    # Tool bar Functions
    # *************************************

class ViewDisplayData(QWidget):
    def __init__(self, mainMenu):
        super().__init__()
        # Initialization
        self.excelProcessor = ExcelProcessor()
        self.tableWidget = QTableWidget()
        self.mainMenu = mainMenu
        
        # Creating the tool bar
        self.toolBar = QHBoxLayout()

        # Add the sort button
        sortButton = QPushButton("Sort")
        sortButton.setIcon(QIcon("GUI Draft/Images/ToolBarIcons/SortIcon.png"))
        sortButton.setStatusTip("Sort Data either Ascending or Descending")
        sortButton.clicked.connect(self.sortButtonClicked)

        # Add the filter button
        filterButton = QPushButton("Filter")
        filterButton.setIcon(QIcon("GUI Draft/Images/ToolBarIcons/FilterIcon.png"))
        filterButton.setStatusTip("Apply Filters to the Data")
        filterButton.clicked.connect(self.filterButtonClicked)

        # Add the search button
        searchButton = QPushButton("")
        searchButton.setIcon(QIcon("GUI Draft/Images/ToolBarIcons/SearchIcon.png"))
        searchButton.setStatusTip("Search for Specific Data")
        searchButton.clicked.connect(self.searchButtonClicked)

        searchLineEdit = QLineEdit("Search")
    
        searchHBox = QHBoxLayout()
        searchHBox.addWidget(searchButton)
        searchHBox.addWidget(searchLineEdit)
        searchHBox.setSpacing(3)

        searchWidget = QWidget()
        searchWidget.setLayout(searchHBox)

        self.spacerLeft = QSpacerItem(380, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.toolBar.addItem(self.spacerLeft)
        self.toolBar.addWidget(sortButton)
        self.toolBar.addWidget(filterButton)
        self.toolBar.addWidget(searchWidget)

        # Declaring the two files VBoxLayout
        self.inconsistenciesVBox = QVBoxLayout()

        # Declaring the excel section
        excelLabel = QLabel("Excel")
        # Declare the excel icons
        self.excelAddFileButton = QPushButton("Select Excel File")
        self.excelAddFileButton.clicked.connect(self.excelAddFileButtonClicked)
        
        self.excelClearTableButton = QPushButton("Clear")
        self.excelClearTableButton.clicked.connect(self.clearExcelTableButton)

        # Declare the spacer
        self.excelSpacerRight = QSpacerItem(500, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # Declare the Excel HBox
        excelHBox = QHBoxLayout()
        excelHBox.addWidget(self.excelAddFileButton)
        excelHBox.addWidget(self.excelClearTableButton)
        excelHBox.addItem(self.excelSpacerRight)


        self.excelTable = QTableWidget()

        # Declaring the visio  section
        visioLabel = QLabel("Visio")
        # Declare the visio icons
        self.visioAddFileButton = QPushButton("Select Visio File")
        self.visioAddFileButton.clicked.connect(self.visioAddFileButtonClicked)

        self.visioClearTableButton = QPushButton("Clear")
        self.visioClearTableButton.clicked.connect(self.clearVisioTableButton)

        # Declare the spacer
        self.visioSpacerRight = QSpacerItem(500, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # Declare the visio HBox
        visioHBox = QHBoxLayout()
        visioHBox.addWidget(self.visioAddFileButton)
        visioHBox.addWidget(self.visioClearTableButton)
        visioHBox.addItem(self.visioSpacerRight)

        self.visioTable = QTableWidget()

        # Creates a container for the borders
        self.containerWidget = QWidget()
        self.containerWidget.setStyleSheet("border: 1px solid lightgray;")  # Add a border to the container widget

        # The actual main display of the table
        self.mainDisplay = QVBoxLayout()

        # Adding the excel widgets to the main display
        self.mainDisplay.addWidget(excelLabel)
        self.mainDisplay.addLayout(excelHBox)
        self.mainDisplay.addWidget(self.excelTable)

        # Adding the visio widgets to the main display
        self.mainDisplay.addWidget(visioLabel)
        self.mainDisplay.addLayout(visioHBox)
        self.mainDisplay.addWidget(self.visioTable)
        
        # Setting up the layout
        self.viewLayout = QVBoxLayout()
        self.viewLayout.addLayout(self.toolBar, stretch=1)
        self.viewLayout.addLayout(self.mainDisplay, stretch=30)
        
        self.setLayout(self.viewLayout)
    
    def populateExcelTable(self, data):
        # Clears the tableWidget first
        self.excelTable.clear()

        # Set the number of rows and columns
        self.excelTable.setRowCount(len(data))
        self.excelTable.setColumnCount(len(data[0]))  # Assuming all rows have the same number of columns

        # Populate the table with data
        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.excelTable.setItem(row_idx, col_idx, item)

    def populateVisioTable(self, data):
        print("Populate visio table button has been clicked")
    
    # Clears the excel table
    def clearExcelTableButton(self):
        self.excelTable.clear()

    # Clears the visio table
    def clearVisioTableButton(self):
        self.visioTable.clear()
    
    # Allows the user to select their file
    def excelAddFileButtonClicked(self):
        print("Opening folder...")
        self.mainMenu.statusBar.showMessage("Opening folder...")
        excelFilePath = self.excelProcessor.openExcelFile()
        df = self.excelProcessor.createDataframe(excelFilePath)
        self.populateExcelTable(df.values.tolist())

    def visioAddFileButtonClicked(self):
        # Incomple for now, waiting for backend
        print("Opening folder...")
        self.mainMenu.statusBar.showMessage("Opening folder...")
        visioFilePath = self.excelProcessor.openVisioFile()
        df = self.excelProcessor.createDataframe(visioFilePath)
        self.populateVisioTable(df.values.tolist())

    # *************************************
    # Tool bar Functions
    # *************************************

    # Define the sort button function
    def sortButtonClicked(self):
        print("Sorting data...")
        if hasattr(self.mainMenu, 'statusBar'):
            self.mainMenu.statusBar.showMessage("Sorting data...")

    # Define the filter button function
    def filterButtonClicked(self):
        print("Filtering data...")
        if hasattr(self.mainMenu, 'statusBar'):
            self.mainMenu.statusBar.showMessage("Filtering data...")

    # Define the search button function
    def searchButtonClicked(self):
        print("Searching for item...")
        if hasattr(self.mainMenu, 'statusBar'):
            self.mainMenu.statusBar.showMessage("Searching for item...")


    # *************************************
    # Tool bar Functions
    # *************************************
