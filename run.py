"""
模型服务入口
"""

import os
import asyncio
import logging.config

from sanic import Sanic
from aiofiles import os as async_os
from sanic.blueprints import Blueprint
from sanic.response import json, file_stream

CURRENT_WORK_DIR = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(os.path.join(CURRENT_WORK_DIR, "conf", "logging.conf"))


app = Sanic("faceplus")
bp = Blueprint("mybp")
logger = logging.getLogger("web")


@bp.get("/")
async def index(request):
    file_path = "./data/classmate.jpeg"
    file_stat = await async_os.stat(file_path)
    headers = {"Content-Length": str(file_stat.st_size)}
    return await file_stream(file_path, headers=headers, chunked=False)


@bp.post("/picture", stream=True)
async def post_picture(request):
    pass


@bp.get("/picture/<picture_id>")
async def get_picture(request, picture_id):
    pass


@bp.put("/picture/<picture_id>")
async def put_picture(request, picture_id):
    pass



if __name__ == "__main__":
    app.run(debug=True, access_log=True, host="localhost", port=8080)
