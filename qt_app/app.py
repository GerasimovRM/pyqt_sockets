import sys
import pickle

from PyQt5.QtCore import QUrl, QTimer, QCoreApplication
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5 import QtCore, QtWebSockets
from ui_main import Ui_MainWindow


class QtTestApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(QtTestApp, self).__init__()
        self.setupUi(self)

        self.client = QtWebSockets.QWebSocket("", QtWebSockets.QWebSocketProtocol.Version13, None)
        self.client.error.connect(self.error)

        self.client.open(QUrl("ws://127.0.0.1:8000"))
        self.client.textMessageReceived.connect(self.receive_message)

    def send_message(self):
        self.client.sendTextMessage("ok")

    def receive_message(self, message):
        print(f"client: receive message: {message}")
        self.client.sendTextMessage("ok")
        self.listWidget.addItem(message)

    def error(self, error_code):
        print("error code: {}".format(error_code))
        print(self.client.errorString())


sys._excepthook = sys.excepthook


def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = exception_hook


if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = QtTestApp()
    client.show()
    sys.exit(app.exec())