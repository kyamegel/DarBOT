import aiomysql
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Read database credentials
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Global connection pool
pool = None


async def create_pool():
    """Initialize the global MySQL connection pool."""
    global pool
    if pool is None:
        pool = await aiomysql.create_pool(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            db=DB_NAME,
            autocommit=True,
            minsize=1,
            maxsize=5
        )
        print("✅ Connected to MySQL database pool.")


async def close_pool():
    """Close the MySQL connection pool."""
    global pool
    if pool:
        pool.close()
        await pool.wait_closed()
        print("🔒 Closed MySQL connection pool.")


async def fetch(query: str, *params):
    """Run SELECT queries and return results."""
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(query, params)
            return await cur.fetchall()


async def execute(query: str, *params):
    """Run INSERT, UPDATE, DELETE queries."""
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, params)
            await conn.commit()
            return cur.lastrowid