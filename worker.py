import os
import json
import random
import uvloop
import logging
import asyncio
import aioredis
import aiofiles
import aiomysql
import logging.config
import face_recognition
from datetime import datetime

from src.utils.face_util import FaceUtil
from concurrent.futures import ProcessPoolExecutor


CURRENT_WORK_DIR = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(os.path.join(CURRENT_WORK_DIR, "conf", "logging.conf"))

logger = logging.getLogger("worker")
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def get_model(fpath) -> (str, str):
    """获取人脸encoding和location信息"""
    img = face_recognition.load_image_file(fpath)
    locations = face_recognition.face_locations(img)
    encodings = face_recognition.face_encodings(img, locations)
    if not (locations and encodings):
        return None
    return json.dumps(locations), json.dumps([e.tolist() for e in encodings])


async def save_model(fpath: str, data: str):
    async with aiofiles.open(fpath, "w") as f:
        await f.write(data)


async def worker(loop, executor, ch):
    """启用redis订阅模式，获取消息并将任务提交给进程池处理
       拿到face encoding和location之后分别保存在文件里
    Args:
        loop: 事件循环
        executor: 进程池实例
        ch (int): 信道编号
    """
    logger.info(f"worker: {ch} started.")
    conn = await aioredis.create_redis("redis://localhost", loop=loop)
    channel = (await conn.subscribe(f"channel:{ch}"))[0]
    while await channel.wait_message():
        fpath = await channel.get(encoding="utf-8")
        logger.info(f"start get_model(fpath): {fpath}")
        data = await loop.run_in_executor(executor, get_model, fpath)
        logger.info(f"end get_model(fpath): {fpath}")
        if not data:
            logger.error(f"picture {fpath} recognize error.")
            continue

        code = fpath.rsplit("/", 1)[-1].rsplit(".", 1)[0]
        encoding_path = f"{FaceUtil.model_path}/{code}-encode.model"
        location_path = f"{FaceUtil.model_path}/{code}-location.model"
        await asyncio.gather(
            save_model(location_path, data[0]),
            save_model(encoding_path, data[1])
        )
        logger.info(f"worker{ch}: the model of picture {code} have saved.")



async def main(loop):
    with ProcessPoolExecutor(max_workers=8) as executor:
        await asyncio.gather(*[worker(loop, executor, ch) for ch in range(8)])


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))

