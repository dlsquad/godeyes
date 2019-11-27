"""
模型服务入口
"""

import os
import aiofiles
import asyncio
import logging.config

from sanic import Sanic
from aiofiles import os as async_os
from sanic.blueprints import Blueprint
from sanic.response import json, file_stream

from handler.user import User
from handler.picture import Picture

CURRENT_WORK_DIR = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(os.path.join(CURRENT_WORK_DIR, "conf", "logging.conf"))


app = Sanic("faceplus")
logger = logging.getLogger("web")


@app.route("/", methods=["GET"])
async def index(request):
    file_path = "./data/classmate.jpeg"
    file_stat = await async_os.stat(file_path)
    headers = {"Content-Length": str(file_stat.st_size)}
    return await file_stream(file_path, headers=headers, chunked=False)


@app.route("/picture", methods=["POST"])
async def post_picture(request):
    for f in list(request.files.values())[0]:
        async with aiofiles.open(f"./image/picture/{f.name}", "wb") as w:
            await w.write(f.body)
    return json({"picture_id": 1})


@app.route("/picture/<picture_id>", methods=["GET"])
async def get_picture(request, picture_id):
    pass


@app.route("/picture/<picture_id>", methods=["PUT"])
async def put_picture(request, picture_id):
    pass




if __name__ == "__main__":
    app.run(debug=True, access_log=True, host="localhost", port=8080)
