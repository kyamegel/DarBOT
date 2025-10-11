import discord
from discord.ext import commands

# Replace with your admin role name
ADMIN_ROLE_NAME = "Admin"

class Boss(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bosses = {}  # Example in-memory data (replace with DB later)

    def is_admin(self, ctx):
        """Check if user has the admin role"""
        return discord.utils.get(ctx.author.roles, name=ADMIN_ROLE_NAME) is not None

    # === /boss parent command ===
    @commands.slash_command(name="boss", description="Manage or view boss information.")
    async def boss(self, ctx):
        pass  # parent command only

    # === /boss add ===
    @boss.subcommand(name="add", description="Add a new boss (admin only)")
    async def add(self, ctx, name: str, atk_type: str, monster_type: str, loot: str, spawn_place: str, spawn_cooldown: str):
        if not self.is_admin(ctx):
            await ctx.respond("❌ You don’t have permission to use this command.", ephemeral=True)
            return

        self.bosses[name.lower()] = {
            "name": name,
            "atk_type": atk_type,
            "monster_type": monster_type,
            "loot": loot,
            "spawn_place": spawn_place,
            "spawn_cooldown": spawn_cooldown
        }
        await ctx.respond(f"✅ Added boss **{name}** successfully!")

    # === /boss edit ===
    @boss.subcommand(name="edit", description="Edit boss info (admin only)")
    async def edit(self, ctx, name: str, field: str, value: str):
        if not self.is_admin(ctx):
            await ctx.respond("❌ You don’t have permission to use this command.", ephemeral=True)
            return

        boss = self.bosses.get(name.lower())
        if not boss:
            await ctx.respond("⚠️ Boss not found.")
            return

        if field not in boss:
            await ctx.respond("⚠️ Invalid field. Valid fields: atk_type, monster_type, loot, spawn_place, spawn_cooldown")
            return

        boss[field] = value
        await ctx.respond(f"✏️ Updated **{name}**'s `{field}` to `{value}`.")

    # === /boss remove ===
    @boss.subcommand(name="remove", description="Remove a boss (admin only)")
    async def remove(self, ctx, name: str):
        if not self.is_admin(ctx):
            await ctx.respond("❌ You don’t have permission to use this command.", ephemeral=True)
            return

        if name.lower() in self.bosses:
            del self.bosses[name.lower()]
            await ctx.respond(f"🗑️ Removed boss **{name}**.")
        else:
            await ctx.respond("⚠️ Boss not found.")

    # === /boss info ===
    @boss.subcommand(name="info", description="Show boss info")
    async def info(self, ctx, name: str):
        boss = self.bosses.get(name.lower())
        if not boss:
            await ctx.respond("⚠️ Boss not found.")
            return

        embed = discord.Embed(title=f"🐉 Boss Info: {boss['name']}", color=discord.Color.gold())
        embed.add_field(name="Attack Type", value=boss["atk_type"], inline=True)
        embed.add_field(name="Monster Type", value=boss["monster_type"], inline=True)
        embed.add_field(name="Loot", value=boss["loot"], inline=False)
        embed.add_field(name="Spawn Place", value=boss["spawn_place"], inline=False)
        embed.add_field(name="Spawn Cooldown", value=boss["spawn_cooldown"], inline=False)
        await ctx.respond(embed=embed)

    # === /boss list ===
    @boss.subcommand(name="list", description="Show boss list (all, today, or specific day)")
    async def list(self, ctx, filter: str = "all"):
        if not self.bosses:
            await ctx.respond("📭 No bosses added yet.")
            return

        embed = discord.Embed(title=f"📜 Boss List ({filter.title()})", color=discord.Color.blue())
        for boss in self.bosses.values():
            embed.add_field(name=boss["name"], value=f"{boss['monster_type']} | {boss['spawn_place']}", inline=False)
        await ctx.respond(embed=embed)

    # === /boss timer ===
    @boss.subcommand(name="timer", description="Show boss timer for selected boss")
    async def timer(self, ctx, name: str):
        boss = self.bosses.get(name.lower())
        if not boss:
            await ctx.respond("⚠️ Boss not found.")
            return

        await ctx.respond(f"⏰ **{boss['name']}** respawns every `{boss['spawn_cooldown']}` at `{boss['spawn_place']}`.")

    # === /boss help ===
    @boss.subcommand(name="help", description="Show all /boss subcommands")
    async def help(self, ctx):
        embed = discord.Embed(title="📘 /boss Command Help", color=discord.Color.green())
        embed.add_field(name="/boss add", value="Add a boss (Admin only)", inline=False)
        embed.add_field(name="/boss edit", value="Edit boss info (Admin only)", inline=False)
        embed.add_field(name="/boss remove", value="Remove a boss (Admin only)", inline=False)
        embed.add_field(name="/boss info [boss_name]", value="Show specific boss info", inline=False)
        embed.add_field(name="/boss list [all|today|<day>]", value="Show boss list", inline=False)
        embed.add_field(name="/boss timer [boss_name]", value="Show boss timer", inline=False)
        embed.add_field(name="/boss help", value="Show this help message", inline=False)
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Boss(bot))