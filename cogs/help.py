import discord, asyncio
from discord.ext import commands

class Help():
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group()
    async def help(self, ctx):
        await ctx.send("""Categories:\r\n
`admin`\r\n
    Commands for server owner/moderator\r\n
\r\n
`furry`\r\n
    Furry related commands\r\n
\r\n
`general`\r\n
    General/fun commands\r\n
\r\n
`osu`\r\n
    osu! related commands\r\n
\r\n
`set`\r\n
    Setting commands for osu! commands\r\n
\r\n
Type `f!help <category>` for more info about each category's command!""")

    @help.command()
    async def admin(self, ctx):
        await ctx.send("""**Admin commands:**\r\n
`role`\r\n
    `set <role name>`\r\n
        Sets a role to user\r\n
    `remove <role name>`\r\n
        Remove a role from user\r\n
\r\n
`purge <number of messages>`\r\n
    Purge/batch delete x messages""")

    @help.command()
    async def furry(self, ctx):
        await ctx.send("""**Furry related commands:**\r\n
`e621 <queries>`\r\n
    Searches e621 with given queries, **NSFW channel only!**\r\n
    \r\n
`e926 <queries>`\r\n
    Same as e621, but only outputs SFW results, can be used in non-NSFW channels\r\n
    \r\n
`show <post id>`\r\n
    Show image from e621/e926 with given post ID\r\n
    \r\n
`randompick`\r\n
    Picks random result from e621 (NSFW channel) or e926 (SFW channel)\r\n
    \r\n
`sofurry <queries>`\r\n
    Searches SoFurry with given queries""")

    @help.command()
    async def general(self, ctx):
        await ctx.send("""**General commands:**\r\n
`about`\r\n
    Sends info about the bot\r\n
\r\n
`help`\r\n
    I believe it brings you here, right? :^)\r\n
\r\n
`report`\r\n
    Reports problem about the bot\r\n
\r\n
`urban`\r\n
    Searches Urban Dictionary with given query\r\n
\r\n
`choose [arg] | [arg] | ...`\r\n
    Chooses one from given arguments""")

def setup(bot):
    bot.add_cog(Help(bot))