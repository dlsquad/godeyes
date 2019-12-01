import base64
import aiofiles

from .base import Base
from .picture import picture
from src.utils import get_file_in_path
from src.utils.face_util import FaceUtil

class User(Base):

    static_path = "./static/user"

    async def _insert_user(self, name: str) -> int:
        sql = f"""INSERT INTO user(name) SELECT '{name}' FROM DUAL 
        WHERE NOT EXISTS (SELECT id FROM user WHERE name='{name}')"""
        async with self, self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql)
                await conn.commit()
                return cur.lastrowid

    async def post_user(self, name: str, pic: str):
        image_str, image_data = pic.split(",", 1)
        image_suf = image_str.split(";")[0].split("/")[-1]
        image_bytes = base64.decodestring(image_data.strip().encode())

        user_id = await self._insert_user(name)
        fname = ".".join([str(user_id), image_suf])
        path = f"{self.static_path}/{fname}"
        async with aiofiles.open(path, "wb") as w:
            await w.write(image_bytes)

    async def find_user(self, name: str, code: str) -> (str, tuple):
        """ 在表user_picture查找该人是否已近被识别过,
            若已识别过，则直接返回位置和加框的图片，
            若没有识别过，则调用模型识别并保存。
            Args:
                name: 用户姓名
                code: 合照编码
            Return:
                fname (string): 加框图片名
                position (Tuple(int, int)): 用户所处坐标
        """
        sql_1 = f"""SELECT id FROM `user` WHERE name='{name}';"""
        sql_2 = f"""SELECT id FROM `picture` WHERE code='{code}';"""
        sql_3 = """SELECT pos_x, pos_y FROM user_picture 
        WHERE user_id={user_id} AND picture_id={picture_id};"""
        async with self, self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql_1)
                user_info = await cur.fetchone()
                if not user_info:
                    return "name is not find.", None
                user_id = user_info[0]
                await cur.execute(sql_2)
                picture_info = await cur.fetchone()
                if not picture_info:
                    return "code is not find.", None
                picture_id = picture_info[0]
                sql_3 = sql_3.format(
                    user_id=user_id,
                    picture_id=picture_id
                )
                await cur.execute(sql_3)
                pos = await cur.fetchone()

        fname = f"{user_id}-{code}.jpg"
        fpath = f"{self.static_path}/{fname}"
        if not pos: 
            gname = get_file_in_path(picture.static_path, code)
            tname = get_file_in_path(self.static_path, str(user_id))
            gpath = f"{picture.static_path}/{gname}"
            tpath = f"{self.static_path}/{tname}"
            pos = await FaceUtil(tpath, gpath)(fpath)
            await self._insert_user_picture(user_id, picture_id, *pos)

        return fname, pos

    async def _insert_user_picture(self, user_id: int, picture_id: int, 
                                   pos_x: int, pos_y: int):
        sql = f"""INSERT INTO user_picture(user_id, picture_id,
        pos_x, pos_y) VALUES({user_id}, {picture_id}, {pos_x}, {pos_y});"""
        async with self, self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql)
                await conn.commit()

    async def generate_user(self, name, code):
        # TODO: 实现无中生有
        pass


user = User()
