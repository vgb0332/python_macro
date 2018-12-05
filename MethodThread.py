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
import keyboard

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
        self.firstTime = False
        self.hotKey = keyboard.add_hotkey('ctrl+q', self.quit, args=[self])
        self.startKey = keyboard.add_hotkey('f5', self.active, args=[self])

    def __del__(self):
        self.wait()

    def active(self, message) :
        print('lets getit')
        self.on()

    def quit(self, message) :
        self.off()

    def run(self):
        xPos = int(GetSystemMetrics(0) / 2)
        yPos = int(GetSystemMetrics(1)*6  / 7)
        # yPos = int(GetSystemMetrics(1) / 2)
        self.mouseXPos.emit(str(xPos))
        self.mouseYPos.emit(str(yPos))

        while True:
            self.mutex.lock()
            if not self._status:
                self.cond.wait(self.mutex)

            # if(self.firstTime) :
            #     win32api.SetCursorPos((xPos,yPos))
            #     self.right_click(xPos, yPos)
            #     self.msleep(1000)
            #     self.press('b')
            #     self.firstTime = False
            # print('restart')
            self.msleep(1000)
            self.press('w')
            self.msleep(5000)
            self.color = self.getColor( xPos, yPos )
            self.message.emit('inital color' + str(self.color))
            while True :
                if not self._status:
                    break
                try :
                    rgb = self.getColor( xPos, yPos )
                    self.mouseColorCode.emit(str(rgb))
                    self.mouseColorBox.emit("background-color:"+"rgb"+str(rgb))
                    if rgb[0] == 255:
                        print('gotcha')
                        self.message.emit('색 변화 감지, 낚아올려부려!' + str(rgb))
                        self.press('w')
                        self.msleep(5000)
                        print('done')
                        break
                except :
                    print('hmmm why?')
                    continue

            self.msleep(100)  # ※주의 QThread에서 제공하는 sleep을 사용

            self.mutex.unlock()
    def getColor(self, xPos, yPos) :
        i_desktop_window_id = win32gui.GetDesktopWindow()
        i_desktop_window_dc = win32gui.GetWindowDC(i_desktop_window_id)
        color = win32gui.GetPixel(i_desktop_window_dc, xPos , yPos)
        rgb = (color & 0xff), ((color >> 8) & 0xff), ((color >> 16) & 0xff)
        return rgb

    def press(self, *args):
        '''
        one press, one release.
        accepts as many arguments as you want. e.g. press('left_arrow', 'a','b').
        '''
        for i in args:
            win32api.keybd_event(VK_CODE[i], 0,0,0)
            self.msleep(50)
            win32api.keybd_event(VK_CODE[i],0 ,win32con.KEYEVENTF_KEYUP ,0)

    def left_click(self, xPos, yPos) :
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,xPos,yPos,0,0)
        self.msleep(50)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,xPos,yPos,0,0)

    def right_click(self, xPos, yPos) :
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,xPos,yPos,0,0)
        self.msleep(50)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,xPos,yPos,0,0)

    def on(self):
        self._status = True
        self.firstTime = True
        self.message.emit('낚시 시작')
        self.cond.wakeAll()

    def off(self):
        self._status = False
        self.firstTime = False
        self.message.emit('낚시 중지')

    @property
    def status(self):
        return self._status

class GatheringThread(QThread):
    # 사용자 정의 시그널 선언
    message = pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self)
        self.cond = QWaitCondition()
        self.mutex = QMutex()
        self.zeroPos = ( int(GetSystemMetrics(0)/2), int(GetSystemMetrics(1)/2) )
        self.distance = 100
        self._status = False
        self.color = None
        # self.hotKey = keyboard.add_hotkey('ctrl+q', self.quit, args=[self])

    def __del__(self):
        self.wait()

    def quit(self, message) :
        self.off()

    def run(self):
        print('zeroPos', self.zeroPos)
        while True:
            self.mutex.lock()
            if not self._status:
                self.cond.wait(self.mutex)
            while True:
                if not self._status:
                    break
                if self.checkIfGathering() :
                    self.msleep(4000)
                self.move_left()


            self.mutex.unlock()

    def checkIfGathering(self) :
        self.press('g')
        self.msleep(100)
        i_desktop_window_id = win32gui.GetDesktopWindow()
        i_desktop_window_dc = win32gui.GetWindowDC(i_desktop_window_id)

        x, y = self.zeroPos
        try :
            color = win32gui.GetPixel(i_desktop_window_dc, 816 , 742)
            rgb = (color & 0xff), ((color >> 8) & 0xff), ((color >> 16) & 0xff)
            if rgb[0] > 205 and rgb[0] < 215:
                return True
        except :
            return False


    def getColor(self, xPos, yPos) :
        i_desktop_window_id = win32gui.GetDesktopWindow()
        i_desktop_window_dc = win32gui.GetWindowDC(i_desktop_window_id)
        color = win32gui.GetPixel(i_desktop_window_dc, xPos , yPos)
        rgb = (color & 0xff), ((color >> 8) & 0xff), ((color >> 16) & 0xff)
        return rgb

    def press(self, *args):
        '''
        one press, one release.
        accepts as many arguments as you want. e.g. press('left_arrow', 'a','b').
        '''
        for i in args:
            win32api.keybd_event(VK_CODE[i], 0,0,0)
            self.msleep(50)
            win32api.keybd_event(VK_CODE[i],0 ,win32con.KEYEVENTF_KEYUP ,0)

    def move_left(self) :
        x, y = self.zeroPos
        self.message.emit('moving left')
        print(x - int(self.distance),y)
        win32api.SetCursorPos((x - int(self.distance) , y))
        self.right_click(x - int(self.distance) , y)

    def move_right(self) :
        x, y = self.zeroPos
        self.message.emit('moving right')
        win32api.SetCursorPos((x + int(self.distance) , y))
        self.right_click(x + int(self.distance) , y)

    def move_up(self):
        x, y = self.zeroPos
        self.message.emit('moving up')
        win32api.SetCursorPos((x , y - int(self.distance)))
        self.right_click(x , y - int(self.distance))

    def move_down(self):
        x, y = self.zeroPos
        self.message.emit('moving down')
        win32api.SetCursorPos((x , y + int(self.distance)))
        self.right_click(x , y + int(self.distance))

    def move_leftup(self):
        x, y = self.zeroPos
        self.message.emit('moving leftup')
        win32api.SetCursorPos((x - int(self.distance) , y - int(self.distance)))
        self.right_click(x - int(self.distance) , y - int(self.distance))

    def move_rightup(self):
        x, y = self.zeroPos
        self.message.emit('moving rightup')
        win32api.SetCursorPos((x + int(self.distance) , y - int(self.distance)))
        self.right_click(x + int(self.distance) , y - int(self.distance))

    def move_leftdown(self):
        x, y = self.zeroPos
        self.message.emit('moving leftdown')
        win32api.SetCursorPos((x - int(self.distance) , y + int(self.distance)))
        self.right_click(x - int(self.distance) , y + int(self.distance))

    def move_rightdown(self):
        x, y = self.zeroPos
        self.message.emit('moving rightdowt')
        win32api.SetCursorPos((x + int(self.distance) , y + int(self.distance)))
        self.right_click(x + int(self.distance) , y + int(self.distance))

    def left_click(self, xPos, yPos) :
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,xPos,yPos,0,0)
        self.msleep(50)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,xPos,yPos,0,0)

    def right_click(self, xPos, yPos) :
        print('right_click', xPos, yPos)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,xPos,yPos,0,0)
        self.msleep(50)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,xPos,yPos,0,0)

    def on(self):
        self._status = True
        self.message.emit('채집 시작')
        self.cond.wakeAll()

    def off(self):
        self._status = False
        self.message.emit('채집 중지')

    @property
    def status(self):
        return self._status
