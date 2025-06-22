import asyncpg
import os

async def get_db_pool():
    return await asyncpg.create_pool(dsn=os.getenv("DATABASE_URL"))

async def save_summary_to_db(request_data, summary: str):
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO summaries (source, name, typ, content, timestamp, status, summary)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
        """, request_data["source"], request_data["name"], request_data["typ"],
             request_data["content"], request_data["timestamp"], request_data["status"],
             summary)
