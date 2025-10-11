import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Initialize bot
intents = discord.Intents.default()
bot = commands.Bot(intents=intents)

# Load the boss cog
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    await bot.sync_commands()
    print("✅ Slash commands synced.")

bot.load_extension("cogs.boss")

bot.run(TOKEN)