import sys
import uuid
import time
import asyncio
from pathlib import Path
from apscheduler.schedulers.asyncio import AsyncIOScheduler


from PyQt5.QtWidgets import QApplication

from monitor import Monitor, Data, Ui_Login, LoginWidget
from monitor.monitor import get_time


def login():

    app = QApplication(sys.argv)
    Login = LoginWidget()
    ui_login = Ui_Login()
    ui_login.setupUi(Login)
    Login.show()
    app.exec()

    return Login.credential


def main(credential):

    sched = AsyncIOScheduler()

    loop = asyncio.get_event_loop()
    rid = int(input('请输入直播间号：'))
    uid = int(input('请输入UID：'))
    data_path = fr".\data\{time.strftime('%Y%m%d%H%M%S', time.gmtime())}"
    Path(data_path).mkdir(parents=True, exist_ok=True)

    data = Data(data_path)
    monitor = Monitor(rid, uid, data, credential, sched)

    cors = asyncio.wait([monitor.live.connect(), monitor.online_num(60)])
    loop.run_until_complete(cors)


if __name__ == '__main__':
    credential = login()
    buvid3 = str(uuid.uuid1())  # input("请输入buvid3码：")
    credential.buvid3 = buvid3
    main(credential)


# pyinstaller --onedir --add-data "D:\PythonProject\0 VirtualVenv\StreamMonitor\\Lib\site-packages\bilibili_api\data\api.json;data" -p ./monitor main.py