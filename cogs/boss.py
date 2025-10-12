import discord
from discord.ext import commands

class Boss(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# Create the /boss command group
boss = discord.SlashCommandGroup("boss", "Manage or view boss-related commands")

class AddBossModal(discord.ui.Modal):
    def __init__(self, boss_name: str):
        super().__init__(title=f"Add Boss: {boss_name}")
        self.boss_name = boss_name

        self.spawn_time = discord.ui.InputText(
            label="Spawn Time",
            placeholder="<day>/cooldown, initial time"
            required=True
        )

        self.location = discord.ui.InputText(
            label="Spawn Location",
            placeholder="Enter spawn location",
            required=True
        )

        self.add_item(self.spawn_time)
        self.add_item(self.location)
    
    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="✅ Boss Added!"
            color=discord.Color.green()
        )
        embed.add_field(name="Name", value=self.boss_name, inline=False)
        embed.add_field(name="Spawn Time", value=self.spawn_time.value, inline=False)
        embed.add_field(name="Location", value=self.location.value, inline=False)

        await interaction.response.send_message(embed=embed)

# === /boss add ===
@boss.command(name="add", description="Add a new boss")
@discord.option(
    "name",
    description="The name of the boss to add",
    required=True
)
async def boss_add(ctx: discord.ApplicationContext, name: str):
    modal = AddBossModal(name)
    await ctx.send_modal(modal)

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