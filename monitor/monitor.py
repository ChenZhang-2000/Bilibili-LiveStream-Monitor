from bilibili_api import live, Credential, sync
from bilibili_api.utils.network import Api

import asyncio
import time

from apscheduler.schedulers.asyncio import AsyncIOScheduler


ONLINE_RANK_API = {
    "url": "https://api.live.bilibili.com/xlive/general-interface/v1/rank/getOnlineRank",
    "method": "GET",
    "verify": False,
    "params": {
      "page": "int: 页码",
      "pageSize": 50,
      "roomId": "int: 真实房间号",
      "ruid": "int: 全称 room_uid，从 room_play_info 里头的 uid 可以找到",
      "platform": "pc_link"
    },
    "comment": "获取在线用户"
}


def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())


class EventHandeler(dict):
    def __init__(self):
        super(EventHandeler, self).__init__()

    def __getitem__(self, item):
        if item in {'SEND_GIFT', 'COMBO_SEND'}:
            return

        elif item == 'GUARD_BUY':
            return

        elif item in {'SUPER_CHAT_MESSAGE', 'SUPER_CHAT_MESSAGE_JPN'}:
            return


class Monitor:
    def __init__(self, rid, uid, data, credential=None, sched=None):
        self.id = rid
        self.uid = uid
        self.data = data
        self.credential = Credential() if credential is None else credential
        self.sched = sched

        # print(self.credential.sessdata)
        self.live = live.LiveDanmaku(rid, credential=self.credential)

        # print(self.live.credential.sessdata)
        self.bc_id = set()
        self.sc_id = set()

        # @self.live.on('DANMU_MSG')
        # async def on_danmu(msg):
        #     data = msg['data']['info']
        #     # print(data)
        #     print(data[2][1] + ': ' + data[1])

        @self.live.on("DANMU_MSG")
        async def on_danmu(msg):
            with open(fr"{self.data.data_path}\danmu_info.txt", "a", encoding="utf_8_sig") as f:
                f.write(str(msg))
                f.write("\n")
            f.close()
            uid = msg["data"]["info"][2][0]
            uname = msg["data"]["info"][2][1]
            # if uid == self.uid:
            #     return
            content = msg["data"]["info"][1]
            if msg["data"]["info"][3] != []:
                fans_medal = (msg["data"]["info"][3][2], msg["data"]["info"][3][1], msg["data"]["info"][3][0])
            else:
                fans_medal = ("", "", "")
            print("收到弹幕")
            print(f"  发送者：{uname}\n  内容：{content}\n  粉丝勋章：{fans_medal}")
            t = get_time()
            self.data.add_danmu([str(t),
                                 str(fans_medal[0]),
                                 str(fans_medal[1]),
                                 str(fans_medal[2]),
                                 str(uname),
                                 str(content)])
            # self.sched.add_job(self.check, 'interval', seconds=1, args=[uid, t], id=str((uid, t)))

        @self.live.on('SEND_GIFT')
        async def on_gift(msg):
            with open(fr"{self.data.data_path}\gift_info.txt", "a", encoding="utf_8_sig") as f:
                f.write(str(msg))
                f.write("\n")
            f.close()
            # print(msg)
            data = msg['data']['data']
            if data['total_coin'] >= 0:
                # print('礼物  ', end='')
                if data['giftName'] != '':
                    # print(data)
                    bc_id = data['batch_combo_id']
                    if bc_id not in self.bc_id:
                        self.bc_id.add(bc_id)
                        print('礼物  ', end='')
                        print(data['uname'] + ': ' + data['giftName'])
                        self.data.add_gift([get_time(),
                                            data['medal_info']["medal_name"],
                                            data['medal_info']["medal_level"],
                                            data['uname'],
                                            data['giftName'],
                                            data['total_coin']])
                        # print(self.bc_id)
                        await asyncio.sleep(10)
                        try:
                            self.bc_id.remove(bc_id)
                        except:
                            pass
                    else:
                        self.data.add_gift([get_time(),
                                            data['medal_info']["medal_name"],
                                            data['medal_info']["medal_level"],
                                            data['uname'],
                                            data['giftName'],
                                            data['total_coin']])

        @self.live.on('COMBO_SEND')
        async def on_gift_combo(msg):
            data = msg['data']['data']
            if data['combo_total_coin'] >= 0:
                # print(data)
                print('礼物连击  ', end='')
                if data['gift_name'] != '':
                    bc_id = data['batch_combo_id']
                    print('\n礼物连击  ', end='')
                    print(data['uname'] + ': ' + data['gift_name'] + ' ' + str(data['batch_combo_num']) + '个\n')
                    self.data.add_gift([get_time(),
                                        data['medal_info']["medal_name"],
                                        data['medal_info']["medal_level"],
                                        data['uname'],
                                        data['giftName'],
                                        data['combo_total_coin']])
                    try:
                        self.bc_id.remove(bc_id)
                    except:
                        pass

        @self.live.on('GUARD_BUY')
        async def on_guard(msg):
            with open(fr"{self.data.data_path}\guard_info.txt", "a") as f:
                f.write(str(msg))
                f.write("\n")
            f.close()
            try:
                data = msg['data']['data']
                print()
                print('大航海  ', end='')
                print(data['username'] + ': ' + data['gift_name'])
                self.data.add_guard([get_time(),
                                     data['medal_info']["medal_name"],
                                     data['medal_info']["medal_level"],
                                     data['username'],
                                     data['giftName'],
                                     "0"])
            except:
                pass
            print()

        @self.live.on('SUPER_CHAT_MESSAGE')
        async def on_SC(msg):
            with open(fr"{self.data.data_path}\sc_info.txt", "a") as f:
                f.write(str(msg))
                f.write("\n")
            f.close()
            try:
                data = msg['data']['data']
                sc_id = int(data['id'])
                if sc_id in self.sc_id:
                    self.sc_id.remove(sc_id)
                else:
                    self.sc_id.add(sc_id)
                    print()
                    print('￥' + str(data['price']) + ' SC  ' + data['user_info']['uname'] + ': ' + data['message'])
                    print()
                    self.data.add_SC([get_time(),
                                      data['medal_info']["medal_name"],
                                      data['medal_info']["medal_level"],
                                      data['user_info']['uname'],
                                      data['message'],
                                      data['price']])

                await asyncio.sleep(5)
                try:
                    self.sc_id.remove(sc_id)
                except:
                    pass

            except:
                pass
            # print(self.sc_id)

        @self.live.on('SUPER_CHAT_MESSAGE_JPN')
        async def on_JSC(msg):
            data = msg['data']['data']
            sc_id = int(data['id'])
            if sc_id in self.sc_id:
                self.sc_id.remove(sc_id)
            else:
                self.sc_id.add(sc_id)
                print()
                print('￥' + str(data['price']) + ' SC  ' + data['user_info']['uname'] + ': ' + data['message'])
                print()
                self.data.add_SC([get_time(), data['user_info']['uname'], data['message'], data['price']])

                await asyncio.sleep(5)
            try:
                self.sc_id.remove(sc_id)
            except:
                pass

        # sched.start()

        # _ = sync(self.online_num())
        # print("TEST")
        # sync(self.live.connect())

    async def get_online_rank(self):
        page = 1
        params = {
            "roomId": self.id,
            "ruid": self.uid,
            "pageSize": 50,
            "page": page,
            "platform": "pc_link",
        }
        return await Api(**ONLINE_RANK_API, credential=self.credential).update_params(**params).result

    async def online_num(self, T=10):
        # url = fr"api.live.bilibili.com/xlive/general-interface/v1/rank/getOnlineRank?page=1&pageSize=50&roomId={rid}&ruid={uid}&platform=%22pc_link%22"
        # r = await live.get_gaonengbang()
        # print(r.keys())
            t = 0
            while True:
                await asyncio.sleep(T-t)

                t0 = time.time()
                r = await self.get_online_rank()
                with open(fr"{self.data.data_path}\onlineNum.txt", "a") as f:
                    f.write(f"{get_time()} {r['onlineNum']}\n")
                f.close()

                await self.data.save()
                t = time.time() - t0

            # print(r.keys())
        # return

    # async def check(self, uid: int, t: str):
    #     '判断是否超过阈值并输出'
    #     user = user_list.get(uid)
    #     if user:
    #         if int(time.time()) - user.get('last_gift_time', 0) > 5:  # 此处的 5 即需求中的 n 表示秒数
    #             self.sched.remove_job(str(uid))  # 移除该监控任务
    #             print(user_list.pop(uid))  # 将该用户从列表中弹出并打印