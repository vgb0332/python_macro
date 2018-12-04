from fbs_runtime.application_context import ApplicationContext, cached_property
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from init import MainWindow

import sys

class AppContext(ApplicationContext):
    def run(self):
        stylesheet = self.get_resource('styles.qss')
        self.app.setStyleSheet(open(stylesheet).read())
        self.window.show()
        return self.app.exec_()

    @cached_property
    def window(self):
        return MainWindow()

# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         text = QLabel()
#         text.setWordWrap(True)
#         button = QPushButton('Next quote >')
#         button.clicked.connect(lambda: text.setText(_get_quote()))
#         layout = QVBoxLayout()
#         layout.addWidget(text)
#         layout.addWidget(button)
#         layout.setAlignment(button, Qt.AlignHCenter)
#         self.setLayout(layout)
#
# def _get_quote():
#     response = requests.get('https://talaikis.com/api/quotes/random/')
#     return response.json()['quote']

if __name__ == '__main__':
    appctxt = AppContext()                      # 4. Instantiate the subclass
    exit_code = appctxt.run()                   # 5. Invoke run()
    sys.exit(exit_code)
