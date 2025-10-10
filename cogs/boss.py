from discord.ext import commands

class Boss(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="boss", description="Shows boss info")
    async def boss(self, ctx):
        await ctx.respond("Boss info goes here!")

def setup(bot):
    bot.add_cog(Boss(bot))
