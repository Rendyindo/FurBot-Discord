import discord, asyncio
from discord.ext import commands

class Admin():
    """The admin commands, for server moderator/owner

    Commands:
        purge      Purge x number of messages
        role       Sets a role to a user"""
    def __init__(self, bot):
        self.bot = bot
        
    @commands.group(invoke_without_command=True)
    async def role(self, ctx, userid, *args):
        """Sets a role to a user
        
        Usage: f!role @user <role name>"""
        permissions = dict(iter(ctx.message.channel.permissions_for(ctx.message.author)))
        if not permissions['manage_roles']:
            await ctx.send("You need 'Manage roles' permission to do this!")
            return
        args = ' '.join(args)
        args = str(args)
        mentions = ctx.message.mentions
        for user in mentions:
            role = discord.utils.get(ctx.guild.roles, name=args)
            await user.add_roles(role)
            await ctx.send("Set role {} for {}!".format(args, user.mention))

    @role.command()
    async def set(self, ctx, userid, *args):
        """Sets a role to a user
        
        Usage: f!role set @user <role name>"""
        permissions = dict(iter(ctx.message.channel.permissions_for(ctx.message.author)))
        if not permissions['manage_roles']:
            await ctx.send("You need 'Manage roles' permission to do this!")
            return
        args = ' '.join(args)
        args = str(args)
        mentions = ctx.message.mentions
        for user in mentions:
            role = discord.utils.get(ctx.guild.roles, name=args)
            await user.add_roles(role)
            await ctx.send("Set role {} for {}!".format(args, user.mention))

    @role.command()
    async def remove(self, ctx, userid, *args):
        """Removes a role from a user
        
        Usage: f!role remove @user <role name>"""
        permissions = dict(iter(ctx.message.channel.permissions_for(ctx.message.author)))
        if not permissions['manage_roles']:
            await ctx.send("You need 'Manage roles' permission to do this!")
            return
        args = ' '.join(args)
        args = str(args)
        mentions = ctx.message.mentions
        for user in mentions:
            role = discord.utils.get(ctx.guild.roles, name=args)
            await user.remove_roles(role)
            await ctx.send("Remove role {} for {}!".format(args, user.mention))


    @commands.command(pass_context=True)
    async def purge(self, ctx, number):
        """Purge x number of messages
        
        Usage: f!purge <number of messages>"""
        permissions = dict(iter(ctx.message.channel.permissions_for(ctx.message.author)))
        if not permissions['manage_messages']:
            await ctx.send("You need 'Manage Messages' permission to do this!")
            return
        if not number:
            ctx.send("Please input amount of messages you want to delete!")
        try:
            number = int(number)
        except:
            ctx.send("Uhmm, it's in number (int), not text (str).")
            return
        counter = 0
        async for x in ctx.history(limit = number, before = ctx.message):
            if counter < number:
                await x.delete()
                counter += 1
                await asyncio.sleep(0.25)
        await ctx.send("Deleted {} messages!".format(str(number)))

def setup(bot):
    bot.add_cog(Admin(bot))