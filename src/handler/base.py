import logging
import asyncio
import aiomysql

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
        print(f"{self.__class__.__name__} acquire connect.")
        logging.info(f"{self.__class__.__name__} acquire connect.")
        if self.pool is None:
            self.pool = await aiomysql.create_pool(
                host='127.0.0.1', port=3306, user='root', 
                password='DLsquad5@fudan',db='faceplus')
            print(f"{self.__class__.__name__} create connect.")
            logging.info(f"{self.__class__.__name__} create connect.")

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print(f"{self.__class__.__name__} release connect.")
        logging.info(f"{self.__class__.__name__} release connect.")
