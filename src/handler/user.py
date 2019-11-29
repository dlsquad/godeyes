from .base import Base

class User(Base):

    static_path = "./static/picture"

    async def insert_user(self, name: str, fname: str):
        sql = f"INSERT INTO user(name, fname) SELECT '{name}', '{fname}'
        FROM DUAL WHERE NOT EXISTS (SELECT id FROM user WHERE name='{name}')"
        async with self, self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql)
                await conn.commit()

    async def save_user(self, data: str):
        image_str, image_data = data.split(",", 1)
        image_suf = image_str.split(";")[0].split("/")[-1]
        image_bytes = base64.decodestring(image_data.strip().encode())
        code, fname = await self.insert_picture(image_suf)

        path = f"{self.static_path}/{fname}"
        async with aiofiles.open(path, "wb") as w:
            await w.write(image_bytes)
        return code

    async def find_user(self):
        pass




user = User()
