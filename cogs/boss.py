import discord
from discord.ext import commands
from datetime import datetime, timedelta
import re
import aiomysql
from dotenv import load_dotenv
import os

load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

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

    try:
        # Parse the time to ensure it's valid
        tod_obj = datetime.strptime(time_of_death, "%H:%M")

        # Connect to the database
        db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        cursor = db.cursor(dictionary=True)

        # 1️⃣ Fetch boss data
        cursor.execute("SELECT id, cooldown, spawn_type FROM bosses WHERE name = %s", (name,))
        boss = cursor.fetchone()

        if not boss:
            await ctx.respond(f"❌ Boss **{name}** not found in database.", ephemeral=True)
            cursor.close()
            db.close()
            return

        if boss["spawn_type"] == "fixed":
            await ctx.respond(f"⚠️ **{name}** has a fixed spawn and cannot be updated manually.", ephemeral=True)
            cursor.close()
            db.close()
            return

        # 2️⃣ Backup the current next_spawn
        cursor.execute("UPDATE boss_timers SET backup = next_spawn WHERE boss_id = %s", (boss["id"],))

        # 3️⃣ Compute next_spawn (TOD today + cooldown hours)
        now = datetime.now()  # current datetime (local)
        today_str = now.strftime("%Y-%m-%d")
        tod_datetime = datetime.strptime(f"{today_str} {time_of_death}", "%Y-%m-%d %H:%M")

        # Add cooldown hours
        next_spawn = tod_datetime + timedelta(hours=boss["cooldown"])

        # 4️⃣ Update boss_timers
        cursor.execute("""
            UPDATE boss_timers
            SET next_spawn = %s,
                last_update = NOW()
            WHERE boss_id = %s
        """, (next_spawn, boss["id"]))

        db.commit()

        # 5️⃣ Generate Discord timestamp <t:unix:R>
        unix_ts = int(next_spawn.timestamp())
        discord_timer = f"<t:{unix_ts}:R>"

        await ctx.respond(f"✅ TOD updated!\n**{name}** will respawn {discord_timer} *(local time: {next_spawn.strftime('%Y-%m-%d %H:%M')})*")

    except Exception as e:
        await ctx.respond(f"❌ Database error: {e}", ephemeral=True)

    finally:
        try:
            cursor.close()
            db.close()
        except:
            pass

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