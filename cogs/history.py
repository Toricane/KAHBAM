import discord
from discord.ext import commands
import asyncio
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option

from paginator import paginate

origin = {
    "title":
    "Origin",
    "description":
    "KAHBAM started as a Teams chat for people to play Kahoot! But that is just the origin of the name.\n\nThe original members were Siddarth and Rishit B, with Prajwal joining a day later.\n\nIt was a WhatsApp group which was called MineBlox, but soon we moved over to a Discord group DM. But this was just a group DM, not yet a server. Soon, our friend Nikhil joined us.\n\nThe KAHBAM Gaming server was made right after Prajwal's 13th birthday (10/10/2020), created by Vishnu. On that day, it was just Vishnu and Prajwal on the server. Soon, Rishit B, Siddarth, and Nikhil were also invited to the server. Also, people like Ahan, Rishit D, Sanjeet, Aarav, Rahul, Shlok, and more joined since they were at Prajwal's virtual birthday party. After all this, we started to invite people from the Teams chat onto the Discord server.",
    "color":
    discord.Colour.green(),
    "thumbnail":
    "https://images-ext-2.discordapp.net/external/BK5Zhjiv7HezIITmQu-ehGpoqCOKvY4Ntd7cXs_QGHU/%3Fsize%3D1024/https/cdn.discordapp.com/icons/764683397528158259/a_a39353e10b567e5091c25e5453e6380d.gif?width=498&height=498"
}

halloween = {
    "title":
    "Champion of Halloween Event",
    "description":
    """In October 2020, Prajwal had invited [Trick'ord Treat](https://support.discord.com/hc/en-us/articles/360057167253-Halloween-Bot-2020) bot made by Discord.
    
    Trick-or-treaters would show up once in a while randomly in a specific channel, and the first person to send either h!trick or h!treat (they change per trick-or-treater), they would get 1 item.

    Prajwal ended up winning and got the Champion of Halloween role, with 40+ items in his inventory, followed by Vishnu and Siddarth.""",
    "color":
    discord.Colour.orange(),
    "thumbnail":
    "https://cdn.discordapp.com/attachments/856008239513468959/856010510994374656/trickord.png"
}

embeds = [origin, halloween]


class Information(commands.Cog, description="Information about KAHBAM Gaming"):
    def __init__(self, bot):
        self.bot = bot

    # code here basically
    @commands.command(help="Learn about KAHBAM's history!")
    async def history(self, ctx):
        await paginate(ctx, self.bot, embeds, "dpy")

    @cog_ext.cog_slash(name="history",
                       description="Learn about KAHBAM's history!",
                       guild_ids=[764683397528158259])
    async def _history(self, ctx):
        await paginate(ctx, self.bot, embeds, "slash")
    

    @commands.command(help="")
    async def user(self, ctx, user: discord.Member):
        embed = discord.Embed(title=f"{user.display_name} ({user.name}#{user.discriminator})", color=discord.Colour.blurple())
        embed.set_image(url=f"{user.avatar_url}")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))
