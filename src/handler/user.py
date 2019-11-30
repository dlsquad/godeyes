from .base import Base
from .picture import picture
from src.utils import get_file_in_path
from src.utils.face_util import FaceUtil

class User(Base):

    static_path = "./static/picture"

    async def _insert_user(self, name: str):
        sql = f"""INSERT INTO user(name) SELECT '{name}' FROM DUAL 
        WHERE NOT EXISTS (SELECT id FROM user WHERE name='{name}')"""
        async with self, self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql)
                await conn.commit()

    async def post_user(self, name: str, pic: str):
        image_str, image_data = pic.split(",", 1)
        image_suf = image_str.split(";")[0].split("/")[-1]
        image_bytes = base64.decodestring(image_data.strip().encode())

        await self._insert_user(name)
        fname = ".".join([name, image_suf])
        path = f"{self.static_path}/{fname}"
        async with aiofiles.open(path, "wb") as w:
            await w.write(image_bytes)

    async def find_user(self, name: str, code: str) -> (str, tuple):
        """ 在表user_picture查找该人是否已近被识别过,
            若已识别过，则直接返回配置和加框的图片，
            若没有识别过，则调用模型识别并保存。
            Args:
                name: 用户姓名
                code: 合照编码
            Return:
                fname (string): 加框图片名
                position (Tuple(int, int)): 用户所处坐标
        """
        sql = f"""SELECT pos_x, pos_y FROM user_picture 
        WHERE user_id=(SELECT id FROM `user` WHERE name='{name}') AND 
        picture_id=(SELECT id FROM `picture` WHERE `code`='{code}');"""
        async with self, self.pool.acquire() as conn:
            async with cur.cursor() as cur:
                await cur.execute(sql)
                ret = await cur.fetchone()

        fname = f"{name}-{code}.jpg"
        fpath = f"{self.static_path}/{fname}"
        if ret: 
            gname = get_file_in_path(self.static_path, code)
            tname = get_file_in_path(picture,static_path, name)
            gpath = f"{self.static_path}/{gname}"
            tname = f"{picture.static_path}/{tname}"
            ret = await FaceUtil(tpath, gpath)(fpath)
            await self._insert_user_picture(name, code, *ret)

        return fpath.strip("."), ret

    async def _insert_user_picture(self, name: str, code: str, 
                                   pos_x: int, pos_y: int):
        sql = f""""""
        async with self, self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql)
                await conn.commit()

    async def generate_user(self, name, code):
        # TODO: 实现无中生有
        pass


user = User()
