import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import win32api, win32con, win32gui
from win32api import GetSystemMetrics


from time import sleep
import threading
import multiprocessing

from getRGBColor import rgbint2rgbtuple
form_class = uic.loadUiType("main_ui.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.curWindowSizeX = GetSystemMetrics(0)
        self.curWindowSizeY = GetSystemMetrics(1)
        self.consoleMessage = None
        self.setupUi(self)
        print('hi')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
