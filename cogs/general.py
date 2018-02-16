import discord
from discord.ext import commands
import asyncio, aiohttp

@bot.command(pass_context=True)
async def avatar(ctx, message):
    mentions = ctx.message.mentions
    for user in mentions:
        avatarurl = user.avatar_url
        await ctx.send("Avatar URL for " + user.mention + """\r
""" + avatarurl)

@bot.command(pass_context=True)
async def urban(ctx, *args):
    args = ' '.join(args)
    args = str(args)
    apilink = "http://api.urbandictionary.com/v0/define?term=" + args
    async with aiohttp.ClientSession() as session:
        async with session.get(apilink, headers=headers) as r:
            if r.status == 200:
                datajson = await r.json()
            else:
                print("Invalid HTTP Response:" + str(r.status))
                raise InvalidHTTPResponse()
    listcount = 0
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

@bot.command()
async def about(ctx):
    embed=discord.Embed(color=0x0089ff)
    embed.add_field(name=Developer, value="Error-", inline=False)
    embed.add_field(name=Library, value=discord.py, inline=False)
    embed.add_field(name="Support Server", value="https://discord.gg/YTEeY9g", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def report(ctx, *args):
    args = ' '.join(args)
    message = str(args)
    with open("reports.log", "w") as text_file:
        text_file.write(message)
    await ctx.send("Thanks for your input! I've notified my owner about it~")
    user = bot.get_user(int(owner))
    await user.send("""New report:\r
```""" + message + "```")

@bot.command()
async def choose(ctx, *args):
    args = ' '.join(args)
    args = str(args)
    choices = args.split('|')
    if len(choices) < 2:
        await ctx.send("You need to send at least 2 argument!")
        return
    await ctx.send(random.choice(choices) + ", of course!")