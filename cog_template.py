import discord
from discord.ext import commands
import asyncio
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option


class cog_name(commands.Cog, description="description"):
    def __init__(self, bot):
        self.bot = bot

    # code here basically
    @commands.command(help="help")
    async def command_name(ctx):
        await ctx.send("test")

    @cog_ext.cog_slash(name="command_name",
                       description="command_description",
                       guild_ids=[764683397528158259])
    async def _command_name(ctx):
        await ctx.send("test")


def setup(bot):
    bot.add_cog(cog_name(bot))
