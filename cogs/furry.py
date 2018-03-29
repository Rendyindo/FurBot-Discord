import discord
from discord.ext import commands
import random, asyncio, cogs.utils.eapi, cogs.utils.sfapi, cogs.utils.inkbunnyapi, os, cogs.utils.fapi
from urllib.parse import urlparse

try:
    import config
    inkpassword = config.inkpassword
    inkusername = config.inkusername
except:
    pass

try:
    inkpassword = os.environ['INK_PASSWORD']
    inkusername = os.environ['INK_USERNAME']
except:
    pass

processapi = cogs.utils.eapi.processapi
processshowapi = cogs.utils.eapi.processshowapi
search = cogs.utils.sfapi.search

class ResultNotFound(Exception):
    """Used if ResultNotFound is triggered by e* API."""
    pass

class InvalidHTTPResponse(Exception):
    """Used if non-200 HTTP Response got from server."""
    pass

class Furry():
    """What every furries need.

    Commands:
        e621       Searches e621 with given queries.
        e926       Searches e926 with given queries.
        inkbunny   Searches InkBunny with given queries.
        randompick Output random result from e621/e926.  
        show       Show a post from e621/e926 with given post ID
        sofurry    Searches SoFurry with given queries."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def e621(self, ctx, *args):
        """Searches e621 with given queries.

        Arguments:

        `*args` : list  
        The quer(y/ies)"""
        if not isinstance(ctx.channel, discord.DMChannel):
            if not isinstance(ctx.channel, discord.GroupChannel):
                if not ctx.channel.is_nsfw():
                    await ctx.send("Cannot be used in non-NSFW channels!")
                    return
        args = ' '.join(args)
        args = str(args)
        netloc = "e621"
        print("------")
        print("Got command with args: " + args)
        if "order:score_asc" in args:
            await ctx.send("I'm not going to fall into that one, silly~")
            return
        if "score:" in args:
            apilink = 'https://e621.net/post/index.json?tags=' + args + '&limit=320'
        else:
            apilink = 'https://e621.net/post/index.json?tags=' + args + ' score:>25&limit=320'
        try:
            await processapi(apilink)
        except ResultNotFound:
            await ctx.send("Result not found!")
            return
        except InvalidHTTPResponse:
            await ctx.send("We're getting invalid response from the API, please try again later!")
            return
        await ctx.send("""Post link: `https://""" + netloc + """.net/post/show/""" + processapi.imgid + """/`\r\nArtist: `""" + processapi.imgartist + """`\r\nSource: `""" + processapi.imgsource + """`\r\nRating: """ + processapi.imgrating + """\r\nTags: `""" + processapi.imgtags + """` ...and more\r\nImage link: """ + processapi.file_link)
        
    @commands.command(pass_context=True)
    async def e926(self, ctx, *args):
        """Searches e926 with given queries.

        Arguments:

        `*args` : list  
        The quer(y/ies)"""
        args = ' '.join(args)
        args = str(args)
        netloc = "e926"
        print("------")
        print("Got command with args: " + args)
        if "order:score_asc" in args:
            await ctx.send("I'm not going to fall into that one, silly~")
            return
        if "score:" in args:
            apilink = 'https://e926.net/post/index.json?tags=' + args + '&limit=320'
        else:
            apilink = 'https://e926.net/post/index.json?tags=' + args + ' score:>25&limit=320'
        try:
            await processapi(apilink)
        except ResultNotFound:
            await ctx.send("Result not found!")
            return
        except InvalidHTTPResponse:
            await ctx.send("We're getting invalid response from the API, please try again later!")
            return
        await ctx.send("""Post link: `https://""" + netloc + """.net/post/show/""" + processapi.imgid + """/`\r\nArtist: `""" + processapi.imgartist + """`\r\nSource: `""" + processapi.imgsource + """`\r\nRating: """ + processapi.imgrating + """\r\nTags: `""" + processapi.imgtags + """` ...and more\r\nImage link: """ + processapi.file_link)

    @commands.command(pass_context=True)
    async def show(self, ctx, arg):
        """Show a post from e621/e926 with given post ID

        Arguments:

        `arg` : int  
        The post ID"""
        print("------")
        arg = str(arg)
        print("Got command with arg: " + arg)
        apilink = 'https://e621.net/post/show.json?id=' + arg
        try:
            await processshowapi(apilink)
        except ResultNotFound:
            await ctx.send("Result not found!")
            return
        except InvalidHTTPResponse:
            await ctx.send("We're getting invalid response from the API, please try again later!")
            return
        await ctx.send("""Artist: """ + processshowapi.imgartist + """\r\nSource: `""" + processshowapi.imgsource + """`\r\nRating: """ + processshowapi.imgrating + """\r\nTags: `""" + processshowapi.imgtags + """` ...and more\r\nImage link: """ + processshowapi.file_link)

    @commands.command(pass_context=True)
    async def randompick(self, ctx, *args, description="Output random result"):
        """Output random result from e621/e926.  
        If channel is NSFW, use e621, if not, then use e926."""
        if not isinstance(ctx.channel, discord.DMChannel):
            if not ctx.channel.is_nsfw():
                netloc = "e926"
            else:
                netloc = "e621"
        else:
            netloc = "e621"
        print("------")
        print("Got command")
        apilink = 'https://' + netloc + '.net/post/index.json?tags=score:>25&limit=320&page=' + str(random.randint(1,51))
        try:
            await processapi(apilink)
        except ResultNotFound:
            await ctx.send("Result not found!")
            return
        except InvalidHTTPResponse:
            await ctx.send("We're getting invalid response from the API, please try again later!")
            return
        await ctx.send("""Post link: `https://""" + netloc + """.net/post/show/""" + processapi.imgid + """/`\r\nArtist: `""" + processapi.imgartist + """`\r\nSource: `""" + processapi.imgsource + """`\r\nRating: """ + processapi.imgrating + """\r\nTags: `""" + processapi.imgtags + """` ...and more\r\nImage link: """ + processapi.file_link)
        
    @commands.command(pass_context=True)
    async def sofurry(self, ctx, *args):
        """Searches SoFurry with given queries.

        Arguments:

        `*args` : list  
        The quer(y/ies)"""
        maxlevel = "2"
        if not isinstance(ctx.channel, discord.DMChannel):
            if not isinstance(ctx.channel, discord.GroupChannel):
                if not ctx.channel.is_nsfw():
                    maxlevel = "0"
        args = ' '.join(args)
        args = str(args)
        print("------")
        print("Got command with args: " + args)
        try:
            await search(args, maxlevel)
        except ResultNotFound:
            await ctx.send("Result not found!")
            return
        except InvalidHTTPResponse:
            await ctx.send("We're getting invalid response from the API, please try again later!")
            return
        await ctx.send("""Title: {}\r\nArtist: {}\r\nTags: `{}`\r\nRating: {}\r\nImage link: {}""".format(search.title, search.artistName, search.tags, search.contentRating, search.full))

    @commands.command()
    async def inkbunny(self, ctx, *args):
        """Searches InkBunny with given queries.

        Arguments:

        `*args` : list  
        The quer(y/ies)"""
        args = ' '.join(args)
        args = str(args)
        try:
            ib = cogs.utils.inkbunnyapi.Inkbunny(username = inkusername, password = inkpassword)
            src = await ib.search(args)
        except ResultNotFound:
            await ctx.send("Result not found!")
            return
        except InvalidHTTPResponse:
            await ctx.send("We're getting invalid response from the API, please try again later!")
            return
        await ctx.send("""Title: {}\r\nOwner: {}\r\nKeywords: `{}`\r\nLast Update: `{}`\r\nRating: {}\r\nImage link: {}""".format(src.submission_title, src.owner, src.keywords, src.last_update, src.rating, src.file_url))

    @commands.command()
    async def fa(self, ctx, *args):
        args = ' '.join(args)
        args = str(args)
        try:
            res = await cogs.utils.fapi.FurAffinity().search(args)
        except ResultNotFound:
            await ctx.send("Result not found!")
            return
        except InvalidHTTPResponse:
            await ctx.send("We're getting invalid response from the API, please try again later!")
            return
        await ctx.send("Title: `{}`\r\nArtist: `{}`\r\nKeywords: `{}`\r\nImage link: https:{}".format(res.title, res.artist, ', '.join(res.keywords), res.imglink))


def setup(bot):
    bot.add_cog(Furry(bot))