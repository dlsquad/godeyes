import logging
import asyncio

logger = logging.getLogger("web")

class Base:

    pool = None
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls, *args, **kwargs)
        print(f"create {cls.__name__} singleton")
        logging.info(f"create {cls.__name__} singleton")
        return cls.instance

    async def __aenter__(self):
        logging.info(f"{cls.__name__} ")
        if self.pool is None:
            self.pool = await aiomysql.create_pool(
                host='127.0.0.1', port=3306, user='root', 
                password='DLsquad5@fudan',db='faceplus')
            logging.info(f"{cls.__name__} create connect.")

        # async with pool.acquire() as conn:
        #     async with conn.cursor() as cur:
        #         await cur.execute("SELECT 42;")
        #         print(cur.description)
        #         (r,) = await cur.fetchone()
        #         assert r == 42

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print(f"{cls.__name__} release connect.")
        logging.info(f"{cls.__name__} release connect.")
