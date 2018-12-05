import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import win32api, win32con, win32gui
from win32api import GetSystemMetrics
from getRGBColor import rgbint2rgbtuple
from VK_CODE import VK_CODE

class FishingThread(QThread):
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
        self.color = None

    def __del__(self):
        self.wait()

    def run(self):
        xPos = int(GetSystemMetrics(0) / 2);
        yPos = int(GetSystemMetrics(1)*2  / 3);
        self.mouseXPos.emit(str(xPos))
        self.mouseYPos.emit(str(yPos))
        win32api.SetCursorPos((xPos,yPos))

        while True:
            self.mutex.lock()
            if not self._status:
                self.cond.wait(self.mutex)

            i_desktop_window_id = win32gui.GetDesktopWindow()
            i_desktop_window_dc = win32gui.GetWindowDC(i_desktop_window_id)
            color = win32gui.GetPixel(i_desktop_window_dc, xPos , yPos)
            rgb = (color & 0xff), ((color >> 8) & 0xff), ((color >> 16) & 0xff)
            self.mouseColorCode.emit(str(rgb))
            self.mouseColorBox.emit("background-color:"+"rgb"+str(rgb))

            print(rgb, self.color, rgb == self.color)
            if not rgb == self.color and self.color:
                print('?')
                self.press('g','r','e','a','t')
                self.msleep(5000)
                self.press('e')
                self.off()

            self.color = rgb
            self.msleep(100)  # ※주의 QThread에서 제공하는 sleep을 사용

            self.mutex.unlock()

    def press(self, *args):
        '''
        one press, one release.
        accepts as many arguments as you want. e.g. press('left_arrow', 'a','b').
        '''
        for i in args:
            win32api.keybd_event(VK_CODE[i], 0,0,0)
            self.msleep(50)
            win32api.keybd_event(VK_CODE[i],0 ,win32con.KEYEVENTF_KEYUP ,0)


    def on(self):
        self._status = True
        self.message.emit('낚시 시작')
        self.cond.wakeAll()

    def off(self):
        self._status = False
        self.message.emit('낚시 중지')

    @property
    def status(self):
        return self._status
