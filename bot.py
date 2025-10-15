import os
import discord
from dotenv import load_dotenv
from db import create_pool, close_pool

# Load .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Use discord.Bot (not commands.Bot)
bot = discord.Bot(intents=discord.Intents.default())

@bot.event
async def on_ready():
    await create_pool()
    print(f"Logged in as {bot.user}")
    print("Syncing commands...")
    await bot.sync_commands()
    print("Commands synced")

@bot.event
async def on_shutdown():
    await close_pool()

# Load cogs
bot.load_extension("cogs.boss")

bot.run(TOKEN)
