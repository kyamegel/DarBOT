import discord
from discord.ext import commands
from datetime import datetime, timedelta
import pytz
from db import fetch

boss = discord.SlashCommandGroup("boss", "/boss commands")

class Boss(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # /boss help
    @boss.command(name="help", description="Displays all /boss subcommands")
    async def help_command(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title="🧭 Boss Command Help",
            description="List of available `/boss` subcommands:",
            color=discord.Color.blurple()
        )
        embed.add_field(
            name="/boss add",
            value="Add a boss (admin only)",
            inline=False
        )
        embed.add_field(
            name="/boss edit [boss_name]",
            value="Edit boss info (admin only)",
            inline=False
        )
        embed.add_field(
            name="/boss remove [boss_name]",
            value="Remove a boss (admin only)",
            inline=False
        )
        embed.add_field(
            name="/boss info [boss_name]",
            value="Displays detailed information about a boss",
            inline=False
        )
        embed.add_field(
            name="/boss timer [boss_name]",
            value="Displays respawn timer of a boss",
            inline=False
        )
        embed.add_field(
            name="/boss list [all/today/day_input]",
            value="Lists bosses depending on filter option",
            inline=False
        )
        embed.add_field(
            name="/boss adjust [boss_name] [datetime]",
            value="Adjust the spawn time of a boss",
            inline=False
        )
        embed.add_field(
            name="/boss tod [boss_name] [time]",
            value="Set or update time of death for a boss",
            inline=False
        )

        await ctx.respond(embed=embed)

    # /boss info [boss_name]
    @boss.command(name="info", description="Displays info of the selected boss")
    async def info(self, ctx: discord.ApplicationContext, boss_name: str):
        await ctx.respond(f"📘 Placeholder: Displaying info for **{boss_name}**")

    # /boss timer [boss_name]
    @boss.command(name="timer", description="Displays timer of the selected boss")
    async def timer(self, ctx: discord.ApplicationContext, boss_name: str):
        await ctx.respond(f"⏱️ Placeholder: Timer for **{boss_name}** → `<t:0000000000:R>`")

    # /boss list [all/today/[day_input]]
    @boss.command(name="list", description="Displays list of bosses")
    async def list_bosses(self, ctx: discord.ApplicationContext, option: str):
        await ctx.respond(f"📋 Placeholder: Showing boss list for **{option}**")

    # /boss adjust [boss_name] [datetime]
    @boss.command(name="adjust", description="Adjust spawn time of a boss")
    async def adjust(self, ctx: discord.ApplicationContext, boss_name: str, datetime: str):
        await ctx.respond(f"⚙️ Placeholder: Adjusting spawn time of **{boss_name}** to `{datetime}`")

    # /boss tod [boss_name] [time]
    @boss.command(name="tod", description="Set or update boss time of death")
    async def tod(self, ctx: discord.ApplicationContext, boss_name: str, time: str):
        await ctx.respond(f"💀 Placeholder: Setting time of death for **{boss_name}** to `{time}`")


def setup(bot):
    bot.add_cog(Boss(bot))
    bot.add_application_command(boss)