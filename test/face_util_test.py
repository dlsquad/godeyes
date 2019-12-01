import asyncio

from src.utils.face_util import FaceUtil
import pandas as pd


async def main():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', 50)

    target_path = "./static/user/陈恩泉.jpeg"
    group_path = "./static/picture/123456.jpg"
    fname = "./static/user/陈恩泉-123456.jpg"
    position = await FaceUtil(target_path, group_path)(fname)
    print("position===>", position)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

