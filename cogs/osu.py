import discord, cogs.utils.osuapi
from discord.ext import commands

osuapi = cogs.utils.osuapi

class osu():
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def osu(self, ctx, *arg):
        args = ' '.join(arg)
        username = str(args)
        await osuapi.get_user(osutoken, username)
        user = osuapi.get_user
        embed=discord.Embed()
        embed.set_thumbnail(url="https://a.ppy.sh/{}_1.png".format(user.id))
        embed.add_field(name="Profile for {}".format(user.name), value="Mode: osu!standard", inline=False)
        embed.add_field(name="Player Info", value="Rank: `{}` | pp: `{}` | Accuracy: `{}` | Level: `{}`".format(user.pp_rank, round(user.pp), round(user.accuracy), round(user.level)), inline=False)
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    async def taiko(self, ctx, *arg):
        args = ' '.join(arg)
        username = str(args)
        await osuapi.get_user(osutoken, username, mode=1)
        user = osuapi.get_user
        embed=discord.Embed()
        embed.set_thumbnail(url="https://a.ppy.sh/{}_1.png".format(user.id))
        embed.add_field(name="Profile for {}".format(user.name), value="Mode: Taiko", inline=False)
        embed.add_field(name="Player Info", value="Rank: `{}` | pp: `{}` | Accuracy: `{}` | Level: `{}`".format(user.pp_rank, round(user.pp), round(user.accuracy), round(user.level)), inline=False)
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    async def catch(self, ctx, *arg):
        args = ' '.join(arg)
        username = str(args)
        await osuapi.get_user(osutoken, username, mode=2)
        user = osuapi.get_user
        embed=discord.Embed()
        embed.set_thumbnail(url="https://a.ppy.sh/{}_1.png".format(user.id))
        embed.add_field(name="Profile for {}".format(user.name), value="Mode: osu!catch", inline=False)
        embed.add_field(name="Player Info", value="Rank: `{}` | pp: `{}` | Accuracy: `{}` | Level: `{}`".format(user.pp_rank, round(user.pp), round(user.accuracy), round(user.level)), inline=False)
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    async def mania(self, ctx, *arg):
        args = ' '.join(arg)
        username = str(args)
        await osuapi.get_user(osutoken, username, mode=3)
        user = osuapi.get_user
        embed=discord.Embed()
        embed.set_thumbnail(url="https://a.ppy.sh/{}_1.png".format(user.id))
        embed.add_field(name="Profile for {}".format(user.name), value="Mode: osu!mania", inline=False)
        embed.add_field(name="Player Info", value="Rank: `{}` | pp: `{}` | Accuracy: `{}` | Level: `{}`".format(user.pp_rank, round(user.pp), round(user.accuracy), round(user.level)), inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(osu(bot))