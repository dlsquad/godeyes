from .base import Base

class User(Base):

    static_path = "./static/picture"

    async def insert_user(self, name: str, fname: str):
        sql = f"""INSERT INTO user(name, fname) SELECT '{name}', '{fname}'
        FROM DUAL WHERE NOT EXISTS (SELECT id FROM user WHERE name='{name}')"""
        async with self, self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql)
                await conn.commit()

    async def post_user(self, name: str, pic: str):
        image_str, image_data = pic.split(",", 1)
        image_suf = image_str.split(";")[0].split("/")[-1]
        image_bytes = base64.decodestring(image_data.strip().encode())

        fname = ".".join([name, image_suf])
        await self.insert_user(name, fname)
        path = f"{self.static_path}/{fname}"
        async with aiofiles.open(path, "wb") as w:
            await w.write(image_bytes)

    async def find_user(self, name, code) -> (str, tuple):
        """ 在表user_picture查找该人是否已近被识别过,
            若已识别过，则直接返回配置和加框的图片，
            若没有识别过，则调用模型识别并保存。
            Args:
                name: 用户姓名
                code: 合照编码
            return:
                fname: 加框图片名
                position: T
        """

        sql = f"""SELECT pos_x, pos_y, fname FROM user_picture 
        WHERE user_id=(SELECT id FROM `user` WHERE name='{name}') AND 
        picture_id=(SELECT id FROM `picture` WHERE `code`='{code}');"""
        async with self, self.pool.acquire() as conn:
            async with cur.cursor() as cur:
                await cur.execute(sql)
                ret = await cur.fetchone()

        if ret:
            return ret[2], (ret[0], ret[1])




user = User()
