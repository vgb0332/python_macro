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
from CursorThread import CursorThread
from MethodThread import FishingThread
from getRGBColor import rgbint2rgbtuple
form_class = uic.loadUiType("main_ui.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.activeMethod = None
        self.running = False

        self.cursorThread = CursorThread()
        self.fishingThread = FishingThread()
        self.setupUi(self)
        self.windowX.setText( str(GetSystemMetrics(0)) )
        self.windowY.setText( str(GetSystemMetrics(1)) )

        self.startBtn.clicked.connect(self.startBtnClicked)
        self.testBtn.clicked.connect(self.testBtnClicked)
        self.endBtn.clicked.connect(self.endBtnClicked)

        #
        self.cursorThread.mouseXPos.connect(self.mouseXPos.setText)
        self.cursorThread.mouseYPos.connect(self.mouseYPos.setText)
        self.cursorThread.mouseColorCode.connect(self.cursorColorCode.setText)
        self.cursorThread.mouseColorBox.connect(self.cursorColorBox.setStyleSheet)
        self.cursorThread.message.connect(self.updateConsole)
        self.cursorThread.start()
        #

        #
        self.fishingThread.mouseXPos.connect(self.mouseXPos.setText)
        self.fishingThread.mouseYPos.connect(self.mouseYPos.setText)
        self.fishingThread.mouseColorCode.connect(self.cursorColorCode.setText)
        self.fishingThread.mouseColorBox.connect(self.cursorColorBox.setStyleSheet)
        self.fishingThread.message.connect(self.updateConsole)
        self.fishingThread.start()
        #

    def endBtnClicked(self):
        QCoreApplication.quit()

    @pyqtSlot(str)
    def updateConsole(self, message) :
        curMessage = self.consoleText.toPlainText()
        print(curMessage)
        print(message)
        self.consoleText.setText( curMessage + '\n' + message)

    @pyqtSlot()
    def testBtnClicked(self) :
        if self.cursorThread.status:
            self.testBtn.setText('테스트')
        else :
            self.testBtn.setText('테스트 중지')

        self.cursorThread.toggle_status()

    @pyqtSlot()
    def startBtnClicked(self) :
        if self.running :
            if self.fishingThread.status :
                self.fishingThread.off()

            # if self.gatheringThead.status:
            #     self.gatheringThread.off()
            self.startBtn.setText('시작')
            self.running = False
        else :
            isFishing = self.fishingRadioButton.isChecked()
            isGathering = self.gatheringRadioButton.isChecked()

            if not isFishing and not isGathering :
                self.showAlertMessage( '뭐할건지 선택해', '알림', '채집이냐 낚시냐...')
                return

            if isFishing :
                self.fishingThread.on()

            # if isGathering:
            #     self.gatheringThead.on()
            self.startBtn.setText('중지')
            self.running = True


    def showAlertMessage( self, message, title, additional ) :
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText(message)
        msg.setWindowTitle(title)
        msg.setDetailedText(additional)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
