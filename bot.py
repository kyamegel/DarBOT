import discord
from discord.ext import commands
from dotenve import load_dotenv
import os

load dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
inents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
	print(f"✅ Logged in as {bot.user}")
    await bot.tree.sync()
    print("✅ Slash commands synced")

@bot.event
async def setup_hook():
    await bot.load_extension("cogs.boss")

bot.run(TOKEN)
