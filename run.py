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

PORT = 8080
HOST = "localhost"
URL = "http://localhost:8080"

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

@app.route("/picture/<code>", methods=["GET"])
async def get_picture(request, code):
    """获取原始合照"""
    if not await picture.check_code(code):
        return json({
            "isSuccess": "false",
            "msg": "code is not exists.",
            "data": {}
        })
    fpath = picture.get_picture(code)
    if not fname:
        return json({
            "isSuccess": "false",
            "msg": "file is not exists.",
            "data": {}
        })
    return json({
        "isSuccess": "true",
        "msg": "",
        "data": {
            "url": f"{URL}/{fpath}"
        }
    })

@app.route("/code/check", methods=["GET", "POST"])
async def check_code(request):
    """检验集体照查看码"""
    msg = ""
    isSuccess = "true"
    code = request.json.get("code", None)
    if not await picture.check_code(code):
        isSuccess = "false"
        msg = f"code is not exists."
    return json({
            "msg": msg,
            "isSuccess": isSuccess,
    })

@app.route("/user/find", methods=["POST"])
async def find_user_in_picture(request):
    """上传自拍，并在合照中识别自己"""
    pic = request.json.get("pic", None)
    name = request.json.get("name", None)
    code = request.json.get("code", None)
    if not (pic and name and code):
        return json({
                "isSuccess": "false",
                "msg": "parameter is not correct.",
                "data": {}
        })

    pic = pic.strip()
    name = name.strip()
    code = code.strip()
    await user.post_user(name, pic)
    fname, pos = await user.find_user(name, code)
    url = f"{URL}/static/user/fname"
    return json({
        "isSuccess": true,
        "msg": null,
        "data": {
            "url": url,
            "position": pos
        }
    })

@app.run("/user/generate", methods=["POST"])
async def generate_user_in_picture(request):
    """上传自拍，在集体照中生成出自己"""
    pic = request.json.get("pic", None)
    name = request.json.get("name", None)
    code = request.json.get("code", None)
    if not (pic and name and code):
        return json({
                "isSuccess": "false",
                "msg": "parameter is not correct.",
                "data": {}
        })

    pic = pic.strip()
    name = name.strip()
    code = code.strip()
    await user.post_user(name, pic)
    fname = await user.generate_user(name, code)
    url = f"{URL}/static/user/fname"
    return json({
        "isSuccess": true,
        "msg": null,
        "data": {
            "url": url,
        }
    })


if __name__ == "__main__":
    app.run(debug=True, access_log=True, host=HOST, port=PORT)
