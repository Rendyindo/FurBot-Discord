import discord
from discord.ext import commands
import random, asyncio
from urllib.parse import urlparse

@bot.command(pass_context=True)
async def e621(ctx, *args):
    if not isinstance(ctx.channel, discord.DMChannel):
        if not isinstance(ctx.channel, discord.GroupChannel):
            if not ctx.channel.is_nsfw():
                await ctx.send("Cannot be used in non-NSFW channels!")
                return
    args = ' '.join(args)
    args = str(args)
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
    await ctx.send("""Post link: `https://e621.net/post/show/""" + processapi.imgid + """/`\r\nArtist: """ + processapi.imgartist + """\r\nSource: `""" + processapi.imgsource + """`\r\nRating: """ + processapi.imgrating + """\r\nTags: `""" + processapi.imgtags + """` ...and more\r\nImage link: """ + processapi.file_link)

@bot.command(pass_context=True)
async def e926(ctx, *args):
    args = ' '.join(args)
    args = str(args)
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
    await ctx.send("""Post link: `https://e926.net/post/show/""" + processapi.imgid + """/`\r\nArtist: """ + processapi.imgartist + """\r\nSource: `""" + processapi.imgsource + """`\r\nRating: """ + processapi.imgrating + """\r\nTags: `""" +
    
    @bot.command(pass_context=True)
async def show(ctx, arg):
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

@bot.command(pass_context=True)
async def randompick(ctx, *args, description="Output random result"):
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
    await ctx.send("""Post link: `https://""" + netloc + """.net/post/show/""" + processapi.imgid + """/`\r\nArtist: """ + processapi.imgartist + """\r\nSource: `""" + processapi.imgsource + """`\r\nRating: """ + processapi.imgrating + """\r\nTags: `""" + processapi.imgtags + """` ...and more\r\nImage link: """ + processapi.file_link)
