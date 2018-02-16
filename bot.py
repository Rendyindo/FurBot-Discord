import discord
from discord.ext import commands
import random, os, re, asyncio, aiohttp, cogs.utils.osuapi, traceback, sys, urllib, aioftp, cogs.utils.eapi
from urllib.parse import urlparse

try:
    import config
    token = config.token
    owner = config.owner
    osutoken = config.osutoken
    ftp_server = config.ftp_server
    ftp_password = config.ftp_password
    ftp_username = config.ftp_username
except ImportError:
    pass

try:
    token = os.environ['DISCORD_TOKEN']
    owner = os.environ['DISCORD_OWNER']
    osutoken = os.environ['OSU_TOKEN']
    ftp_server = os.environ['FTP_SERVER']
    ftp_password = os.environ['FTP_PASSWORD']
    ftp_username = os.environ['FTP_USERNAME']
except KeyError:
    pass

description = '''Bot that uhh, actually just searches e621'''
initial_extensions = (
    'cogs.furry',
    'cogs.general',
    'cogs.osu',
    'cogs.set'
)

osuapi = cogs.utils.osuapi
processapi = cogs.utils.eapi.processapi
processshowapi = cogs.utils.eapi.processshowapi

class ResultNotFound(Exception):
    pass

class InvalidHTTPResponse(Exception):
    pass

class FurBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=('f!'), description=description)
        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                print("Failed to load extension {extension}.")
                traceback.print_exc()
        if ftp_server:
            try:
                urllib.request.urlretrieve('ftp://{}:{}@{}/user.ini'.format(ftp_username, ftp_password, ftp_server), 'user.ini')
            except urllib.error.URLError:
                print("WARNING! Cannot download user.ini file!")

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        self.remove_command('help')
        await self.change_presence(game=discord.Game(name='f!help'))
    
    @commands.command()
    async def help(self, ctx, *args):
        await ctx.send("Go ahead read the README here! https://furbot.rorre.me/command")

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        await asyncio.sleep(0.5)
        await self.process_commands(message)
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

    async def find_channel(self, guild):
        for c in guild.text_channels:
            if not c.permissions_for(guild.me).send_messages:
                continue
            return c

    async def on_guild_join(self, guild):
        channel = await find_channel(guild)
        await channel.send("~~Awoo!~~ Hewwo thewe, " + guild.name + """!\r
    I'm FurBot~ If you want to try me out, go ahead check out the help! The command is `!furbot help`.\r
    If any of you need any help, feel free to join our Discord server at: `https://discord.gg/YTEeY9g`\r
    Thank you very much for using this bot!""")

    async def config_sync(self, server, username, password):
        Continue = True
        while Continue:
            async with aioftp.ClientSession(server, user=username, password=password) as client:
                print("Syncronizing config file")
                try:
                    await client.upload("user.ini")
                except:
                    print("An error occured during upload.")
                finally:
                    print("Done!")
                await asyncio.sleep(30)

bot = FurBot()
bot.loop.create_task(FurBot().config_sync(ftp_server, ftp_username, ftp_password))
bot.run(token)