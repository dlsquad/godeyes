import typing
import base64
import random
import logging
import asyncio
import aiofiles
from typing import List
from pymysql.err import IntegrityError

from .base import Base
from src.utils.face_util import FaceUtil
from src.utils.gen_loc import BBoxesTool
from src.utils import gen_code, get_file_in_path

logger = logging.getLogger("web")


class Picture(Base):

    static_path = "./static/picture"

    async def check_code(self, code: str) -> bool:
        sql = f"SELECT code FROM picture WHERE code='{code}'"
        async with self, self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await conn.commit()
                await cur.execute(sql)
                result = await cur.fetchone()
                return bool(result)

    async def post_picture(self, data: str) -> str:
        image_str, image_data = data.split(",", 1)
        image_suf = image_str.split(";")[0].split("/")[-1]
        image_bytes = base64.decodestring(image_data.strip().encode())

        code = await self._insert_picture()
        path = f"{self.static_path}/{code}.{image_suf}"
        async with aiofiles.open(path, "wb") as w:
            await w.write(image_bytes)

        channels = await self.redis.pubsub_channels('channel:*')
        await self.redis.publish(random.choice(channels), path)
        return code

    def get_picture(self, code: str) -> str:
        fname = get_file_in_path(self.static_path, code)
        return f"{self.static_path.strip('.')}/{fname}"

    async def _insert_picture(self) -> str:
        sql = "INSERT INTO picture(code) values('{code}');"
        async with self, self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                while 1:
                    code = gen_code()
                    try:
                        await cur.execute(sql.format(
                            code=code,
                        ))
                        await conn.commit()
                    except IntegrityError:
                        logger.warn(f"{code} is already exists.")
                        continue
                    logger.info(f"{code} have inserted.")
                    return code

    async def export_table(self, code: str) -> List[List[str]]:
        """ 导出名单表
        Args:
            code: 合照查看码
        Return:
            [["", "jake",...], ...] max_row * max_col 的二维列表
        """
        table_info = await FaceUtil.get_table_info(code)
        if not table_info:
            return f"there is no faces in picture {code}"
        user_info = await self._get_user_picture(code)
        if not user_info:
            return f"there is no recongnized user in picture {code}"

        max_row, max_col = max(table_info.keys()), max(table_info.values())
        data = [["" for _ in range(max_col)] for _ in range(max_row)] # 初始化二维列表
        # 其中(max_col-table_info.get(row))//2为居中偏移量, python3.8支持以下表达式
        # _ = [data[row-1][col-1+(max_col-table_info.get(row))//2] := name for name, row, col in user_info]

        for name, row, col in user_info:
            offset = (max_col - table_info.get(row)) // 2
            data[row-1][col-1+offset] = name

        return data

    async def _get_user_picture(self, code: str):
        sql = f"""SELECT u.name,t.pos_x,t.pos_y FROM (SELECT user_id, pos_x, pos_y 
        FROM user_picture WHERE picture_id=(SELECT id FROM picture WHERE code='{code}')) 
        t JOIN user u ON u.id=t.user_id"""
        async with self, self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await conn.commit()
                await cur.execute(sql)
                user_info = await cur.fetchall()
                return user_info


picture = Picture()
