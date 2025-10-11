import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents)

# Load cogs
bot.load_extension("boss")  # make sure this matches your filename (boss.py)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    await bot.sync_commands()  # <-- important! sync all slash commands
    print("✅ Slash commands synced.")

bot.run(os.getenv("DISCORD_TOKEN"))
