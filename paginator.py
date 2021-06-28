import discord
import asyncio

async def paginate(ctx, bot, pages, method):
    def check(reaction, user):
        if method == "dpy":
            return user == ctx.message.author and str(reaction.emoji) == '◀' or '▶'
        else:
            return user == ctx.author and str(reaction.emoji) == '◀' or '▶'

    embed = discord.Embed(title=pages[0]["title"], description=pages[0]["description"], color=pages[0]["color"])

    try:
        thumbnail = pages[0]["thumbnail"]
        embed.set_thumbnail(url=thumbnail)
    except Exception:
        pass
    
    embed.set_footer(text=f"Page 1/{len(pages)}")

    msg = await ctx.send(embed=embed)
    await msg.add_reaction("◀")
    await msg.add_reaction("▶")

    await asyncio.sleep(0.5)
    
    page = 0

    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout= 60, check=check)
            if reaction.emoji == '◀' and page > 0:
                page -= 1
                embed = discord.Embed(title=pages[page]["title"], description=pages[page]["description"], color=pages[page]["color"])
                try:
                    thumbnail = pages[page]["thumbnail"]
                    embed.set_thumbnail(url=thumbnail)
                except Exception:
                    pass
                embed.set_footer(text=f"Page {page + 1}/{len(pages)}")
                await msg.edit(embed=embed)
                await msg.remove_reaction(reaction, user)
            if reaction.emoji == '▶' and page < len(pages) -1:
                page += 1
                embed = discord.Embed(title=pages[page]["title"], description=pages[page]["description"], color=pages[page]["color"])
                try:
                    thumbnail = pages[page]["thumbnail"]
                    embed.set_thumbnail(url=thumbnail)
                except Exception:
                    pass
                embed.set_footer(text=f"Page {page + 1}/{len(pages)}")
                await msg.edit(embed=embed)
                await msg.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            await msg.edit(content="Timed out.")
            await msg.clear_reactions()