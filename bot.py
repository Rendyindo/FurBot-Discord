import asyncio
import os
import random
import re
import sys
import traceback
import urllib
from urllib.parse import urlparse

import aioftp
import aiohttp
import discord
from discord.ext import commands
from bs4 import BeautifulSoup

import cogs.utils.eapi
import cogs.utils.osuapi

try:
    import config
    token = config.token
    owner = config.owner
    osutoken = config.osutoken
    fa_a = config.fa_a
    fa_b = config.fa_b
    fa_cfuid = config.fa_cfuid
    ftp_server = config.ftp_server
    ftp_password = config.ftp_password
    ftp_username = config.ftp_username
except:
    ftp_server = ''
    ftp_password = ''
    ftp_username = ''

try:
    token = os.environ['DISCORD_TOKEN']
    owner = os.environ['DISCORD_OWNER']
    osutoken = os.environ['OSU_TOKEN']
    ftp_server = os.environ['FTP_SERVER']
    ftp_password = os.environ['FTP_PASSWORD']
    ftp_username = os.environ['FTP_USERNAME']
    fa_a = os.environ['A_FA']
    fa_b = os.environ['B_FA']
    fa_cfuid = os.environ['CFUID_FA']
except KeyError:
    pass

description = '''Bot that does mainly for furry stuffs!'''
initial_extensions = (
    'cogs.furry',
    'cogs.general',
    'cogs.osu',
    'cogs.admin',
    'cogs.setting',
    'cogs.wiki'
)

osuapi = cogs.utils.osuapi
processapi = cogs.utils.eapi.processapi
processshowapi = cogs.utils.eapi.processshowapi

class ResultNotFound(Exception):
    """Used if ResultNotFound is triggered by e* API."""
    pass

class InvalidHTTPResponse(Exception):
    """Used if non-200 HTTP Response got from server."""
    pass

class FurBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=('f!'), description=description, owner_id=owner)
        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception:
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
        await self.change_presence(game=discord.Game(name='f!help'))

    @commands.command()
    @commands.is_owner()
    async def reload(self):
        """Reloads extensions."""
        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception:
                print("Failed to load extension {extension}.")
                traceback.print_exc()

    async def on_message(self, message):
        """URL detection to message.

        If we got e621 or e926 link, it will invoke `processshowapi(apilink)` and respond with given result.  
        If we got osu! beatmap link, it will invoke `osuapi.get_beatmaps(osutoken, beatmapid=mapid, beatmapsetid=mapid)` and respond with given result."""
        if message.author.id == self.user.id:
            return
        if message.author.bot:
            return
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
            if parsed.netloc == "furaffinity.net" or parsed.netloc == "www.furaffinity.net":
                urlargs = parsed.path.split('/')
                if "view" not in urlargs[1]:
                    return
                link = msgurl
                cookie = { 'b' : fa_b, 'a' : fa_a, '__cfuid' : fa_cfuid}
                async with aiohttp.ClientSession(cookies=cookie) as session:
                    async with session.get(link) as r:
                        if r.status == 200:
                            data = await r.text()
                        else:
                            print("Invalid HTTP Response:" + str(r.status))
                            raise InvalidHTTPResponse()

                s = BeautifulSoup(data, 'html.parser')
                imglink = s.find(attrs={'class' : 'alt1 actions aligncenter'}).findAll('b')[1].a.get('href')
                title = s.find(attrs={'class' : 'cat'}).string.strip()
                artist = s.findAll(attrs={'class' : 'cat'})[1].find('a').string
                keywords = []
                try:
                    for kw in s.find(attrs={'id' : 'keywords'}).findAll('a'):
                         keywords.append(kw.string)
                except:
                    keywords.append("Unspecified")
                await message.channel.send("Title: `{}`\r\nArtist: `{}`\r\nKeywords: `{}`\r\nImage link: https:{}".format(title, artist, ', '.join(keywords), imglink))


    async def find_channel(self, guild):
        """Automatically find suitable channel to send, this is invoked for `on_guild_join(guild)`"""
        for c in guild.text_channels:
            if not c.permissions_for(guild.me).send_messages:
                continue
            return c

    async def on_guild_join(self, guild):
        """Sends greeting message to server when joining, but it searches for suitable channel first by invoking `find_channel(guild)`"""
        channel = await self.find_channel(guild)
        await channel.send("~~Awoo!~~ Hewwo thewe, " + guild.name + """!\r
    I'm FurBot~ If you want to try me out, go ahead check out the help! The command is `!furbot help`.\r
    If any of you need any help, feel free to join our Discord server at: `https://discord.gg/YTEeY9g`\r
    Thank you very much for using this bot!""")
        try:
            await guild.create_role(name="Silenced", permissions=[discord.Permissions.read_messages, discord.Permissions.read_message_history])
        except:
            await channel.send("Huh, seems like I failed to add a role, did you add 'Manage Role' permission to me?")
            traceback.print_exc()

    async def config_sync(self, server, username, password):
        """Configuration syncronization"""
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
                await asyncio.sleep(300)

bot = FurBot()
if ftp_server:
    bot.loop.create_task(FurBot().config_sync(ftp_server, ftp_username, ftp_password))
bot.run(token)