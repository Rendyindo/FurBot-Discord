import discord
from discord.ext import commands
from configparser import SafeConfigParser

parser = SafeConfigParser()

class setting:
    """Settings related

    Commands:
        set        Sets something"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group()
    async def set(self, ctx):
        """Sets something
        
        Current setting commands:  
        osu: f!set osu <osu username> (Sets osu! username for osu! commands)"""
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid setting command!')

    @set.command(name="osu")
    async def _osu(self, ctx, *arg):
        """Sets osu! username."""
        args = ' '.join(arg)
        username = str(args)
        userid = ctx.message.author.id
        parser.add_section(str(userid))
        parser.set(str(userid), "osu_username", username)
        with open('user.ini', 'w') as configfile:
            parser.write(configfile)
        await ctx.send("Set osu! username to: {}".format(username))

def setup(bot):
    bot.add_cog(setting(bot))