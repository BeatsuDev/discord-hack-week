import discord
import asyncio
from discord.ext import commands

class ExampleCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # commands for your cog go here
    @commands.command()
    async def examplecommand(self, ctx):
        #insert code
        await ctx.send("Hello! You triggered the example command from a cog!")

def setup(bot):
    bot.add_cog(ExampleCog(bot))
