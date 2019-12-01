import asyncio
import aiomysql

from src.utils import gen_code

from pymysql.err import IntegrityError


async def main():
    pool = await aiomysql.create_pool(
        port=3306,
        user="root",
        db="faceplus",
        host="localhost",
        password='DLsquad5@fudan'
    )
    sql = "INSERT INTO picture(code) values('123420')"
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            while 1:
                try:
                    await cur.execute(sql)
                    await conn.commit()
                except IntegrityError:
                    print("catch!")
                    await asyncio.sleep(1)
                    continue
                print("execute success!")
                break
            print(cur.lastrowid)
            print(await cur.fetchone())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    
