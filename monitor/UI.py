from PyQt5.QtCore import pyqtProperty, QCoreApplication, QObject, QUrl
from PyQt5.QtQml import qmlRegisterType, QQmlComponent, QQmlEngine
from PyQt5.QtWidgets import QWidget


class LoginWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.credential = None

