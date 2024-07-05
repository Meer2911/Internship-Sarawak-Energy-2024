import sys
import pandas as pd
from PySide6.QtWidgets import QApplication, QFileDialog, QWidget

class DataHandler(QWidget):
    def __init__(self):
        super().__init__()
        self.listOfExcelFile = []
        self.listofOriginalDataFrames = []
        self.listOfDisplayedDataFrames = []

    # Open Excel file and read the data into a DataFrame
    def openExcelFile(self):
        excel_file_path = QFileDialog.getOpenFileName(self, "Select Excel File", "", "Excel files (*.xlsx)")[0]
        if excel_file_path:
            self.listOfExcelFile.append(excel_file_path)
            df = self.createDataframe(excel_file_path)

            df.columns = df.columns.str.strip()
            self.listofOriginalDataFrames.append(df)
            self.listOfDisplayedDataFrames.append(df)

            return excel_file_path
        else:
            print("No excel file selected.")

    # Open Visio file and return file path
    def openVisioFile(self):
        visio_file_path = QFileDialog.getOpenFileName(self, "Select Visio File", "", "Visio files (*.vsdx)")[0]
        if visio_file_path:
            return visio_file_path
        else:
            print("No visio file selected.")
            return None

    def createDataframe(self, excel_file_path):
        # Example function to create a dataframe from an excel file
        return pd.read_excel(excel_file_path)

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    handler = DataHandler()
    handler.show()
    sys.exit(app.exec())
