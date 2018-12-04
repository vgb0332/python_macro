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

from getRGBColor import rgbint2rgbtuple
form_class = uic.loadUiType("main_ui.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.isOn = False
        self.history = [];
        self.cursorPos = None
        self.cursorColor = None
        self.curWindowSizeX = GetSystemMetrics(0)
        self.curWindowSizeY = GetSystemMetrics(1)
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
    def testBtnClicked(self) :
        print('testing!')
        # print(str(self.cursorPos))
        # x, y = self.cursorPos
        # print(str(self.cursorColor))
        # win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
        # win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)
        # win32api.SetCursorPos((500,500))

        done = False
        xPos = 0
        yPos = 0
        print('starting xPos: {}, yPos: {}'.format(xPos, yPos))
        print('windowSize x: {}, y : {}'.format(self.curWindowSizeX, self.curWindowSizeY))
        while xPos < self.curWindowSizeX:
            print(xPos)
            win32api.SetCursorPos((xPos,yPos))
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,xPos,yPos,0,0)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,xPos,yPos,0,0)
            xPos = xPos + 10

            sleep(0.5)

        # while yPos < self.curWindowSizeY:
        #     win32api.SetCursorPos((xPos,yPos))
        #     yPos = yPos + 10
        #     sleep(1)
        print('done')
        return

    def startBtnClicked(self):
        if self.isOn:
            print('already started..')
            return
        self.isOn = True
        self.console.setText('작동중...')

        cursorTracker = threading.Thread( target=self.trackCursorPos )
        cursorTracker.start()

        colorTracker = threading.Thread( target=self.trackCursorCol )
        colorTracker.start()

    def endBtnClicked(self):
        self.isOn = False
        QCoreApplication.quit()

    def stopBtnClicked(self) :
        self.isOn = False
        self.console.setText('중지됨')

    def trackCursorCol(self) :
        while self.isOn:
            mouse_p = win32api.GetCursorPos()
            #get mouse curor color
            color = win32gui.GetPixel(win32gui.GetDC(win32gui.GetActiveWindow()), mouse_p[0] , mouse_p[1])
            rgb = rgbint2rgbtuple(color)
            self.cursorColorCode.setText(str(rgb))
            self.cursorColorCode.setStyleSheet("color:" + str(rgb))
            self.cursorColorBox.setStyleSheet("background-color:" + "rgb" + str(rgb))
            self.cursorColor = rgb
            sleep(0.05)
        return

    def trackCursorPos(self):
        while self.isOn:
            # get mouse cursor position
            mouse_p = win32api.GetCursorPos()
            self.mouseXPos.setText(str(mouse_p[0]))
            self.mouseYPos.setText(str(mouse_p[1]))
            self.cursorPos = mouse_p
            sleep(0.05)
        return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
