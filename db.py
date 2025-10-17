import os
import aiomysql
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "db": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "autocommit": True,
}

# Connection pool (shared across your bot)
pool = None

async def create_pool():
    """Create a global aiomysql connection pool."""
    global pool
    if pool is None:
        try:
            pool = await aiomysql.create_pool(**DB_CONFIG)
            print("✅ MySQL connection pool created")
        except Exception as e:
            print(f"❌ Failed to create MySQL pool: {e}")

async def get_connection():
    """Get a connection from the pool."""
    global pool
    if pool is None:
        await create_pool()
    return await pool.acquire()

async def release_connection(conn):
    """Release a connection back to the pool."""
    global pool
    if pool and conn:
        pool.release(conn)

async def close_pool():
    """Close the connection pool."""
    global pool
    if pool:
        pool.close()
        await pool.wait_closed()
        print("🔌 MySQL pool closed")
