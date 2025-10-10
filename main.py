import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.slash_command(name="hello", description="say hello!")
async def hello(ctx):
    await ctx.respond("Hi!")

@bot.slash_command(name="goodbye", description="say goodbye!")
async def goodbye(ctx):
    await ctx.respond("Goodbye!")

bot.run('MTQyNTc5MTg4MjE0NzEzNTU0OA.G3wHOG.b7eJjU0RthL6TWZpw88lrT__i23Qc8E9yeeeKo')