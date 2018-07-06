import discord, mediawiki
from discord.ext import commands
from mediawiki import MediaWiki

wikifur = MediaWiki(url="https://en.wikifur.com/w/api.php")
wikipedia = MediaWiki()

class Wiki():
    """Wiki stuffs

    Commands:
        wikifur    Searches WikiFur with given queries
        wikipedia  Searches Wikipedia with given queries"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wikifur(self, ctx, *args):
        """Searches WikiFur with given queries
        
        Usage: f!wikifur <args>"""
        args = ' '.join(args)
        args = str(args)
        try:
            pageresult = wikifur.search(args, results=1)[0]
        except IndexError:
            await ctx.send("Result not found!")
            return
        try:
            page = wikifur.page(pageresult)
        except mediawiki.exceptions.DisambiguationError:
            await ctx.send("Title is pretty ambiguous, please be more spesific!")
            return
        embed=discord.Embed(title=page.title, url="https://en.wikifur.com/wiki/{}".format(page.title.replace(" ", "_")), color=0xd61510)
        embed.add_field(name="Summary", value=page.summarize(chars=1000), inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def wikipedia(self,ctx, *args):
        """Searches Wikipedia with given queries
        
        Usage: f!wikipedia <args>"""
        args = ' '.join(args)
        args = str(args)
        try:
            pageresult = wikipedia.search(args, results=1)[0]
        except IndexError:
            await ctx.send("Result not found!")
            return
        try:
            page = wikipedia.page(pageresult)
        except mediawiki.exceptions.DisambiguationError:
            await ctx.send("Title is pretty ambiguous, please be more spesific!")
            return
        embed=discord.Embed(title=page.title, url="https://en.wikipedia.org/wiki/{}".format(page.title.replace(" ", "_")), color=0xd61510)
        embed.add_field(name="Summary", value=page.summarize(chars=1000), inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Wiki(bot))
