import discord, osuapi
from discord.ext import commands

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