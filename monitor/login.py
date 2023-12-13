import json
import sys
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from bilibili_api import login_func, user, sync


# 二维码登录窗口类
class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.setFixedSize(360, 420)
        icon = QtGui.QIcon()
        Login.setWindowIcon(icon)
        self.label_5 = QtWidgets.QLabel(Login)
        self.label_5.setGeometry(QtCore.QRect(20, 80, 322, 322))
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.label_2 = QtWidgets.QLabel(Login)
        self.label_2.setGeometry(QtCore.QRect(70, 20, 170, 42))
        self.label_2.setObjectName("label_2")
        self.pushButton_2 = QtWidgets.QPushButton(Login)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 0, 100, 80))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Login)

        qrcode_data = login_func.get_qrcode()
        self.pixmap = QtGui.QPixmap()
        self.pixmap.loadFromData(qrcode_data[0].content, qrcode_data[0].imageType)
        self.label_5.setPixmap(self.pixmap)
        self.label_5.setScaledContents(True)
        self.qrcode_sec = qrcode_data[1]

        self.pushButton_2.setIcon(QtGui.QIcon(QtGui.QPixmap("update.jpg")))

        def update_qrcode():
            qrcode_data = login_func.get_qrcode()
            self.label_5.setPixmap(QtGui.QPixmap(qrcode_data[0]))
            self.label_5.setScaledContents(True)
            self.label_5.update()
            self.qrcode_sec = qrcode_data[1]
        self.pushButton_2.clicked.connect(update_qrcode)

        Login.startTimer(1000)
        def timerEvent(*args, **kwargs):
            _translate = QtCore.QCoreApplication.translate
            try:
                events = login_func.check_qrcode_events(self.qrcode_sec)
            except:
                self.label_2.setText(_translate("Login", "⚫️二维码登录"))
                return
            else:
                if events == None: return
                if events[0] == login_func.QrCodeLoginEvents.SCAN:
                    self.label_2.setText(_translate("Login", "🔴二维码登录"))
                elif events[0] == login_func.QrCodeLoginEvents.CONF:
                    self.label_2.setText(_translate("Login", "🟡二维码登录"))
                elif events[0] == login_func.QrCodeLoginEvents.DONE:
                    self.label_2.setText(_translate("Login", "🟢二维码登录"))
                    credential = events[1]
                    Login.credential = credential
                    self_info = sync(user.get_self_info(credential)) # type: ignore
                    reply = QtWidgets.QMessageBox.information(
                        Login,
                        "已成功登录到你的帐号",
                        "欢迎：" + self_info['name'],
                        QtWidgets.QMessageBox.Ok
                    )
                    Login.close()
                    return 1
        Login.timerEvent = timerEvent

        # while True:
        #     time.sleep(3)
        #     if timerEvent() == 1:
        #         break

        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "登录"))
        self.label_2.setText(_translate("Login", "🔴二维码登录"))