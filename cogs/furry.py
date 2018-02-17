import discord
from discord.ext import commands
import random, asyncio, cogs.utils.eapi
from urllib.parse import urlparse

processapi = cogs.utils.eapi.processapi
processshowapi = cogs.utils.eapi.processshowapi

class ResultNotFound(Exception):
    """Used if ResultNotFound is triggered by e* API."""
    pass

class InvalidHTTPResponse(Exception):
    """Used if non-200 HTTP Response got from server."""
    pass

class Furry():
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
        apilink = 'https://e621.net/post/index.json?tags=' + args + '&limit=320'
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
        apilink = 'https://e926.net/post/index.json?tags=' + args + '&limit=320'
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
            if not isinstance(ctx.channel, discord.GroupChannel):
                if not ctx.channel.is_nsfw():
                    netloc = "e926"
                else:
                    netloc = "e621"
        print("------")
        print("Got command")
        apilink = 'https://' + netloc + '.net/post/index.json?tags=score:>200 rating:e&limit=320'
        try:
            await processapi(apilink)
        except ResultNotFound:
            await ctx.send("Result not found!")
            return
        except InvalidHTTPResponse:
            await ctx.send("We're getting invalid response from the API, please try again later!")
            return
        await ctx.send("""Post link: `https://""" + netloc + """.net/post/show/""" + processapi.imgid + """/`\r\nArtist: `""" + processapi.imgartist + """`\r\nSource: `""" + processapi.imgsource + """`\r\nRating: """ + processapi.imgrating + """\r\nTags: `""" + processapi.imgtags + """` ...and more\r\nImage link: """ + processapi.file_link)

def setup(bot):
    bot.add_cog(Furry(bot))