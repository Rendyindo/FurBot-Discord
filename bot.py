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
bot = commands.Bot(command_prefix='e621!', description=description)
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

def shuffle(arr):
    random.shuffle(arr)
    return arr

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name='e621!help'))

@bot.command()
async def search(ctx, *args, description="Searches e621 with given queries"):
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
        processapi(apilink)
    except ResultNotFound:
        await ctx.send("Result not found!")
        return
    await ctx.send("""Post link: `https://e621.net/post/show/""" + processapi.imgid + """/`\r\nArtist: """ + processapi.imgartist + """\r\nSource: `""" + processapi.imgsource + """`\r\nRating: """ + processapi.imgrating + """\r\nTags: `""" + processapi.imgtags + """` ...and more\r\nImage link: """ + processapi.file_link)

bot.remove_command('help')
@bot.command()
async def help(ctx, *args):
    await ctx.send("""```FurBot, basically just a simple bot that searches e621.\r\rCommands:\r
    help: Shows this message\r
    search <search queries>: Searches e621 with given queries\r
    show <post id>: Show image with given post ID (Example Post ID: 1438576)\r\rNeed help? Something broke? Contact Error-#2194```""")

@bot.command()
async def show(ctx, arg):
    try:
        arg = int(arg)
    except ValueError:
        await ctx.send( arg + " is not a valid post id!")
        return
    if not isinstance(ctx.channel, discord.DMChannel):
        if not isinstance(ctx.channel, discord.GroupChannel):
            if not ctx.channel.is_nsfw():
                await ctx.send("Cannot be used in non-NSFW channels!")
                return
    print("------")
    arg = str(arg)
    print("Got command with arg: " + arg)
    apilink = 'https://e621.net/post/show.json?id=' + arg
    print("API Link: " + apilink)
    print("Requesting json from API")
    r = requests.get(url=apilink, headers=headers)
    data = r.json()
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
        imgrating = "Explicit"
    if imgrate == "s":
        imgrating = "Safe"
    if imgrate == "q":
        imgrating = "Mature/Questionable"
    imgsources = data['source']
    imgsource = str(imgsources)
    if imgartist == "None":
        imgartist = "Unspecified"
    if imgsource == "None":
        imgsource = "Unspecified"
    imgtags = str(' '.join(imgtags))
    file_link = str(fileurl).replace('None', '')
    await ctx.send("""Artist: """ + imgartist + """\r\nSource: `""" + imgsource + """`\r\nRating: """ + imgrating + """\r\nTags: `""" + imgtags + """` ...and more\r\nImage link: """ + file_link)

@bot.command()
async def randompick(ctx, *args, description="Output random result"):
    if not isinstance(ctx.channel, discord.DMChannel):
        if not isinstance(ctx.channel, discord.GroupChannel):
            if not ctx.channel.is_nsfw():
                await ctx.send("Cannot be used in non-NSFW channels!")
                return
    print("------")
    print("Got command")
    apilink = 'https://e621.net/post/index.json?tags=score:>200 rating:e&limit=320'
    try:
        processapi(apilink)
    except ResultNotFound:
        await ctx.send("Result not found!")
        return
    await ctx.send("""Post link: `https://e621.net/post/show/""" + processapi.imgid + """/`\r\nArtist: """ + processapi.imgartist + """\r\nSource: `""" + processapi.imgsource + """`\r\nRating: """ + processapi.imgrating + """\r\nTags: `""" + processapi.imgtags + """` ...and more\r\nImage link: """ + processapi.file_link)

@bot.event
async def on_message(message):
    msgurls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content)
    for msgurl in msgurls:
        parsed = urlparse(msgurl)
        if parsed.netloc == "e621.net":
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
            print("API Link: " + apilink)
            print("Requesting json from API")
            r = requests.get(url=apilink, headers=headers)
            data = r.json()
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
                imgrating = "Explicit"
            if imgrate == "s":
                imgrating = "Safe"
            if imgrate == "q":
                imgrating = "Mature/Questionable"
            imgsources = data['source']
            imgsource = str(imgsources)
            if imgartist == "None":
                imgartist = "Unspecified"
            if imgsource == "None":
                imgsource = "Unspecified"
            imgtags = str(' '.join(imgtags))
            file_link = str(fileurl).replace('None', '')
            await message.channel.send("""Artist: """ + imgartist + """\r\nSource: `""" + imgsource + """`\r\nRating: """ + imgrating + """\r\nTags: `""" + imgtags + """` ...and more\r\nImage link: """ + file_link)

bot.run(token)