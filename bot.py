import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
ADMIN_ROLE = os.getenv("ADMIN_ROLE")

# Configure intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

# Create bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# Load cogs automatically
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"🔹 Loaded cog: {filename}")

asyncio.run(load_cogs())

# Run bot
bot.run(TOKEN)