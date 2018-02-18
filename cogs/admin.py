import discord, asyncio
from discord.ext import commands

class Admin():
    def __init__(self, bot):
        self.bot = bot
        
    @commands.group(invoke_without_command=True)
    async def role(self, ctx, userid, *args):
        args = ' '.join(args)
        args = str(args)
        mentions = ctx.message.mentions
        for user in mentions:
            role = discord.utils.get(ctx.guild.roles, name=args)
            await user.add_roles(role)
            await ctx.send("Set role {} for {}!".format(args, user.mention)

def setup(bot):
    bot.add_cog(Admin(bot))