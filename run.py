"""
模型服务入口
"""

import os
import asyncio
import logging.config

from sanic import Sanic
from aiofiles import async_os
from sanic.response import json, file_stream

CURRENT_WORK_DIR = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(os.path.join(CURRENT_WORK_DIR, "conf", "logging.conf"))


app = Sanic("myapp")
logger = logging.getLogger("web")


@app.route("/")
async def index(request):
    file_path = "./data/classmate.jpeg"
    file_stat = await async_os.stat(file_path)
    headers = {"Content-Length": str(file_stat.st_size)}
    return await file_stream(file_path, headers=headers, chunked=False)


@app.route("/find")
async def find(request):
    pass


if __name__ == "__main__":
    app.run(debug=True, access_log=True, host="localhost", port=8080)
