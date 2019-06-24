import asyncio
import os

import discord
from discord.ext import commands
from PIL import Image


class WumpusGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx):
        await ctx.send('''**Welcome to the Wumpus Game!**
*Wumpus is stuck on Discord Island and needs help to go free! You need to tell the Discord staff team where to go to save Wumpus!*
Send a pixel location *(using the format 0000x0000)* that is located on Wumpus. You need to find Wumpus and then accurately guess a pixel value that is on him!
*Good luck!~* :tada:''')
        
        # Open images
        wumpus = Image.open(os.path.join('images', 'WumpusLove.png'))
        dmap = Image.open(os.path.join('images', 'DiscordMap.png'))

        embed = discord.Embed(title="Free the Wumpus!", description="The map size is {0}x{1} (width x height). Now quick! Send a pixel location to save Wumpus!".format(dmap.size[0], dmap.size[1]), color=0x42f4ee)
        
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(WumpusGame(bot))
