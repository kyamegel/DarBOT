import os
import discord
from dotenv import load_dotenv

# Load .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Use discord.Bot (not commands.Bot)
bot = discord.Bot(intents=discord.Intents.default())

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    print("🔁 Syncing commands...")
    await bot.sync_commands()
    print("✅ Commands synced!")
    print("DEBUG DB_PASS =", os.getenv("DB_PASS"))

# Load cogs
bot.load_extension("cogs.boss")

bot.run(TOKEN)
