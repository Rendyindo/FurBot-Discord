import discord, cogs.utils.osuapi, os
from discord.ext import commands
import configparser
from configparser import SafeConfigParser

osuapi = cogs.utils.osuapi

try:
    import config
    osutoken = config.osutoken
except ImportError:
    pass

try:
    osutoken = os.environ['OSU_TOKEN']
except KeyError:
    pass

parser = SafeConfigParser()

class osu():
    """Everything osu! related

    Commands:
        catch      Gives osu! profile info for osu!catch mode.
        mania      Gives osu! profile info for osu!mania mode.
        osu        Gives osu! profile info for osu!standard mode.
        taiko      Gives osu! profile info for Taiko mode."""
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def osu(self, ctx, *arg):
        """Gives osu! profile info for osu!standard mode.

        Arguments:

        `*arg` : list  
        The username of the player.
        
        recent : command
        Replies most recent play of a user."""
        if arg:
            args = ' '.join(arg)
            username = str(args)
        else:
            try:
                userid = ctx.message.author.id
                parser.read('user.ini')
                username = parser.get(str(userid), "osu_username")
            except configparser.NoSectionError:
                await ctx.send("Please specify your username!")
        await osuapi.get_user(osutoken, username)
        user = osuapi.get_user
        embed=discord.Embed()
        embed.set_thumbnail(url="https://a.ppy.sh/{}_1.png".format(user.id))
        embed.add_field(name="Profile for {}".format(user.name), value="Mode: osu!standard", inline=False)
        embed.add_field(name="Player Info", value="Rank: `{}` | pp: `{}` | Accuracy: `{}` | Level: `{}`".format(user.pp_rank, round(user.pp), round(user.accuracy), round(user.level)), inline=False)
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    async def taiko(self, ctx, *arg):
        """Gives osu! profile info for Taiko mode.

        Arguments:

        `*arg` : list  
        The username of the player."""
        if arg:
            args = ' '.join(arg)
            username = str(args)
        else:
            try:
                userid = ctx.message.author.id
                parser.read('user.ini')
                username = parser.get(str(userid), "osu_username")
            except configparser.NoSectionError:
                await ctx.send("Please specify your username!")
        await osuapi.get_user(osutoken, username, mode=1)
        user = osuapi.get_user
        embed=discord.Embed()
        embed.set_thumbnail(url="https://a.ppy.sh/{}_1.png".format(user.id))
        embed.add_field(name="Profile for {}".format(user.name), value="Mode: Taiko", inline=False)
        embed.add_field(name="Player Info", value="Rank: `{}` | pp: `{}` | Accuracy: `{}` | Level: `{}`".format(user.pp_rank, round(user.pp), round(user.accuracy), round(user.level)), inline=False)
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    async def catch(self, ctx, *arg):
        """Gives osu! profile info for osu!catch mode.

        Arguments:

        `*arg` : list  
        The username of the player."""
        if arg:
            args = ' '.join(arg)
            username = str(args)
        else:
            try:
                userid = ctx.message.author.id
                parser.read('user.ini')
                username = parser.get(str(userid), "osu_username")
            except configparser.NoSectionError:
                await ctx.send("Please specify your username!")
        await osuapi.get_user(osutoken, username, mode=2)
        user = osuapi.get_user
        embed=discord.Embed()
        embed.set_thumbnail(url="https://a.ppy.sh/{}_1.png".format(user.id))
        embed.add_field(name="Profile for {}".format(user.name), value="Mode: osu!catch", inline=False)
        embed.add_field(name="Player Info", value="Rank: `{}` | pp: `{}` | Accuracy: `{}` | Level: `{}`".format(user.pp_rank, round(user.pp), round(user.accuracy), round(user.level)), inline=False)
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    async def mania(self, ctx, *arg):
        """Gives osu! profile info for osu!mania mode.

        Arguments:

        `*arg` : list  
        The username of the player."""
        if arg:
            args = ' '.join(arg)
            username = str(args)
        else:
            try:
                userid = ctx.message.author.id
                parser.read('user.ini')
                username = parser.get(str(userid), "osu_username")
            except configparser.NoSectionError:
                await ctx.send("Please specify your username!")
        await osuapi.get_user(osutoken, username, mode=3)
        user = osuapi.get_user
        embed=discord.Embed()
        embed.set_thumbnail(url="https://a.ppy.sh/{}_1.png".format(user.id))
        embed.add_field(name="Profile for {}".format(user.name), value="Mode: osu!mania", inline=False)
        embed.add_field(name="Player Info", value="Rank: `{}` | pp: `{}` | Accuracy: `{}` | Level: `{}`".format(user.pp_rank, round(user.pp), round(user.accuracy), round(user.level)), inline=False)
        await ctx.send(embed=embed)

    @osu.command()
    async def recent(self, ctx, *arg):
        """Sends info about last play of user

        Arguments:

        `*arg` : list  
        The username of the player."""
        if arg:
            args = ' '.join(arg)
            username = str(args)
        else:
            userid = ctx.message.author.id
            parser.read('user.ini')
            username = parser.get(str(userid), "osu_username")
        await osuapi.get_user_recent(osutoken, username, mode=0)
        play = osuapi.get_user_recent
        await osuapi.get_beatmaps(osutoken, beatmapid=play.beatmap_id)
        map = osuapi.get_beatmaps
        embed=discord.Embed(title="{} - {} [{}]".format(map.artist, map.title, map.version), url="https://osu.ppy.sh/b/{}".format(play.beatmap_id), description="Played by: {}".format(username), color=0x52b34d)
        embed.set_thumbnail(url="https://b.ppy.sh/thumb/{}l.jpg".format(str(map.set_id)))
        embed.add_field(name="Play info", value="Mods: {} | Score: {} | Accuracy {} | FC: {} | Combo: {}".format(''.join(play.enabled_mods), play.score, play.accuracy, play.FC, play.maxcombo), inline=False)
        embed.add_field(name="Date Played", value="{}".format(play.date), inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(osu(bot))