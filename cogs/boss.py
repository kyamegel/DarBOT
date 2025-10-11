import discord
from discord.ext import commands

class Boss(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# Create the /boss command group
boss = discord.SlashCommandGroup("boss", "Manage or view boss-related commands")

# === /boss add ===
@boss.command(name="add", description="Add a new boss")
async def boss_add(ctx):
    await ctx.respond("🧩 You used `/boss add`")

# === /boss edit ===
@boss.command(name="edit", description="Edit a boss")
async def boss_edit(ctx, boss_name: str = None):
    await ctx.respond(f"🧩 You used `/boss edit` (boss: {boss_name})")

# === /boss remove ===
@boss.command(name="remove", description="Remove a boss")
async def boss_remove(ctx, boss_name: str = None):
    await ctx.respond(f"🧩 You used `/boss remove` (boss: {boss_name})")

# === /boss info ===
@boss.command(name="info", description="Show boss info")
async def boss_info(ctx, boss_name: str = None):
    await ctx.respond(f"🧩 You used `/boss info` (boss: {boss_name})")

# === /boss list ===
@boss.command(name="list", description="List all bosses")
async def boss_list(ctx, filter: str = "all"):
    await ctx.respond(f"🧩 You used `/boss list` (filter: {filter})")

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

    embed.set_footer(text="Use these commands to manage or view boss information.")
    await ctx.respond(embed=embed)

# Register the group with the bot
def setup(bot):
    bot.add_cog(Boss(bot))
    bot.add_application_command(boss)