import asyncio
from monitor import Monitor


async def main():
    pass
    # while True:
    #     await asyncio.sleep(0.1)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    id = int(input('Please type in stream id\n'))
    monitor = Monitor(id)

    asyncio.run(main())

# pyinstaller --onedir --add-data "D:\PythonProject\0 VirtualVenv\StreamMonitor\\Lib\site-packages\bilibili_api\data\api.json;data" -p ./monitor main.py