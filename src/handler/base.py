import logging
import aioredis
import aiomysql

logger = logging.getLogger("web")

class Base:

    pool = None
    redis = None
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls, *args, **kwargs)
            logger.info(f"create {cls.__name__} singleton")
        return cls.instance

    async def __aenter__(self):
        logger.info(f"{self.__class__.__name__} acquire connect.")
        if self.pool is None:
            self.pool = await aiomysql.create_pool(
                host='127.0.0.1', port=3306, user='root', 
                password='DLsquad5@fudan',db='faceplus')
            logger.info(f"{self.__class__.__name__} create mysql pool.")
        if self.redis is None:
            self.redis = await aioredis.create_redis("redis://localhost")
            logger.info(f"{self.__class__.__name__} create redis client.")


    async def __aexit__(self, exc_type, exc_val, exc_tb):
        logger.info(f"{self.__class__.__name__} release connect.")
