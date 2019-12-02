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
from sanic_openapi import doc
from sanic.blueprints import Blueprint
from sanic.response import json, file_stream
from sanic_openapi import swagger_blueprint

from src.handler.user import user
from src.handler.picture import picture
from src.utils.data import Response, FormResponse

CURRENT_WORK_DIR = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(os.path.join(CURRENT_WORK_DIR, "conf", "logging.conf"))

PORT = 8080
HOST = "localhost"
URL = "http://localhost:8080"

app = Sanic("faceplus")
app.blueprint(swagger_blueprint)

app.static('/static', './static')
logger = logging.getLogger("web")

@app.route("/", methods=["GET"])
@doc.summary("欢迎使用faceplus系统")
@doc.produces(Response)
async def index(request):
    return json({
        "isSuccess": "true",
        "msg": "welcome to faceplus system!",
        "data": {
            "url": f"{URL}/static/picture/123456.jpg"
        }
    })

@app.route("/picture/post", methods=["POST"])
@doc.summary("上传集体照接口")
@doc.description("通过post上传json对象，其中pic字段对应图片base64的编码")
@doc.consumes({"pic": str}, location="body")
@doc.produces(Response)
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
@doc.summary("通过code获取集体照")
@doc.produces(Response)
async def get_picture(request, code: str):
    """获取原始合照"""
    if not await picture.check_code(code):
        return json({
            "isSuccess": "false",
            "msg": "code is not exists.",
            "data": {}
        })
    fpath = picture.get_picture(code)
    if not fpath:
        return json({
            "isSuccess": "false",
            "msg": "file is not exists.",
            "data": {}
        })
    return json({
        "isSuccess": "true",
        "msg": "",
        "data": {
            "url": URL+fpath
        }
    })

@app.route("/code/<code>", methods=["GET"])
@doc.summary("检测code码是否存在")
@doc.produces(Response)
async def check_code(request, code: str):
    """检验集体照查看码"""
    msg = ""
    isSuccess = "true"
    code = code.strip()
    if not await picture.check_code(code):
        isSuccess = "false"
        msg = f"code is not exists."
    return json({
        "msg": msg,
        "isSuccess": isSuccess,
        "data": {"code": code}
    })

@app.route("/user/find", methods=["POST"])
@doc.summary("若用户在合照中, 则在合照中找到用户")
@doc.description("入参为pic,code,name；返回url,position")
@doc.consumes({"pic": str,"code": str,"name": str}, location="body")
@doc.produces(Response)
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
    if not pos:
        return json({
            "isSuccess": "false",
            "msg": fname,
            "data": {}
        })
    url = f"{URL}/static/user/{fname}"
    pos = f"第{pos[0]}排 第{pos[1]}位"
    return json({
        "isSuccess": "true",
        "msg": "user is find in picture.",
        "data": {
            "url": url,
            "position": pos
        }
    })

@app.route("/user/generate", methods=["POST"])
@doc.summary("若用户不再合照中，则在在合照中生成用户")
@doc.description("入参为pic,code,name；返回url")
@doc.consumes({"pic": str,"code": str,"name": str}, location="body")
@doc.produces(Response)
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
    url = f"{URL}/static/user/{fname}"
    return json({
        "isSuccess": true,
        "msg": null,
        "data": {
            "url": url,
        }
    })

@app.route("/table/<code>", methods=["GET"])
@doc.summary("导出code对应合照的人名表单")
@doc.produces(FormResponse)
async def export_names_in_picture(request, code: str):
    """导出合照中的名单表"""
    if not await picture.check_code(code):
        return json({
            "isSuccess": "false",
            "msg": "code is not exists.",
            "data": {}
        })
    data = await picture.export_table(code)
    return json({
        "isSuccess": "true",
        "msg": "",
        "data": data
    })


if __name__ == "__main__":
    app.run(debug=True, access_log=True, host=HOST, port=PORT)
