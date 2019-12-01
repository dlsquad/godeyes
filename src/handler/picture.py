import base64
import logging
import asyncio
import aiofiles
from pymysql.err import IntegrityError

from .base import Base
from src.utils import gen_code, get_file_in_path

logger = logging.getLogger("web")


class Picture(Base):

    static_path = "./static/picture"

    async def check_code(self, code: str) -> bool:
        sql = f"SELECT code FROM picture WHERE code={code}"
        async with self, self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql)
                return bool(await cur.fetchone())

    async def post_picture(self, data: str) -> str:
        image_str, image_data = data.split(",", 1)
        image_suf = image_str.split(";")[0].split("/")[-1]
        image_bytes = base64.decodestring(image_data.strip().encode())

        code = await self._insert_picture()
        path = f"{self.static_path}/{code}.{image_suf}"
        async with aiofiles.open(path, "wb") as w:
            await w.write(image_bytes)
        return code

    def get_picture(self, code: str) -> str:
        fname = get_file_in_path(self.static_path, code)
        return f"{self.static_path.strip('.'}/{fname}"

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


picture = Picture()
