import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def setup_hook():
    await bot.load_extension("cogs.boss")        # main boss command
    await bot.load_extension("cogs.boss_add")    # separate /boss add form

bot.run(TOKEN)
