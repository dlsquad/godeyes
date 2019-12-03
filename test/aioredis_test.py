import time
import uvloop
import asyncio
import aioredis
import aiomysql
import random

from concurrent.futures import ProcessPoolExecutor


def task(fpath: str, ch: int):
    """模拟cpu密集型任务"""
    time.sleep(2)
    print(f"channel: {ch} ==> fpath: {fpath}")


async def publish(loop):
    """消息发布者, 随机选取一个channel发布消息"""
    await asyncio.sleep(2)
    conn = await aioredis.create_redis("redis://localhost", loop=loop)
    channels = await conn.pubsub_channels('channel:*')
    print(f"publish get channels => {channels}")
    while 1:
        channel = random.choice(channels)
        await conn.publish(channel, "hello world")
        await asyncio.sleep(1)


async def worker(loop, executor, ch):
    """启用redis订阅模式，获取消息并将任务提交给进程池处理
    Args:
        loop: 事件循环
        executor: 进程池实例
        ch (int): 信道编号
    """
    conn = await aioredis.create_redis("redis://localhost", loop=loop)
    channel = (await conn.subscribe(f"channel:{ch}"))[0]
    print(f"channel====> {channel}")
    while await channel.wait_message():
        fpath = await channel.get(encoding="utf-8")
        await loop.run_in_executor(executor, task, fpath, ch)


async def main(loop):
    with ProcessPoolExecutor(max_workers=8) as executor:
        await asyncio.gather(*([worker(loop, executor, ch) for ch in range(8)]+[publish(loop)]))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))

