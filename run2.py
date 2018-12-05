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
        self.isTest = False
        self.isReal = False
        self.history = []
        self.cursorPos = self.getCurCursorPos()
        self.cursorColor = self.getCurCursorColor()
        self.curWindowSizeX = GetSystemMetrics(0)
        self.curWindowSizeY = GetSystemMetrics(1)
        self.consoleMessage = None
        self.setupUi(self)

        # check for current window size
        # print("Width =", GetSystemMetrics(0))
        # print("Height =", GetSystemMetrics(1))
        self.windowX.setText( str(GetSystemMetrics(0)) )
        self.windowY.setText( str(GetSystemMetrics(1)) )

        self.startBtn.clicked.connect(self.startBtnClicked)
        self.endBtn.clicked.connect(self.endBtnClicked)
        self.stopBtn.clicked.connect(self.stopBtnClicked)
        self.testBtn.clicked.connect(self.testBtnClicked)

    def getCurCursorPos(self) :
        self.cursorPos = win32api.GetCursorPos()
        return self.cursorPos

    def getCurCursorColor(self) :
        mouse_p = win32api.GetCursorPos()
        i_desktop_window_id = win32gui.GetDesktopWindow()
        i_desktop_window_dc = win32gui.GetWindowDC(i_desktop_window_id)
        color = win32gui.GetPixel(i_desktop_window_dc, mouse_p[0] , mouse_p[1])
        rgb = (color & 0xff), ((color >> 8) & 0xff), ((color >> 16) & 0xff)
        self.cursorColor = rgb
        return rgb

    def getColor(self, xPos, yPos) :
        i_desktop_window_id = win32gui.GetDesktopWindow()
        i_desktop_window_dc = win32gui.GetWindowDC(i_desktop_window_id)
        color = win32gui.GetPixel(i_desktop_window_dc, int(xPos) , int(yPos))
        rgb = (color & 0xff), ((color >> 8) & 0xff), ((color >> 16) & 0xff)
        self.cursorColor = rgb
        return rgb

    def mouseRightClick(xPos, yPos) :
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,xPos,yPos,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,xPos,yPos,0,0)
        return

    def mouseLeftClick(xPos, yPos) :
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,xPos,yPos,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,xPos,yPos,0,0)
        return

    def updateStatus(self) :
        self.mouseXPos.setText(str(self.cursorPos[0]))
        self.mouseYPos.setText(str(self.cursorPos[1]))
        self.consoleText.setText(self.consoleMessage)
        # self.cursorColorCode.setText(str(self.cursorColor))
        self.cursorColorCode.setStyleSheet("color:" + str(self.cursorColor))
        self.cursorColorBox.setStyleSheet("background-color:" + "rgb" + str(self.cursorColor))
        return

    def startBtnClicked(self) :
        if self.isReal:
            print('already started')
            return
        self.isReal = True
        print('testing!')

        colorDetector = threading.Thread( target=self.detectColorChange )
        colorDetector.start()


    def detectColorChange(self) :
        xPos = int(self.curWindowSizeX / 2);
        yPos = int(self.curWindowSizeY*2  / 3);
        win32api.SetCursorPos((xPos,yPos))
        while self.isReal :
            color = self.getColor(xPos, yPos)
            print(color)
            # self.consoleMessage = str(color)
            # self.updateStatus()
            sleep(0.1)
        return

    def testBtnClicked(self):
        if self.isTest:
            print('already started..')
            return
        self.isTest = True
        self.consoleText.setText('작동중...')

        cursorTracker = threading.Thread( target=self.trackCursorPos )
        cursorTracker.start()

        colorTracker = threading.Thread( target=self.trackCursorCol )
        colorTracker.start()

    def endBtnClicked(self):
        self.isTest = False
        self.isReal = False
        sys.exit()
        QCoreApplication.quit()

    def stopBtnClicked(self) :
        print('중지')
        self.isTest = False
        self.isReal = False
        self.console.setText('중지됨')

    def trackCursorCol(self) :
        while self.isTest:
            color = self.getCurCursorColor()
            sleep(0.05)
            self.updateStatus()
            sleep(0.05)
        return

    def trackCursorPos(self):
        while self.isTest:
            # get mouse cursor position
            mouse_p = self.getCurCursorPos()
            sleep(0.05)
            self.updateStatus()
            sleep(0.05)
        return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
