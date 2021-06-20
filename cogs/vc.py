from classes import YTDLSource

import discord
from discord.ext import commands
from discord.utils import get
import asyncio

class VC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # code here basically
    @commands.command(help="Plays audio from any YouTube video URL")
    async def play(self, ctx, *, url=None):
        channel = ctx.message.author.voice.channel
        if not channel:
            await ctx.send("You are not connected to a voice channel")
            return
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        if url != None:
            """Plays from a url (almost anything youtube_dl supports)"""

            async with ctx.typing():
                player = await YTDLSource.from_url(url,
                                                   loop=self.bot.loop,
                                                   stream=True)
                try:
                    ctx.voice_client.play(
                        player,
                        after=lambda e: print('Player error: %s' % e)
                        if e else None)
                except:
                    ctx.voice_client.stop()
                    ctx.voice_client.play(
                        player,
                        after=lambda e: print('Player error: %s' % e)
                        if e else None)

            url_thumb = f"https://i.ytimg.com/vi/{url.replace('https://www.youtube.com/watch?v=', '')}/maxresdefault.jpg"

            embed = discord.Embed(colour=discord.Colour.blue())
            embed.add_field(
                name="▶️ Now playing",
                value=
                f"[{player.title}]({url}) [<@{ctx.author.id}>]\nJoin VC <#{channel.id}>",
                inline=False)
            if "https://www.youtube.com/watch?v=" in url:
                embed.set_thumbnail(url=url_thumb)
            embed.set_footer(
                text=
                f"Requested by {ctx.author.name}#{ctx.author.discriminator}.")
            await ctx.send(embed=embed)
            while ctx.voice_client.is_playing() == True:
                await asyncio.sleep(1)
            await asyncio.sleep(1)
            await voice.disconnect()

            embed = discord.Embed(colour=discord.Colour.blue())
            embed.add_field(name="⏹️ Stopped and left",
                            value=f"<#{channel.id}>",
                            inline=False)
            embed.set_footer(
                text=
                f"Requested by {ctx.author.name}#{ctx.author.discriminator}.")
            await ctx.send(embed=embed)

        else:
            """Plays from a url (almost anything youtube_dl supports)"""
            url = "https://www.youtube.com/watch?v=KybAvaM3b90"
            async with ctx.typing():
                player = await YTDLSource.from_url(url,
                                                   loop=self.bot.loop,
                                                   stream=True)
                try:
                    ctx.voice_client.play(
                        player,
                        after=lambda e: print('Player error: %s' % e)
                        if e else None)
                except:
                    ctx.voice_client.stop()
                    ctx.voice_client.play(
                        player,
                        after=lambda e: print('Player error: %s' % e)
                        if e else None)

            url_thumb = f"https://i.ytimg.com/vi/{url.replace('https://www.youtube.com/watch?v=', '')}/maxresdefault.jpg"

            embed = discord.Embed(colour=discord.Colour.blue())
            embed.add_field(
                name="▶️ Now playing",
                value=
                f"[{player.title}]({url}) [<@{ctx.author.id}>]\nJoin VC <#{channel.id}>",
                inline=False)
            if "https://www.youtube.com/watch?v=" in url:
                embed.set_thumbnail(url=url_thumb)
            embed.set_footer(
                text=
                f"Requested by {ctx.author.name}#{ctx.author.discriminator}.")
            await ctx.send(embed=embed)
            while ctx.voice_client.is_playing() == True:
                await asyncio.sleep(1)
            await asyncio.sleep(1)
            await voice.disconnect()

            embed = discord.Embed(colour=discord.Colour.blue())
            embed.add_field(name="⏹️ Stopped and left",
                            value=f"<#{channel.id}>",
                            inline=False)
            embed.set_footer(
                text=
                f"Requested by {ctx.author.name}#{ctx.author.discriminator}.")
            await ctx.send(embed=embed)

    @commands.command(aliases=["leave"],
                      help="Stops playing in the VC and leaves")
    async def stop(self, ctx):
        try:
            channelid = ctx.message.author.voice.channel.id
            await ctx.voice_client.disconnect()
            embed = discord.Embed(colour=discord.Colour.blue())
            embed.add_field(name="⏹️ Stopped and left",
                            value=f"<#{channelid}>",
                            inline=False)
            embed.set_footer(
                text=
                f"Requested by {ctx.author.name}#{ctx.author.discriminator}.")
            await ctx.send(embed=embed)
        except:
            if ctx.author.voice == None:
                await ctx.send("You are not in a voice channel!")
            else:
                await ctx.send("The bot is not in a voice channel!")

def setup(bot):
    bot.add_cog(VC(bot))