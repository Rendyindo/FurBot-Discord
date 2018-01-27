import discord
from discord.ext import commands
import requests, random, os

try:
    import config
except ImportError:
    pass

try:
    token = os.environ['DISCORD_TOKEN']
except KeyError:
    pass

description = '''Bot that uhh, actually just searches e621'''
bot = commands.Bot(command_prefix='?', description=description)
def shuffle(arr):
    random.shuffle(arr)
    return arr

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name='?e621 <search queries>'))

@bot.command()
async def e621(*args, description="Searches e621 with given queries"):
    headers = {
        'User-Agent': 'SearchBot/1.0 (by Error- on e621)'
    }
    args = str(args).replace('(', '').replace("'", '').replace(',', '').replace(')', '')
    print(args)
    apilink = 'https://e621.net/post/index.json?tags=' + args + '&limit=320'
    print(apilink)
    r = requests.get(url=apilink, headers=headers)
    datajson = r.json()
    if not datajson:
        await bot.say("No result for that query")
        return
    data = shuffle(datajson)
    fileurl = data[0]['file_url']
    imgartists = data[0]['artist']
    imgartist = ''.join(imgartists)
    imgtag = data[0]['tags']
    imgrate = data[0]['rating']
    if imgrate == "e":
        imgrating = "Explicit"
    if imgrate == "s":
        imgrating = "Safe"
    if imgrate == "q":
        imgrating = "Mature/Questionable"
    imgsources = data[0]['source']
    imgsource = str(imgsources)
    if imgartist == "None":
        imgartist = "Unspecified"
    if imgsource == "None":
        imgsource = "Unspecified"
    print(fileurl)
    imgtags = str(imgtag)
    file_link = str(fileurl).replace('None', '')
    print(file_link)
    print(imgtags)
    await bot.say("""Artist: """ + imgartist + """\rSource: """ + imgsource + """\rRating: """ + imgrating + """\rTags: `""" + imgtags + """`\rImage link: """ + file_link)

bot.remove_command('help')
@bot.command()
async def help(*args):
    await bot.say("""```FurBot, basically just a simple bot that searches e621.\r\rCommands:\r
    help: Shows this message\r
    e621 <search queries>: Searches e621 with given queries\r\rNeed help? Something broke? Contact Error-#2194```""")

bot.run(token)