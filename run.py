"""
模型服务入口
"""

import os
import base64
import aiofiles
import asyncio
import logging
import logging.config

from sanic import Sanic
from aiofiles import os as async_os
from sanic.response import json, file_stream

from src.handler.user import user
from src.handler.picture import picture

CURRENT_WORK_DIR = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(os.path.join(CURRENT_WORK_DIR, "conf", "logging.conf"))


app = Sanic("faceplus")
app.static('/static', './static')
logger = logging.getLogger("web")

@app.route("/", methods=["GET"])
async def index(request):
    return json({
        "isSuccess": "true",
        "msg": "welcome to faceplus system!",
        "data": {
            "url": "xxxx.com/xx.png"
        }
    })

@app.route("/picture/post", methods=["POST"])
async def post_picture(request):
    """上传集体照,并返回集体照的查看码。"""
    data = request.json.get("pic", None)
    if not data:
        return json({
            "isSuccess": "false",
            "msg": "paramter pic is not find",
            "data": {
                "code": ""
            }
        })
    code = await picture.post_picture(data)
    return json({
            "isSuccess": "true",
            "msg": "",
            "data": {
                "code": code
            }
    })

@app.route("/code/check", methods=["GET", "POST"])
async def check_code(request, code):
    """检验集体照查看码"""
    msg = ""
    isSuccess = "true"
    code = request.json.get("code", None)
    if not await picture.check_code(code):
        isSuccess = "false"
        msg = "code is not exists."
    return json({
            "msg": msg,
            "isSuccess": isSuccess,
    })

@app.route("/user/find", methods=["POST"])
async def find_user_in_picture(request):
    """上传自拍，并在合照中识别自己"""
    return json({
            "isSuccess": "true",
            "msg": "",
            "data": {
                "url": "xxxx.com/xx.png"
            }
    })


if __name__ == "__main__":
    app.run(debug=True, access_log=True, host="localhost", port=8080)
