import discord
from discord.ext import commands
from dotenve import load_dotenv
import os

load dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
inents.message_content = True

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

for filename in os.listdir("./cogs"):
	if filename.endswith(".py:):
		bot.load_extension(f"cogs.{filename[:-3]}")

@bot.event
async def on_ready():
	print(f"✅ Logged in as {bot.user}")
    await bot.tree.sync()
    print("✅ Slash commands synced")

bot.run(TOKEN)

