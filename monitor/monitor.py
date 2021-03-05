from bilibili_api import live
import asyncio



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
    def __init__(self, id):
        self.id = id
        self.live = live.LiveDanmaku(id)
        self.bc_id = set()
        self.sc_id = set()

        # @self.live.on('DANMU_MSG')
        # async def on_danmu(msg):
        #     data = msg['data']['info']
        #     # print(data)
        #     print(data[2][1] + ': ' + data[1])

        @self.live.on('SEND_GIFT')
        async def on_gift(msg):
            data = msg['data']['data']
            if data['total_coin'] > 0:
                # print('礼物  ', end='')
                if data['giftName'] != '辣条':
                    # print(data)
                    bc_id = data['batch_combo_id']
                    if bc_id not in self.bc_id:
                        self.bc_id.add(bc_id)
                        print('礼物  ', end='')
                        print(data['uname'] + ': ' + data['giftName'])
                        # print(self.bc_id)
                        await asyncio.sleep(5)
                        try:
                            self.bc_id.remove(bc_id)
                        except:
                            pass

        @self.live.on('COMBO_SEND')
        async def on_gift_combo(msg):
            data = msg['data']['data']
            if data['combo_total_coin'] > 0:
                # print(data)
                # print('礼物连击  ', end='')
                if data['gift_name'] != '辣条':
                    bc_id = data['batch_combo_id']
                    print('\n礼物连击  ', end='')
                    print(data['uname'] + ': ' + data['gift_name'] + ' ' + str(data['batch_combo_num']) + '个\n')
                    try:
                        self.bc_id.remove(bc_id)
                    except:
                        pass

        @self.live.on('GUARD_BUY')
        async def on_guard(msg):
            data = msg['data']['data']
            print()
            print('大航海  ', end='')
            print(data['username'] + ': ' + data['gift_name'])
            print()

        @self.live.on('SUPER_CHAT_MESSAGE')
        async def on_SC(msg):
            data = msg['data']['data']
            sc_id = int(data['id'])
            if sc_id in self.sc_id:
                self.sc_id.remove(sc_id)
            else:
                self.sc_id.add(sc_id)
                print()
                print('￥' + str(data['price']) + ' SC  ' + data['user_info']['uname'] + ': ' + data['message'])
                print()

            await asyncio.sleep(5)
            try:
                self.sc_id.remove(sc_id)
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

                await asyncio.sleep(5)
            try:
                self.sc_id.remove(sc_id)
            except:
                pass
            # print(self.sc_id)

        # @self.live.on('DANMU_MSG')
        # async def on_danmu(msg):
        #     print(msg)

        # @self.live.on('ALL')
        # async def on_all(msg):
        #     print(msg)

        self.live.connect()

    def get_gifts(self):
        pass

