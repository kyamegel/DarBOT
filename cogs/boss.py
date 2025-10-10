import discord
from discord import option
from discord.ext import commands
import datetime

class Boss(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.boss_data = {}  # Temporary placeholder for boss info

    boss = discord.SlashCommandGroup("boss", "Manage boss information")

    # /boss list [all/today/<day>]
    @boss.command(name="list", description="List bosses (all, today, or a specific day)")
    @option("day", description="Choose a day or 'all'", required=False)
    async def list(self, ctx, day: str = "all"):
        await ctx.defer()
        day = day.lower()
        if day == "all":
            bosses = ", ".join(self.boss_data.keys()) or "No bosses available."
        elif day == "today":
            weekday = datetime.datetime.now().strftime("%A")
            bosses = f"Bosses for {weekday}: TBD"  # Replace with DB query later
        else:
            bosses = f"Bosses for {day.capitalize()}: TBD"
        await ctx.respond(f"📜 **Boss List ({day})**\n{bosses}")

    # /boss add
    @boss.command(name="add", description="Add a new boss (Admin only)")
    async def add(self, ctx):
        if not await self._is_admin(ctx):
            return await ctx.respond("🚫 You don’t have permission to use this command.", ephemeral=True)

        await ctx.respond("📝 Please provide the boss name:")
        msg = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author)
        boss_name = msg.content

        self.boss_data[boss_name] = {"name": boss_name}
        await ctx.respond(f"✅ Boss **{boss_name}** added!")

    # /boss edit [boss_name]
    @boss.command(name="edit", description="Edit existing boss info (Admin only)")
    @option("boss_name", description="Select a boss to edit")
    async def edit(self, ctx, boss_name: str):
        if not await self._is_admin(ctx):
            return await ctx.respond("🚫 You don’t have permission to use this command.", ephemeral=True)
        if boss_name not in self.boss_data:
            return await ctx.respond("⚠️ Boss not found.")

        await ctx.respond(f"🛠️ Editing info for {boss_name}... (Feature in progress)")

    # /boss remove [boss_name]
    @boss.command(name="remove", description="Remove a boss (Admin only)")
    @option("boss_name", description="Select a boss to remove")
    async def remove(self, ctx, boss_name: str):
        if not await self._is_admin(ctx):
            return await ctx.respond("🚫 You don’t have permission to use this command.", ephemeral=True)
        if boss_name not in self.boss_data:
            return await ctx.respond("⚠️ Boss not found.")

        view = ConfirmView(ctx, boss_name, self)
        await ctx.respond(f"❗ Are you sure you want to remove **{boss_name}**?", view=view)

    # /boss info [boss_name]
    @boss.command(name="info", description="View info about a boss")
    @option("boss_name", description="Select a boss")
    async def info(self, ctx, boss_name: str):
        boss = self.boss_data.get(boss_name)
        if not boss:
            return await ctx.respond("⚠️ Boss not found.")
        await ctx.respond(f"📘 **Boss Info:**\nName: {boss_name}")

    # /boss tod [boss_name] [time_of_death]
    @boss.command(name="tod", description="Add boss time of death")
    @option("boss_name", description="Select a boss")
    @option("time_of_death", description="Enter time of death (HH:MM 24-hour format)")
    async def tod(self, ctx, boss_name: str, time_of_death: str):
        if boss_name not in self.boss_data:
            return await ctx.respond("⚠️ Boss not found.")

        self.boss_data[boss_name]["tod"] = time_of_death
        await ctx.respond(f"💀 Time of death for **{boss_name}** set to {time_of_death}")

    # /boss timer
    @boss.command(name="timer", description="Show boss respawn timers")
    async def timer(self, ctx):
        if not self.boss_data:
            return await ctx.respond("⏰ No boss data available.")
        response = "### Boss Timers:\n"
        for name, data in self.boss_data.items():
            if "tod" in data:
                # Example: calculate +4 hours respawn
                tod = datetime.datetime.strptime(data["tod"], "%H:%M")
                respawn = tod + datetime.timedelta(hours=4)
                timestamp = int(respawn.timestamp())
                response += f"- **{name}** respawns <t:{timestamp}:R>\n"
        await ctx.respond(response or "No timers set yet.")

    # Helper: admin role check
    async def _is_admin(self, ctx):
        role_names = [role.name for role in ctx.author.roles]
        return ADMIN_ROLE in role_names


# Confirmation view for /boss remove
class ConfirmView(discord.ui.View):
    def __init__(self, ctx, boss_name, cog):
        super().__init__(timeout=30)
        self.ctx = ctx
        self.boss_name = boss_name
        self.cog = cog

    @discord.ui.button(label="✅ Confirm", style=discord.ButtonStyle.green)
    async def confirm(self, button, interaction):
        del self.cog.boss_data[self.boss_name]
        await interaction.response.edit_message(content=f"🗑️ Boss **{self.boss_name}** removed.", view=None)

    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, button, interaction):
        await interaction.response.edit_message(content="❎ Action cancelled.", view=None)


def setup(bot):
    bot.add_cog(Boss(bot))