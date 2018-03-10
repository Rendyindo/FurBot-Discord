import discord
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
        pageresult = wikifur.search(args, results=1)[0]
        page = wikifur.page(pageresult)
        embed=discord.Embed(title=page.title, url="https://en.wikifur.com/wiki/{}".format(page.title.replace(" ", "_")), color=0xd61510)
        embed.add_field(name="Summary", value=page.summarize(chars=1000), inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def wikipedia(self,ctx, *args):
        """Searches Wikipedia with given queries
        
        Usage: f!wikipedia <args>"""
        args = ' '.join(args)
        args = str(args)
        pageresult = wikipedia.search(args, results=1)[0]
        page = wikipedia.page(pageresult)
        embed=discord.Embed(title=page.title, url="https://en.wikipedia.org/wiki/{}".format(page.title.replace(" ", "_")), color=0xd61510)
        embed.add_field(name="Summary", value=page.summarize(chars=1000), inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Wiki(bot))