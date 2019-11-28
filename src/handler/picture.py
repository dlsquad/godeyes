import asyncio
import aiofiles

from hashlab import md5
from pymysql.err import IntegrityError

from .base import Base
from utils import gen_code

class Picture(Base):

    def __init__(self):
        pass

    async def post_picture(self, data: str):
        image = base64.decodestring(data.encode())

        await self.insert_picture()

        async with aiofiles.open("./image/picture/chenenquan.jpg", "wb") as w:
            await w.write(image)
        
    async def get_picture(self, request, picture_id):
        pass

    async def put_picture(self, request, picture_id):
        pass

    async def insert_picture(self):
        sql = "INSERT INTO picture(code,) values({code}); "
        async with self, self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                while 1:
                    code = gen_code()
                    try:
                        await cur.execute(sql.format(code))
                    except IntegrityError:
                        logger.info(f"{code} is already exists.")
                        continue
                    break
                cur.



picture = Picture()
