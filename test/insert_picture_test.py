import asyncio
import aiomysql


async def main():
    pool = await aiomysql.create_pool(
        port=3306,
        user="root",
        db="faceplus",
        host="localhost",
        password='DLsquad5@fudan'
    )
    sql = "INSERT INTO picture(code) "
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:


    


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    
