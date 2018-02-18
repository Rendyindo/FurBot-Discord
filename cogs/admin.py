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
            await ctx.send("Set role {} for {}!".format(args, user.mention))

    @role.command()
    async def set(self, ctx, userid, *args):
        args = ' '.join(args)
        args = str(args)
        mentions = ctx.message.mentions
        for user in mentions:
            role = discord.utils.get(ctx.guild.roles, name=args)
            await user.add_roles(role)
            await ctx.send("Set role {} for {}!".format(args, user.mention))

    @role.command()
    async def remove(self, ctx, userid, *args):
        args = ' '.join(args)
        args = str(args)
        mentions = ctx.message.mentions
        for user in mentions:
            role = discord.utils.get(ctx.guild.roles, name=args)
            await user.remove_roles(role)
            await ctx.send("Remove role {} for {}!".format(args, user.mention))


    @commands.command(pass_context = True)
    async def purge(ctx, number):
        number = int(number)
        counter = 0
        async for x in Client.logs_from(ctx.message.channel, limit = number):
            if counter < number:
                await Client.delete_message(x)
                counter += 1
                await asyncio.sleep(0.25)
        await ctx.send("Deleted {} messages!".format(str(number)))

def setup(bot):
    bot.add_cog(Admin(bot))