import discord
from discord.ext import commands
from datetime import datetime
import re

class Boss(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# Create the /boss command group
boss = discord.SlashCommandGroup("boss", "Manage or view boss-related commands")

# === /boss info ===
@boss.command(name="info", description="Show boss info")
async def boss_info(ctx, boss_name: str = None):
    await ctx.respond(f"🧩 You used `/boss info` (boss: {boss_name})")

# === /boss list ===
@boss.command(name="list", description="List all bosses")
async def boss_list(ctx, filter: str = "all"):
    await ctx.respond(f"🧩 You used `/boss list` (filter: {filter})")

# === /boss tod [name] [time_of_death] ===
@boss.command(name="tod", description="Update the time of death for a boss")
@discord.option("name", description="The name of the boss", required=True)
@discord.option("time_of_death", description="Time of death (HH:mm 24-hour format)", required=True)
async def boss_tod(ctx: discord.ApplicationContext, name: str, time_of_death: str):
    # Validate HH:mm format (24-hour)
    if not re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", time_of_death):
        await ctx.respond(
            "❌ Invalid time format! Please use **HH:mm** in 24-hour format (e.g. `14:30`).",
            ephemeral=True
        )
        return

    # Optional: convert to datetime for internal processing
    try:
        datetime.strptime(time_of_death, "%H:%M")
    except ValueError:
        await ctx.respond("❌ Invalid time. Please check your input.", ephemeral=True)
        return

    # Respond with confirmation
    await ctx.respond(f"✅ TOD: **{time_of_death}** for **{name}** has been updated.")

# === /boss timer ===
@boss.command(name="timer", description="Show boss timer")
async def boss_timer(ctx, boss_name: str = None):
    await ctx.respond(f"🧩 You used `/boss timer` (boss: {boss_name})")

# === /boss help ===
@boss.command(name="help", description="Show boss command help")
async def boss_help(ctx):
    embed = discord.Embed(
        title="👹 **Boss Commands** 👹",
        description="Here's a list of all available `/boss` subcommands:",
        color=discord.Color.red()
    )

    embed.add_field(name="**``/boss add``**", value="Adds a boss to the list.", inline=False)
    embed.add_field(name="**``/boss edit [boss_name]``**", value="Edit the information of the chosen boss.", inline=False)
    embed.add_field(name="**``/boss remove``**", value="Remove the chosen boss.", inline=False)
    embed.add_field(name="**``/boss info [boss_name]``**", value="Displays the chosen boss' information.", inline=False)
    embed.add_field(name="**``/boss list [all/today/<day>] ``**", value="Displays a list of bosses.\n -# options: all, today, day", inline=False)
    embed.add_field(name="**``/boss timer [boss_name]``**", value="Displays the chosen boss' timer.", inline=False)
    embed.add_field(name="**``/boss tod [name] [time_of_death]``**", value="Add time of death to the selected boss", inline=False)

    embed.set_footer(text="Use these commands to manage or view boss information.")
    await ctx.respond(embed=embed)

# Register the group with the bot
def setup(bot):
    bot.add_cog(Boss(bot))
    bot.add_application_command(boss)