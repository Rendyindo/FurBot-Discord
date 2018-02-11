import discord
from discord.ext import commands
import random, os, re, asyncio, aiohttp, osuapi
from urllib.parse import urlparse

try:
    import config
    token = config.token
    owner = config.owner
    osutoken = config.osutoken
except ImportError:
    pass

try:
    token = os.environ['DISCORD_TOKEN']
    owner = os.environ['DISCORD_OWNER']
    osutoken = os.environ['OSU_TOKEN']
except KeyError:
    pass

class ResultNotFound(Exception):
    pass

class InvalidHTTPResponse(Exception):
    pass

description = '''Bot that uhh, actually just searches e621'''
bot = commands.Bot(command_prefix=('f!'), description=description)
headers = {
    'User-Agent': 'SearchBot/1.0 (by Error- on e621)'
}

async def processapi(apilink):
    print("API Link: " + apilink)
    print("Requesting json from API")
    async with aiohttp.ClientSession() as session:
        async with session.get(apilink, headers=headers) as r:
            if r.status == 200:
                datajson = await r.json()
            else:
                print("Invalid HTTP Response:" + str(r.status))
                raise InvalidHTTPResponse()
    if not datajson:
        print("Result Not Found")
        raise ResultNotFound()
    print("Shuffling data from json")
    data = shuffle(datajson)
    print("Parsing data from json")
    fileurl = data[0]['file_url']
    imgartists = data[0]['artist']
    imgartist = ', '.join(imgartists)
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

async def processshowapi(apilink):
    print("API Link: " + apilink)
    print("Requesting json from API")
    async with aiohttp.ClientSession() as session:
        async with session.get(apilink, headers=headers) as r:
            if r.status == 200:
                datajson = await r.json()
            else:
                print("Invalid HTTP Response:" + str(r.status))
                raise InvalidHTTPResponse()
    if not data:
        print("Result Not Found")
        raise ResultNotFound()
    print("Parsing data from json")
    fileurl = data['file_url']
    imgartists = data['artist']
    imgartist = ', '.join(imgartists)
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
    await bot.change_presence(game=discord.Game(name='f!help'))

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
    await ctx.send("""Post link: `https://e926.net/post/show/""" + processapi.imgid + """/`\r\nArtist: """ + processapi.imgartist + """\r\nSource: `""" + processapi.imgsource + """`\r\nRating: """ + processapi.imgrating + """\r\nTags: `""" + processapi.imgtags + """` ...and more\r\nImage link: """ + processapi.file_link)


bot.remove_command('help')
@bot.command(pass_context=True)
async def help(ctx, *args):
    await ctx.send("Go ahead read the README here! https://github.com/Rendyindo/FurBot-Discord")

@bot.command(pass_context=True)
async def show(ctx, arg):
    if not isinstance(ctx.channel, discord.DMChannel):
        if not isinstance(ctx.channel, discord.GroupChannel):
            if not ctx.channel.is_nsfw():
                netloc = "e926"
            else:
                netloc = "e621"
    print("------")
    arg = str(arg)
    print("Got command with arg: " + arg)
    apilink = 'https://' + netloc + '.net/post/show.json?id=' + arg
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

@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
         return
    await asyncio.sleep(0.5)
    await bot.process_commands(message)
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
            try:
                await processshowapi(apilink)
            except ResultNotFound:
                return
            except InvalidHTTPResponse:
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
                await processshowapi(apilink)
            except ResultNotFound:
                return
            except InvalidHTTPResponse:
                return
            await message.channel.send("""Artist: """ + processshowapi.imgartist + """\r\nSource: `""" + processshowapi.imgsource + """`\r\nRating: """ + processshowapi.imgrating + """\r\nTags: `""" + processshowapi.imgtags + """` ...and more\r\nImage link: """ + processshowapi.file_link)
        if parsed.netloc == "osu.ppy.sh":
            urlargs = parsed.path.split('/')
            try:
                if not urlargs[1]:
                    return
                maptype = urlargs[1]
                mapid = urlargs[2]
            except IndexError:
                return
            if maptype == "b":
                await osuapi.get_beatmaps(osutoken, beatmapid=mapid)
            else:
                await osuapi.get_beatmaps(osutoken, beatmapsetid=mapid)
            map = osuapi.get_beatmaps
            embed=discord.Embed(title="{} - {} [{}]".format(map.artist, map.title, map.version), url=msgurl, description="Mapped by: {}".format(map.creator), color=0xa04db3)
            embed.set_thumbnail(url="https://b.ppy.sh/thumb/{}l.jpg".format(str(map.set_id)))
            embed.add_field(name="Map Status", value="Ranked: `{}` | Ranked date: `{}`".format(map.isranked, map.approved_date), inline=False)
            embed.add_field(name="Map Info", value="HP: `{}` | AR: `{}` | OD: `{}` | CS: `{}` | SR: `{}`".format(map.diff_drain, map.diff_approach, map.diff_overall, map.diff_size, round(map.difficultyrating, 2)), inline=False)
            await message.channel.send(embed=embed)
            

@bot.command(pass_context=True)
async def avatar(ctx, message):
    mentions = ctx.message.mentions
    for user in mentions:
        avatarurl = user.avatar_url
        await ctx.send("Avatar URL for " + user.mention + """\r
""" + avatarurl)

@bot.command(pass_context=True)
async def urban(ctx, *args):
    args = ' '.join(args)
    args = str(args)
    apilink = "http://api.urbandictionary.com/v0/define?term=" + args
    r = requests.get(url=apilink, headers=headers)
    datajson = r.json()
    listcount = 0
    try:
        while datajson['list'][listcount]['definition'].count('') > 1001:
            listcount = listcount + 1
    except IndexError:
        await ctx.send("Sorry, but we seem to reach the Discord character limit!")
    result = datajson['list'][listcount]
    embed=discord.Embed(title="**" + result['word'] + "**", url=result['permalink'], description="by: " + result['author'], color=0xc4423c)
    embed.add_field(name="Definition", value=result['definition'], inline=False)
    embed.add_field(name="Example", value=result['example'], inline=True)
    embed.set_footer(text=u"👍 " + str(result['thumbs_up']) + " | " + u"👎 " + str(result['thumbs_down']))
    await ctx.send(embed=embed)

async def find_channel(guild):
    for c in guild.text_channels:
        if not c.permissions_for(guild.me).send_messages:
            continue
        return c

@bot.event
async def on_guild_join(guild):
    channel = await find_channel(guild)
    await channel.send("~~Awoo!~~ Hewwo thewe, " + guild.name + """!\r
I'm FurBot~ If you want to try me out, go ahead check out the help! The command is `!furbot help`.\r
If any of you need any help, feel free to join our Discord server at: `https://discord.gg/YTEeY9g`\r
Thank you very much for using this bot!""")

@bot.command()
async def about(ctx):
    embed=discord.Embed(color=0x0089ff)
    embed.add_field(name=Developer, value="Error-", inline=False)
    embed.add_field(name=Library, value=discord.py, inline=False)
    embed.add_field(name="Support Server", value="https://discord.gg/YTEeY9g", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def report(ctx, *args):
    args = ' '.join(args)
    message = str(args)
    with open("reports.log", "w") as text_file:
        text_file.write(message)
    await ctx.send("Thanks for your input! I've notified my owner about it~")
    user = bot.get_user(int(owner))
    await user.send("""New report:\r
```""" + message + "```")

@bot.command()
async def choose(ctx, *args):
    args = ' '.join(args)
    args = str(args)
    choices = args.split('|')
    if len(choices) < 2:
        await ctx.send("You need to send at least 2 argument!")
        return
    await ctx.send(random.choice(choices) + ", of course!")

@bot.group()
async def osu(ctx, *arg):
    if not arg:
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid osu command!')
            return
    args = ' '.join(arg)
    username = str(args)
    await osuapi.get_user(osutoken, username)
    user = osuapi.get_user
    embed=discord.Embed()
    embed.set_thumbnail(url="https://a.ppy.sh/{}_1.png".format(user.id))
    embed.add_field(name="Profile for {}".format(user.name), value="Mode: osu!standard", inline=False)
    embed.add_field(name="Player Info", value="Rank: `{}` | pp: `{}` | Accuracy: `{}` | Level: `{}`".format(user.pp_rank, round(user.pp), round(user.accuracy), round(user.level)), inline=False)
    await ctx.send(embed=embed)

@bot.group()
async def taiko(ctx, *arg):
    if not arg:
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid taiko command!')
            return
    args = ' '.join(arg)
    username = str(args)
    await osuapi.get_user(osutoken, username, mode=1)
    user = osuapi.get_user
    embed=discord.Embed()
    embed.set_thumbnail(url="https://a.ppy.sh/{}_1.png".format(user.id))
    embed.add_field(name="Profile for {}".format(user.name), value="Mode: Taiko", inline=False)
    embed.add_field(name="Player Info", value="Rank: `{}` | pp: `{}` | Accuracy: `{}` | Level: `{}`".format(user.pp_rank, round(user.pp), round(user.accuracy), round(user.level)), inline=False)
    await ctx.send(embed=embed)

@bot.group()
async def catch(ctx, *arg):
    if not arg:
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid catch command!')
            return
    args = ' '.join(arg)
    username = str(args)
    await osuapi.get_user(osutoken, username, mode=2)
    user = osuapi.get_user
    embed=discord.Embed()
    embed.set_thumbnail(url="https://a.ppy.sh/{}_1.png".format(user.id))
    embed.add_field(name="Profile for {}".format(user.name), value="Mode: osu!catch", inline=False)
    embed.add_field(name="Player Info", value="Rank: `{}` | pp: `{}` | Accuracy: `{}` | Level: `{}`".format(user.pp_rank, round(user.pp), round(user.accuracy), round(user.level)), inline=False)
    await ctx.send(embed=embed)

@bot.group()
async def mania(ctx, *arg):
    if not arg:
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid mania command!')
            return
    args = ' '.join(arg)
    username = str(args)
    await osuapi.get_user(osutoken, username, mode=3)
    user = osuapi.get_user
    embed=discord.Embed()
    embed.set_thumbnail(url="https://a.ppy.sh/{}_1.png".format(user.id))
    embed.add_field(name="Profile for {}".format(user.name), value="Mode: osu!mania", inline=False)
    embed.add_field(name="Player Info", value="Rank: `{}` | pp: `{}` | Accuracy: `{}` | Level: `{}`".format(user.pp_rank, round(user.pp), round(user.accuracy), round(user.level)), inline=False)
    await ctx.send(embed=embed)

bot.run(token)