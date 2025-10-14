import discord
from discord.ext import commands
from datetime import datetime, timedelta
from db import fetch

class Boss(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# Create the /boss command group
boss = discord.SlashCommandGroup("boss", "Manage or view boss-related commands")

# === /boss info ===
@boss.command(name="info", description="Display boss information from the database")
async def boss_info(ctx, name: str):
    # Query exactly as you specified
    query = """
        SELECT cooldown, spawn_time, spawn_day, timer, location,
               boss_type, boss_level
        FROM boss_timers AS a
        JOIN bosses AS b
        ON a.boss_name = b.boss_name
        WHERE a.boss_name = %s
    """
    rows = await fetch(query, name)

    if not rows:
        await ctx.respond(f"⚠️ No boss found with name **{name}**.")
        return

    boss = rows[0]

    cooldown = boss["cooldown"]
    spawn_time = boss["spawn_time"]
    spawn_day = boss["spawn_day"]
    timer = boss["timer"]
    location = boss["location"]
    boss_type = boss["boss_type"]
    boss_level = boss["boss_level"]

    # ✅ Compute "(x minutes ago)" or Discord timestamp
    time_ago = ""
    if isinstance(timer, datetime):
        unix_timestamp = int(timer.replace(tzinfo=timezone.utc).timestamp())
        time_ago = f"(<t:{unix_timestamp}:R>)"  # auto-updating relative time

    # ✅ Build Embed
    embed = discord.Embed(
        description=f"**{name}** Lv.{boss_level}",
        color=discord.Color.blurple()
    )

    embed.add_field(name="Boss Type", value=boss_type or "-", inline=True)
    embed.add_field(name="Spawn Location", value=location or "-", inline=True)
    embed.add_field(name="Cooldown", value=f"{cooldown} hours", inline=True)

    embed.add_field(
        name="\u200B",
        value=f"**SPAWN TIME:**\n{spawn_day}, {spawn_time} {time_ago}",
        inline=False
    )

    await ctx.respond(embed=embed)

# === /boss list ===
@boss.command(name="list", description="List all bosses or filter by day")
async def boss_list(ctx, filter: str):
    """Show boss list filtered by all, today, or specific day"""

    valid_days = ["sunday", "monday", "tuesday", "wednesday",
                  "thursday", "friday", "saturday"]

    # Normalize filter input
    filter_lower = filter.lower()

    # ✅ Get today's weekday (Philippine timezone)
    tz = pytz.timezone("Asia/Manila")
    today_name = datetime.now(tz).strftime("%A").lower()

    # ✅ Build query based on filter
    if filter_lower == "all":
        query = """
            SELECT a.boss_name, a.timer, a.spawn_day
            FROM boss_timers AS a
            JOIN bosses AS b ON a.boss_name = b.boss_name
            ORDER BY a.spawn_day, a.spawn_time
        """
        params = ()
    elif filter_lower == "today":
        query = """
            SELECT a.boss_name, a.timer, a.spawn_day
            FROM boss_timers AS a
            JOIN bosses AS b ON a.boss_name = b.boss_name
            WHERE LOWER(a.spawn_day) = %s
            ORDER BY a.spawn_time
        """
        params = (today_name,)
    elif filter_lower in valid_days:
        query = """
            SELECT a.boss_name, a.timer, a.spawn_day
            FROM boss_timers AS a
            JOIN bosses AS b ON a.boss_name = b.boss_name
            WHERE LOWER(a.spawn_day) = %s
            ORDER BY a.spawn_time
        """
        params = (filter_lower,)
    else:
        await ctx.respond("⚠️ Invalid filter. Use `all`, `today`, or a weekday name.")
        return

    # ✅ Fetch rows
    rows = await fetch(query, *params)

    if not rows:
        await ctx.respond("⚠️ No bosses found for that filter.")
        return

    # ✅ Format the boss list
    description = ""
    now = datetime.now(tz)
    for row in rows:
        name = row["boss_name"]
        timer = row["timer"]

        # Compute time left or relative time
        if isinstance(timer, datetime):
            unix_timestamp = int(timer.replace(tzinfo=timezone.utc).timestamp())
            description += f"• **{name}** spawning <t:{unix_timestamp}:R>\n"
        else:
            description += f"• **{name}** spawning soon\n"

    # ✅ Create embed
    title_map = {
        "all": "All Bosses",
        "today": f"Bosses Spawning Today ({today_name.title()})",
    }
    title = title_map.get(filter_lower, f"Bosses on {filter_lower.title()}")

    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.blurple()
    )

    await ctx.respond(embed=embed)

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