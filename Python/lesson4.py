####Version 1####


# from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
# import sys
# def buttonClicked(data):
#     #If its true, a "/" will appear, similar to a checkbox
#     if(data):
#         button.setText("/")
#     else:
#         button.setText("")
#     print("You clicked the button, didn't you!\nCheck status:", data)

# app = QApplication()
# button = QPushButton("")
# #Setting the button as checkable to allow it to act like a checkbox
# button.setCheckable(True)
# button.clicked.connect(buttonClicked)

# button.show()
# app.exec()

####Version 2####
#Capture Value From a Slider

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QSlider

def respondToSlider(data):
    print("Slider moved to: ", data)

app = QApplication()
slider = QSlider(Qt.Horizontal)
slider.setMinimum(1)
slider.setMaximum(50)
slider.setValue(25)

slider.valueChanged.connect(respondToSlider)
slider.show()
app.exec()