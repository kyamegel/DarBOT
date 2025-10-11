import discord
from discord.ext import commands

# Enable default intents
intents = discord.Intents.default()

# Create bot instance
bot = commands.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    await bot.sync_commands()
    print("✅ Slash commands synced.")

# Load cogs
bot.load_extension("cogs.boss")

bot.run("YOUR_BOT_TOKEN_HERE")