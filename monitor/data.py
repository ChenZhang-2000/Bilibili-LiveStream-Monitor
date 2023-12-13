import pandas as pd


class Data:
    def __init__(self, data_path):
        self.gift = pd.DataFrame(columns=["Time", "MedalName", "Level", "uname", "GiftName", "Value"])
        self.danmu = pd.DataFrame(columns=["Time", "Streamer", "MedalName", "Level", "uname", "Content"])
        self.SC = pd.DataFrame(columns=["Time", "MedalName", "Level", "uname", "Content", "Value"])
        self.guard = pd.DataFrame(columns=["Time", "MedalName", "Level", "uname", "GuardLevel", "Value"])
        self.data_path = data_path

        self.gift_count = 0
        self.danmu_count = 0
        self.SC_count = 0
        self.guard_count = 0

    def add_gift(self, content):
        self.gift.loc[self.gift_count] = content
        self.gift_count += 1

    def add_danmu(self, content):
        self.danmu.loc[self.danmu_count] = content
        self.danmu_count += 1
        # print(self.danmu)

    def add_SC(self, content):
        self.SC.loc[self.SC_count] = content
        self.SC_count += 1

    def add_guard(self, content):
        self.guard.loc[self.guard_count] = content
        self.guard_count += 1

    async def save(self):
        self.gift.to_csv(fr"{self.data_path}\gift.csv", mode="a", header=False, encoding="utf_8_sig")
        self.danmu.to_csv(fr"{self.data_path}\danmu.csv", mode="a", header=False, encoding="utf_8_sig")
        self.SC.to_csv(fr"{self.data_path}\sc.csv", mode="a", header=False, encoding="utf_8_sig")
        self.guard.to_csv(fr"{self.data_path}\guard.csv", mode="a", header=False, encoding="utf_8_sig")
        self.gift = pd.DataFrame(columns=["Time", "MedalName", "Level", "uname", "GiftName", "Value"])
        self.danmu = pd.DataFrame(columns=["Time", "Streamer", "MedalName", "Level", "uname", "Content"])
        self.SC = pd.DataFrame(columns=["Time", "MedalName", "Level", "uname", "Content", "Value"])
        self.guard = pd.DataFrame(columns=["Time", "MedalName", "Level", "uname", "GuardLevel", "Value"])


def decode_online_rank(r):
    num = r["onlineNum"]
    item = r["item"]

    return ...

