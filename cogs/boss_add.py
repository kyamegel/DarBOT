import discord
from discord.ext import commands
from db.db_connect import execute_query

ADMIN_ROLE_NAME = "Admin"

class BossAddModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="📝 Add New Boss")

        # Form fields for each column in the `bosses` table
        self.boss_name = discord.ui.InputText(label="Boss Name", placeholder="e.g. Abyss Lord", required=True)
        self.boss_level = discord.ui.InputText(label="Boss Level", placeholder="e.g. 120", required=True)
        self.boss_type = discord.ui.InputText(label="Boss Type", placeholder="e.g. Raid / Field / Dungeon", required=True)
        self.spawn_type = discord.ui.InputText(label="Spawn Type", placeholder="e.g. Timed / Manual / Random", required=True)
        self.armor_type = discord.ui.InputText(label="Armor Type", placeholder="e.g. Physical / Magical", required=True)
        self.place = discord.ui.InputText(label="Place", placeholder="e.g. Dark Cave", required=True)

        # Add inputs to the modal
        for field in [self.boss_name, self.boss_level, self.boss_type, self.spawn_type, self.armor_type, self.place]:
            self.add_item(field)

    async def callback(self, interaction: discord.Interaction):
        """Runs when the user submits the form"""
        name = self.boss_name.value.strip()
        level = self.boss_level.value.strip()
        btype = self.boss_type.value.strip()
        stype = self.spawn_type.value.strip()
        atype = self.armor_type.value.strip()
        place = self.place.value.strip()

        # Insert data into MySQL
        query = """
            INSERT INTO bosses (boss_name, boss_level, boss_type, spawn_type, armor_type, place)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        execute_query(query, (name, level, btype, stype, atype, place))

        embed = discord.Embed(title="✅ Boss Added Successfully", color=discord.Color.green())
        embed.add_field(name="Boss Name", value=name, inline=False)
        embed.add_field(name="Level", value=level, inline=True)
        embed.add_field(name="Type", value=btype, inline=True)
        embed.add_field(name="Spawn Type", value=stype, inline=True)
        embed.add_field(name="Armor Type", value=atype, inline=True)
        embed.add_field(name="Place", value=place, inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)


class BossAdd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ BossAdd Cog loaded")

    @commands.slash_command(name="boss_add_internal", description="Internal boss add trigger (hidden)")
    async def boss_add_internal(self, ctx):
        """This hidden command allows other cogs to access this subcommand."""
        pass

    # Hook this into /boss add
    @commands.slash_command(name="boss_add_form", description="Add a boss using form (admin only)")
    async def boss_add_form(self, ctx):
        """This will be called by the main /boss add subcommand in boss.py"""
        if not discord.utils.get(ctx.author.roles, name=ADMIN_ROLE_NAME):
            await ctx.respond("❌ You don’t have permission to use this command.", ephemeral=True)
            return

        modal = BossAddModal()
        await ctx.send_modal(modal)


def setup(bot):
    bot.add_cog(BossAdd(bot))