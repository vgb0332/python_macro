from fbs_runtime.application_context import ApplicationContext, cached_property
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import requests

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        text = QLabel()
        text.setWordWrap(True)
        button = QPushButton('Next quote >')
        button.clicked.connect(lambda: text.setText(_get_quote()))
        layout = QVBoxLayout()
        layout.addWidget(text)
        layout.addWidget(button)
        layout.setAlignment(button, Qt.AlignHCenter)
        self.setLayout(layout)


def _get_quote():
    response = requests.get('https://talaikis.com/api/quotes/random/')
    return response.json()['quote']

def print_hi():
    print('hi')
    return

if __name__ == '__main__':
    print('no')
