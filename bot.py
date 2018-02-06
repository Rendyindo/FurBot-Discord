import discord
from discord.ext import commands
import requests, random, os, re
from urllib.parse import urlparse

try:
    import config
    token = config.token
except ImportError:
    pass

try:
    token = os.environ['DISCORD_TOKEN']
except KeyError:
    pass

class ResultNotFound(Exception):
    pass

description = '''Bot that uhh, actually just searches e621'''
bot = commands.Bot(command_prefix=('!furbot ', '!e621 ', '!e926 '), description=description)
headers = {
    'User-Agent': 'SearchBot/1.0 (by Error- on e621)'
}

def processapi(apilink):
    print("API Link: " + apilink)
    print("Requesting json from API")
    r = requests.get(url=apilink, headers=headers)
    datajson = r.json()
    if not datajson:
        print("Result Not Found")
        raise ResultNotFound()
    print("Shuffling data from json")
    data = shuffle(datajson)
    print("Parsing data from json")
    fileurl = data[0]['file_url']
    imgartists = data[0]['artist']
    imgartist = ''.join(imgartists)
    imgtag = data[0]['tags']
    imgtag = imgtag.split(" ")
    tags = [imgtag[x:x+25] for x in range(0, len(imgtag), 25)]
    imgtags = tags[0]
    imgrate = data[0]['rating']
    if imgrate == "e":
        processapi.imgrating = "Explicit"
    if imgrate == "s":
        processapi.imgrating = "Safe"
    if imgrate == "q":
        processapi.imgrating = "Mature/Questionable"
    imgsources = data[0]['source']
    imgsource = str(imgsources)
    if imgartist == "None":
        processapi.imgartist = "Unspecified"
    else:
        processapi.imgartist = imgartist
    if imgsource == "None":
        processapi.imgsource = "Unspecified"
    else:
        processapi.imgsource = imgsource
    processapi.imgtags = str(' '.join(imgtags))
    imgid = data[0]['id']
    processapi.imgid = str(imgid)
    processapi.file_link = str(fileurl).replace('None', '')

def processshowapi(apilink):
    print("API Link: " + apilink)
    print("Requesting json from API")
    r = requests.get(url=apilink, headers=headers)
    data = r.json()
    if not data:
        print("Result Not Found")
        raise ResultNotFound()
    print("Parsing data from json")
    fileurl = data['file_url']
    imgartists = data['artist']
    imgartist = ''.join(imgartists)
    imgtag = data['tags']
    imgtag = imgtag.split(" ")
    tags = [imgtag[x:x+25] for x in range(0, len(imgtag), 25)]
    imgtags = tags[0]
    imgrate = data['rating']
    if imgrate == "e":
        processshowapi.imgrating = "Explicit"
    if imgrate == "s":
        processshowapi.imgrating = "Safe"
    if imgrate == "q":
        processshowapi.imgrating = "Mature/Questionable"
    imgsources = data['source']
    imgsource = str(imgsources)
    if imgartist == "None":
        processshowapi.imgartist = "Unspecified"
    else:
        processshowapi.imgartist = imgartist
    if imgsource == "None":
        processshowapi.imgsource = "Unspecified"
    else:
        processshowapi.imgsource = imgsource
    processshowapi.imgtags = str(' '.join(imgtags))
    processshowapi.file_link = str(fileurl).replace('None', '')

def shuffle(arr):
    random.shuffle(arr)
    return arr

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name='!furbot help'))

@bot.command(pass_context=True)
async def search(ctx, *args, description="Searches e621 with given queries"):
    if ctx.message.content.startswith('!e926'):
        netloc = "e926"
    else:
        netloc = "e621"
    if netloc == "e621":
        if not isinstance(ctx.channel, discord.DMChannel):
            if not isinstance(ctx.channel, discord.GroupChannel):
                if not ctx.channel.is_nsfw():
                    await ctx.send("Cannot be used in non-NSFW channels!")
                    return
    args = ' '.join(args)
    args = str(args)
    print("------")
    print("Got command with args: " + args)
    apilink = 'https://' + netloc + '.net/post/index.json?tags=' + args + '&limit=320'
    try:
        processapi(apilink)
    except ResultNotFound:
        await ctx.send("Result not found!")
        return
    await ctx.send("""Post link: `https://""" + netloc + """.net/post/show/""" + processapi.imgid + """/`\r\nArtist: """ + processapi.imgartist + """\r\nSource: `""" + processapi.imgsource + """`\r\nRating: """ + processapi.imgrating + """\r\nTags: `""" + processapi.imgtags + """` ...and more\r\nImage link: """ + processapi.file_link)

bot.remove_command('help')
@bot.command(pass_context=True)
async def help(ctx, *args):
    await ctx.send("""```FurBot, basically just a simple bot that searches e621 and e926.
\r
\rCommands:\r
    help: Shows this message\r
    search <search queries>: Searches e621 with given queries\r
    show <post id>: Show image with given post ID (Example Post ID: 1438576)\r
    randompick: Replies a random pick from e621 or e926
\rUse !e621 for NSFW result, or use !e926 for SFW result. (Using !furbot will force using !e621)
\r
\rNeed help? Something broke? Contact Error-#2194```""")

@bot.command(pass_context=True)
async def show(ctx, arg):
    if ctx.message.content.startswith('!e926'):
        netloc = "e926"
    else:
        netloc = "e621"
    try:
        arg = int(arg)
    except ValueError:
        await ctx.send( arg + " is not a valid post id!")
        return
    if netloc == "e621":
        if not isinstance(ctx.channel, discord.DMChannel):
            if not isinstance(ctx.channel, discord.GroupChannel):
                if not ctx.channel.is_nsfw():
                    await ctx.send("Cannot be used in non-NSFW channels!")
                    return
    print("------")
    arg = str(arg)
    print("Got command with arg: " + arg)
    apilink = 'https://' + netloc + '.net/post/show.json?id=' + arg
    try:
        processshowapi(apilink)
    except ResultNotFound:
        await ctx.send("Result not found!")
        return
    await ctx.send("""Artist: """ + processshowapi.imgartist + """\r\nSource: `""" + processshowapi.imgsource + """`\r\nRating: """ + processshowapi.imgrating + """\r\nTags: `""" + processshowapi.imgtags + """` ...and more\r\nImage link: """ + processshowapi.file_link)

@bot.command(pass_context=True)
async def randompick(ctx, *args, description="Output random result"):
    if ctx.message.content.startswith('!e926'):
        netloc = "e926"
    else:
        netloc = "e621"
    print("------")
    print("Got command")
    apilink = 'https://' + netloc + '.net/post/index.json?tags=score:>200 rating:e&limit=320'
    try:
        processapi(apilink)
    except ResultNotFound:
        await ctx.send("Result not found!")
        return
    await ctx.send("""Post link: `https://""" + netloc + """.net/post/show/""" + processapi.imgid + """/`\r\nArtist: """ + processapi.imgartist + """\r\nSource: `""" + processapi.imgsource + """`\r\nRating: """ + processapi.imgrating + """\r\nTags: `""" + processapi.imgtags + """` ...and more\r\nImage link: """ + processapi.file_link)

@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
         return
    await bot.process_commands(message)
    msgurls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content)
    for msgurl in msgurls:
        parsed = urlparse(msgurl)
        if parsed.netloc == "e621.net":
            if not isinstance(message.channel, discord.DMChannel):
                if not isinstance(message.channel, discord.GroupChannel):
                    if not message.channel.is_nsfw():
                        return
            urlargs = parsed.path.split('/')
            try:
                postid = urlargs[3]
            except IndexError:
                return
            try:
                int(postid)
            except ValueError:
                return
            print("------")
            arg = str(postid)
            print("Got command with arg: " + arg)
            apilink = 'https://e621.net/post/show.json?id=' + arg
            try:
                processshowapi(apilink)
            except ResultNotFound:
                return
            await message.channel.send("""Artist: """ + processshowapi.imgartist + """\r\nSource: `""" + processshowapi.imgsource + """`\r\nRating: """ + processshowapi.imgrating + """\r\nTags: `""" + processshowapi.imgtags + """` ...and more\r\nImage link: """ + processshowapi.file_link)
        if parsed.netloc == "e926.net":
            urlargs = parsed.path.split('/')
            try:
                postid = urlargs[3]
            except IndexError:
                return
            try:
                int(postid)
            except ValueError:
                return
            print("------")
            arg = str(postid)
            print("Got command with arg: " + arg)
            apilink = 'https://e926.net/post/show.json?id=' + arg
            try:
                processshowapi(apilink)
            except ResultNotFound:
                return
            await message.channel.send("""Artist: """ + processshowapi.imgartist + """\r\nSource: `""" + processshowapi.imgsource + """`\r\nRating: """ + processshowapi.imgrating + """\r\nTags: `""" + processshowapi.imgtags + """` ...and more\r\nImage link: """ + processshowapi.file_link)

async def find_channel(guild):
    for c in guild.text_channels:
        if not c.permissions_for(guild.me).send_messages:
            continue
        return c

@bot.event
async def on_guild_join(guild):
    channel = await find_channel(guild)
    await channel.send("~~Awoo!~~ Hewwo thewe, " + guild.name + """!\r
I'm FurBot, a e621/e926 search bot! If you want to try me out, go ahead check out the help! The command is `!furbot help`.\r
If any of you need any help, feel free to join our Discord server at: `https://discord.gg/YTEeY9g`\r
Thank you very much for using this bot!""")

bot.run(token)