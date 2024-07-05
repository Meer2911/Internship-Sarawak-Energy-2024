from PyQt5.QtWidgets import QApplication, QToolButton, QFileDialog, QWidget, QVBoxLayout, QLabel, QStyle

class FileSelector(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("No file selected", self)
        layout.addWidget(self.label)

        self.tool_button = QToolButton(self)
        self.tool_button.setText('Select File')
        self.tool_button.setIcon(self.style().standardIcon(QStyle.SP_DirOpenIcon))
        self.tool_button.clicked.connect(self.showFileDialog)
        layout.addWidget(self.tool_button)

        self.setLayout(layout)
        self.setWindowTitle('File Selector')
        self.show()

    def showFileDialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            self.label.setText(file_name)

if __name__ == '__main__':
    app = QApplication([])
    file_selector = FileSelector()
    app.exec_()
