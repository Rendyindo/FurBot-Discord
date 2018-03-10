import discord
from discord.ext import commands
from weather import Weather

w = Weather(unit='c')

class WeatherBot():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def weather(self, ctx, *args):
        args = ' '.join(args)
        args = str(args)
        location = w.lookup_by_location(args)
        condition = location.condition()
        embed=discord.Embed(title="Weather for {}".format(args), description="Current weather: {}".format(condition.text()), color=0x0080c0)
        for forecast in location.forecast()[:9]:
            embed.add_field(name=forecast.date(), value=forecast.text(), inline=True)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(WeatherBot(bot))