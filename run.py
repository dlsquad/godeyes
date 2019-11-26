"""
模型服务入口
"""

import os
import asyncio
import logging.config

from sanic import Sanic
from sanic import json

from src.main import main

CURRENT_WORK_DIR = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(os.path.join(CURRENT_WORK_DIR, "conf", "logging.conf"))


app = Sanic("myapp")

@app.route("/")
async def index():
    logger = logging.getLogger("sync")
    return json({"hello": "world!"})


@app.route("/find")
async def find():
    pass


if __name__ == "__main__":
    app.run(debug=True, access_log=True, host="localhost", port=80)
