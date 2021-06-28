import discord
from discord.ext import commands
import asyncio
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option


class Utility(commands.Cog, description="Utility commands"):
    def __init__(self, bot):
        self.bot = bot

    # code here basically
    @commands.command(help="Suggest something in <#856052541532143616>!")
    async def suggest(self, ctx, *, suggestion):
        channel = await self.bot.fetch_channel(856052541532143616)
        embed1 = discord.Embed(color=discord.Color.blurple())
        embed1.add_field(name=f"Suggestion from {ctx.author.display_name} ({ctx.author.name}#{ctx.author.discriminator}):", value=f"{suggestion}", inline=False)
        msg = await channel.send(embed=embed1)
        await msg.add_reaction("🔼")
        await msg.add_reaction("🔽")
        await ctx.message.add_reaction("✅")

    @cog_ext.cog_slash(name="suggest",
                       description="Suggest something in #suggestions!",
                       options=[
                        create_option(name="suggestion",
                         description="Enter your suggestion for the server here",
                         option_type=3,
                         required=True)
        ],
                       guild_ids=[764683397528158259])
    async def _suggest(self, ctx, suggestion):
        channel = await self.bot.fetch_channel(856052541532143616)
        embed1 = discord.Embed(color=discord.Color.blurple())
        embed1.add_field(name=f"Suggestion from {ctx.author.display_name} ({ctx.author.name}#{ctx.author.discriminator}):", value=f"{suggestion}", inline=False)
        msg = await channel.send(embed=embed1)
        await msg.add_reaction("🔼")
        await msg.add_reaction("🔽")
        await ctx.send("✅", hidden=True)


def setup(bot):
    bot.add_cog(Utility(bot))
