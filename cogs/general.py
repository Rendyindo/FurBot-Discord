import discord, random, spice_api, lxml, os, html
from discord.ext import commands
import asyncio, aiohttp
from weather import Weather
import urllib
from urllib.parse import urlparse
import cogs.utils.eapi

processshowapi = cogs.utils.eapi.processshowapi
w = Weather(unit='c')
sauceurl = "https://saucenao.com/search.php?db=999&output_type=2&testmode=1&numres=16&url="
try:
    import config
    MALUsername = config.malusername
    MALPassword = config.malpassword
except ImportError:
    pass

try:
    MALUsername = os.environ['MAL_USERNAME']
    MALPassword = os.environ['MAL_PASSWORD']
except KeyError:
    pass

try:
    import config
    owner = config.owner
except:
    pass

class ResultNotFound(Exception):
    """Used if ResultNotFound is triggered by e* API."""
    pass

class InvalidHTTPResponse(Exception):
    """Used if non-200 HTTP Response got from server."""
    pass

class General():
    """General/fun stuffs.

    Commands:
        about      Well uhh, the bot's info, of course...
        anime      Searches anime to MAL
        avatar     Sends avatar link of mentioned user.
        choose     Choose one of a lot arguments
        manga      Searches manga to MAL
        report     Reports a problem to bot owner.
        sauce      Reverse search an image given
        urban      Searches urbandictionary for a definition.
        weather    Searches weather of a location (and forecast)"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def avatar(self, ctx, message):
        """Sends avatar link of mentioned user.

        Arguments:

        `(mentioned user)` : `discord.User`"""
        mentions = ctx.message.mentions
        for user in mentions:
            avatarurl = user.avatar_url
            await ctx.send("Avatar URL for " + user.mention + """\r
    """ + avatarurl)

    @commands.command(pass_context=True)
    async def urban(self, ctx, *args):
        """Searches urbandictionary for a definition.

        Arguments:

        `*args` : list  
        The quer(y/ies)"""
        args = ' '.join(args)
        args = str(args)
        apilink = "http://api.urbandictionary.com/v0/define?term=" + args
        async with aiohttp.ClientSession() as session:
            async with session.get(apilink) as r:
                if r.status == 200:
                    datajson = await r.json()
                else:
                    print("Invalid HTTP Response:" + str(r.status))
                    raise InvalidHTTPResponse()
        listcount = 0
        if not datajson['list']:
            await ctx.send("Result not found!")
            return
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

    @commands.command()
    async def about(self, ctx):
        """Well uhh, the bot's info, of course..."""
        embed=discord.Embed(color=0x0089ff)
        embed.add_field(name="Developer", value="Error-", inline=False)
        embed.add_field(name="Library", value="discord.py", inline=False)
        embed.add_field(name="Support Server", value="https://discord.gg/YTEeY9g", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def report(self, ctx, *args):
        """Reports a problem to bot owner.

        Arguments:

        `*args` : list  
        The report splitted to list."""
        args = ' '.join(args)
        message = str(args)
        with open("reports.log", "w") as text_file:
            text_file.write(message)
        await ctx.send("Thanks for your input! I've notified my owner about it~")
        user = self.bot.get_user(int(owner))
        await user.send("""New report:\r
    ```""" + message + "```")

    @commands.command()
    async def choose(self, ctx, *args):
        """Choose one of a lot arguments

        Arguments:

        `*args` : list  
        The message but its splitted to a list.

        Usage:

        `<prefix>choose Arg1 | Arg2 | Arg3 | ...`"""
        args = ' '.join(args)
        args = str(args)
        choices = args.split('|')
        if len(choices) < 2:
            await ctx.send("You need to send at least 2 argument!")
            return
        await ctx.send(random.choice(choices) + ", of course!")

    @commands.command()
    async def weather(self, ctx, *args):
        """Searches weather of a location (and forecast)
        
        Usage: f!weather <place>"""
        args = ' '.join(args)
        args = str(args)
        location = w.lookup_by_location(args)
        condition = location.condition()
        embed=discord.Embed(title="Weather for {}".format(args), description="Current weather: {}".format(condition.text()), color=0x0080c0)
        for forecast in location.forecast()[:9]:
            embed.add_field(name=forecast.date(), value=forecast.text(), inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def sauce(self, ctx):
        """Reverse search an image given

            Usage: uhmm, actually just send an image wiyh f!sauce as description"""
        embeds = ctx.message.attachments
        if not embeds:
            await ctx.send("Please send me an image with `f!sauce` as description!")
        for embed in embeds:
            imageurl = embed.url
            apilink = sauceurl + imageurl
            async with aiohttp.ClientSession() as session:
                async with session.get(apilink) as r:
                    if r.status == 200:
                        datajson = await r.json()
                    else:
                        print("Invalid HTTP Response:" + str(r.status))
                        raise InvalidHTTPResponse()
            result = datajson['results'][0]
            name = result['header']['index_name']
            data = result['data']
            if float(result['header']['similarity']) < 70:
                await ctx.send("No result with 75% (or more) found for this image!")
                return
            try:
                title = data['title']
            except KeyError:
                title = ""
            try:
                author = data['author_name']
            except KeyError:
                author = ""
            origurl = data['ext_urls'][0]
            if "Anime" in name:
                anime = data['source']
                part = data['part']
                time = data['est_time']
                await ctx.send("Result found!\r\nAnime: {} - {}\r\nEstimated Time: {}".format(anime, part, time))
            elif "e621" in name:
                parsed = urlparse(origurl)
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
                    await ctx.send("""Result found!\r\nArtist: """ + processshowapi.imgartist + """\r\nSource: `""" + processshowapi.imgsource + """`\r\nRating: """ + processshowapi.imgrating + """\r\nTags: `""" + processshowapi.imgtags + """` ...and more\r\nImage link: """ + processshowapi.file_link)
            else:
                await ctx.send("Result found! ({})\r\nTitle: {}\r\nAuthor: {}\r\nURL: {}".format(name, title, author, origurl))
    
    @commands.command()
    async def anime(self, ctx, *args):
        """Searches anime to MAL
        
        Usage: f!anime <query>"""
        args = ' '.join(args)
        args = str(args)
        creds = spice_api.init_auth(MALUsername, MALPassword)
        try:
            anime = spice_api.search(args, spice_api.get_medium("anime"), creds)[0]
        except IndexError:
            await ctx.send("Cannot find that anime from MAL!")
            return
        embed=discord.Embed(title=anime.title, url="https://myanimelist.net/anime/{}".format(anime.id), description="{} | {} episode(s) | Score: {}".format(anime.anime_type, anime.episodes, anime.score), color=0x2c80d3)
        embed.set_thumbnail(url=anime.image_url)
        if len(anime.synopsis) > 1024:
            embed.add_field(name="Synopsis", value=html.unescape(anime.synopsis[:1000]).replace("<br />", "") + "...", inline=False)
        else:
            embed.add_field(name="Synopsis", value=html.unescape(anime.synopsis).replace("<br />", ""), inline=False)
        embed.set_footer(text=anime.status)
        await ctx.send(embed=embed)

    @commands.command()
    async def manga(self, ctx, *args):
        """Searches manga to MAL
        
        Usage: f!manga <query>"""
        args = ' '.join(args)
        args = str(args)
        creds = spice_api.init_auth(MALUsername, MALPassword)
        try:
            manga = spice_api.search(args, spice_api.get_medium("manga"), creds)[0]
        except IndexError:
            await ctx.send("Cannot find that manga from MAL!")
            return
        embed=discord.Embed(title=manga.title, url="https://myanimelist.net/anime/{}".format(manga.id), description="{} | {} volume(s) and {} chapter(s) | Score: {}".format(manga.manga_type, manga.volumes, manga.chapters , manga.score), color=0x2c80d3)
        embed.set_thumbnail(url=manga.image_url)
        if len(manga.synopsis) > 1024:
            embed.add_field(name="Synopsis", value=html.unescape(manga.synopsis[:1000]).replace("<br />", "") + "...", inline=False)
        else:
            embed.add_field(name="Synopsis", value=html.unescape(manga.synopsis[:1000]).replace("<br />", ""), inline=False)
        embed.set_footer(text=manga.status)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(General(bot))