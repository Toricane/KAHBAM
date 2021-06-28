import os
import discord
from discord.ext import commands, tasks
from keep_alive import keep_alive
from itertools import cycle
from discord_slash import SlashCommand
from discord.flags import Intents
import re, ast, inspect
import sys
import datetime
import asyncio, youtube_dl
from discord.utils import get
import requests
from discord.errors import Forbidden
from pretty_help import PrettyHelp

ending_note = "Type kb.help command for more info on a command.\nYou can also type kb.help category for more info on a category.\nCategories are cAsE sEnSiTiVe.\n\nThe bot also has / commands, try them out!"

bot = commands.Bot(command_prefix="kb.",
                   case_insensitive=True,
                   help_command=PrettyHelp(color=discord.Colour.blurple(),
                                           page_left="◀️",
                                           page_right="▶️",
                                           remove="❌",
                                           ending_note=ending_note))
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    change_status.start()
    print(f'We have logged in as {bot.user}')
    timestamp = datetime.datetime.now()
    print(timestamp.strftime(r"%A, %b %d, %Y, %I:%M %p UTC"))


status = cycle(['kb.help', 'ping @Prajwal for help!'])


@bot.event
async def on_message(message):
    await bot.process_commands(message)


@tasks.loop(seconds=15)
async def change_status():
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name=next(status)))


@bot.command(aliases=["l"])
async def load(ctx, extension=None):
    if ctx.author.id == 721093211577385020:
        if extension == None:
            try:
                for filename in os.listdir("./cogs"):
                    if filename.endswith(".py"):
                        bot.load_extension(f"cogs.{filename[:-3]}")
                await ctx.send("Successfully loaded all extensions.")
            except Exception as e:
                await ctx.send(f"{e}")
        else:
            bot.load_extension(f"cogs.{extension}")
            await ctx.send(f"Successfully loaded `cogs/{extension}.py`")
    else:
        await ctx.message.add_reaction('<:no:828741445069963274>')


@bot.command(aliases=["ul"])
async def unload(ctx, extension=None):
    if ctx.author.id == 721093211577385020:
        if extension == None:
            try:
                for filename in os.listdir("./cogs"):
                    if filename.endswith(".py"):
                        bot.unload_extension(f"cogs.{filename[:-3]}")
                await ctx.send("Successfully unloaded all extensions.")
            except Exception as e:
                await ctx.send(f"{e}")
        else:
            bot.unload_extension(f"cogs.{extension}")
            await ctx.send(f"Successfully unloaded `cogs/{extension}.py`")
    else:
        await ctx.message.add_reaction('<:no:828741445069963274>')


@bot.command(aliases=["rl"])
async def reload(ctx, extension=None):
    if ctx.author.id == 721093211577385020:
        if extension == None:
            try:
                for filename in os.listdir("./cogs"):
                    if filename.endswith(".py"):
                        bot.unload_extension(f"cogs.{filename[:-3]}")
            except Exception as e:
                await ctx.send(f"{e}")
            try:
                for filename in os.listdir("./cogs"):
                    if filename.endswith(".py"):
                        bot.load_extension(f"cogs.{filename[:-3]}")
            except Exception as e:
                await ctx.send(f"{e}")
            await ctx.send("Successfully reloaded all extensions.")
        else:
            try:
                bot.unload_extension(f"cogs.{extension}")
                bot.load_extension(f"cogs.{extension}")
                await ctx.send(f"Successfully reloaded `cogs/{extension}.py`")
            except Exception as e:
                await ctx.send(f"{e}")
    else:
        await ctx.message.add_reaction('<:no:828741445069963274>')


@bot.command(description="Restarts the bot")
async def restart(ctx):
    if ctx.author.id == 721093211577385020:
        await ctx.message.add_reaction('🆗')
        os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        await ctx.message.add_reaction('❌')


@bot.command()
async def embed(ctx):
    embed1 = discord.Embed()
    embed1.add_field(
        name="List of candidates 1:",
        value=
        "- Evan G [speech](https://discord.com/channels/764683397528158259/855223035144306719/855223190828744756)\n- BTS (Meshroon, and Jovan/Ahan/Andrea/Vishnu as Mods) [speech](https://discord.com/channels/764683397528158259/855223035144306719/855252145182605312), [speech](https://discord.com/channels/764683397528158259/855223035144306719/855223765213380659), [speech](https://discord.com/channels/764683397528158259/855223035144306719/855224235257888789), [speech](https://discord.com/channels/764683397528158259/855223035144306719/855224416584466483), [speech](https://discord.com/channels/764683397528158259/855223035144306719/855254716597272616), [speech](https://discord.com/channels/764683397528158259/855223035144306719/855524465973395486), and [speech](https://discord.com/channels/764683397528158259/855223035144306719/855293473716043826)",
        inline=False)
    embed1.add_field(
        name="List of candidates 2:",
        value=
        "- Leo [speech](https://discord.com/channels/764683397528158259/855223035144306719/855223836249554945)\n- Prajwal [speech](https://discord.com/channels/764683397528158259/855223035144306719/855233289895673886) and [speech](https://discord.com/channels/764683397528158259/855223035144306719/855261942720757760)\n- Sid [speech](https://discord.com/channels/764683397528158259/855223035144306719/855311123511640086)\n- Rishit B [speech](https://discord.com/channels/764683397528158259/855223035144306719/855329086746656789) and [speech](https://discord.com/channels/764683397528158259/855223035144306719/855331043455926302)\n- Plague Master [speech](https://discord.com/channels/764683397528158259/855223035144306719/855519344946446336)\n- Rahul [speech](https://discord.com/channels/764683397528158259/855223035144306719/855634703804530718)",
        inline=False)
    await ctx.send(embed=embed1)


def source(o):
    s = inspect.getsource(o).split("\n")
    indent = len(s[0]) - len(s[0].lstrip())
    return "\n".join(i[indent:] for i in s)


source_ = source(discord.gateway.DiscordWebSocket.identify)
source_ = re.sub(r'([\'"]\$browser[\'"]:\s?[\'"]).+([\'"])',
                 r"\1Discord Android\2", source_)
m = ast.parse(source_)

loc = {}
exec(compile(m, "<string>", "exec"), discord.gateway.__dict__, loc)

discord.gateway.DiscordWebSocket.identify = loc["identify"]

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.load_extension("jishaku")

keep_alive()
bot.run(os.getenv('TOKEN'))
