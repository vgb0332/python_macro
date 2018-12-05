import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import win32api, win32con, win32gui
from win32api import GetSystemMetrics
from getRGBColor import rgbint2rgbtuple

class CursorThread(QThread):
    # 사용자 정의 시그널 선언
    mouseXPos = pyqtSignal(str)
    mouseYPos = pyqtSignal(str)
    mouseColorCode = pyqtSignal(str)
    mouseColorBox = pyqtSignal(str)
    message = pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self)
        self.cond = QWaitCondition()
        self.mutex = QMutex()
        self._status = False

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            self.mutex.lock()
            if not self._status:
                self.cond.wait(self.mutex)

            xPos, yPos = win32api.GetCursorPos()
            self.mouseXPos.emit(str(xPos))
            self.mouseYPos.emit(str(yPos))

            i_desktop_window_id = win32gui.GetDesktopWindow()
            i_desktop_window_dc = win32gui.GetWindowDC(i_desktop_window_id)
            color = win32gui.GetPixel(i_desktop_window_dc, xPos , yPos)
            rgb = (color & 0xff), ((color >> 8) & 0xff), ((color >> 16) & 0xff)
            self.mouseColorCode.emit(str(rgb))
            self.mouseColorBox.emit("background-color:"+"rgb"+str(rgb))
            self.message.emit('inital color' + str(rgb))
            self.msleep(500)  # ※주의 QThread에서 제공하는 sleep을 사용

            self.mutex.unlock()

    def toggle_status(self):
        self._status = not self._status
        if self._status:
            self.message.emit('테스트 시작')
            self.cond.wakeAll()
        else :
            self.message.emit('테스트 중지')


    @property
    def status(self):
        return self._status
