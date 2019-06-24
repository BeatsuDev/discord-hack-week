import asyncio
import os
import random

import discord
from discord.ext import commands
from PIL import Image


class WumpusGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command()
    async def play(self, ctx):
        imsg = await ctx.send('''**Welcome to the Wumpus Game!**
*Wumpus is stuck on Discord Island and needs help to go free! You need to tell the Discord staff team where to go to save Wumpus!*
Send a pixel location *(using the format 0000x0000)* that is located on Wumpus. You need to find Wumpus and then accurately guess a pixel value that is on him!
*Good luck!~* :tada:''')
        
        # Open images
        wumpus = Image.open(os.path.join('images', 'WumpusLove.png'))
        wumpus = wumpus.resize((400, 400))
        dmap = Image.open(os.path.join('images', 'DiscordMap.png'))
        
        mpxs = dmap.load()

        land = []
        
        # Iterate over every width pixel in the map
        for w in range(dmap.size[0]):
            # Iterate over every heigh pixel in the map
            for h in range(dmap.size[1]):
                # If the average of R and G colour channels are higher than the B colour channel, regard it as land
                if int(sum(mpxs[w, h][:2])/2) > mpxs[w, h][2] and not mpxs[w, h] == (255, 255, 255):
                    land.append((w, h))

        rland = random.choice(land)
        topleftw = rland[0]-int(wumpus.size[0]/2)
        toplefth = rland[1]-int(wumpus.size[1]/2)
        poffset = (topleftw, toplefth)

        final = dmap.paste(wumpus, poffset, wumpus)
        final.save(os.path.join('images', 'temp_map.png'), 'PNG')

        embed = discord.Embed(title="Free the Wumpus!", description="The map size is {0}x{1} (width x height). Now quick! Send a pixel location to save Wumpus!".format(dmap.size[0], dmap.size[1]), color=0x42f4ee)
        embed.set_image(os.path.join('images', 'temp_map.png'))
        emsg = await ctx.send(embed=embed)

        def check(msg):
            return msg.author == ctx.author

        msg = await ctx.bot.wait_for('message', check=check, timeout=30)
        upx = msg.content.split('x')
        if not len(upx) == 2:
            errmsg = await ctx.send("This doesn't seem to be a valid syntax, please start over again. Use the format **0000x0000**, for example **481x1299**")
            await asyncio.sleep(10)
            await imsg.delete()
            await emsg.delete()
            await errmsg.delete()
            return

        try:
            upx = (upx[0], upx[1])
        except TyperError:
            errmsg = await ctx.send("Doesn't seem like you parsed numbers. Use the format **0000x0000**, for example **481x1299**")
            await asyncio.sleep(10)
            await imsg.delete()
            await emsg.delete()
            await errmsg.delete()
            return

        uw, uh = upx
        if uw > dmap.size[0] or uh > dmap.size[1]: 
            errmsg = await ctx.send("The pixel you have chose is out of bounds! Select wone within the specified image size.")
            await asyncio.sleep(10)
            await imsg.delete()
            await emsg.delete()
            await errmsg.delete()
            return

        if uw > topleftw and uw < (topleftw+wumpus.size[0]):
            # User point is within wumpus width
            if uh > toplefth and uh < (toplefth+wumpus.size[1]):
                # User point is within wumpus height
                await ctx.send("Congratulations! You saved Wumpus! View the pixel you selected up above.")
            else:
                await ctx.send("That was close! Try again! We *must* save Wumpus!")

        else:
            await ctx.send("Oh no! You didn't get it right... That was unfortunate. Next time we must save Wumpus!")

        target = Image.open(os.path.join('images', 'target.png'))
        poffset = (uw-int(target.size[0]/2), uh-int(target.size[1]/2))
        
        post_game = dmap.paste(target, poffset, target)
        post_game.save(os.path.join('images', 'temp_map.png'), 'PNG')

        embed.set_image(os.path.join('images', 'temp_map.png'))
        await emsg.edit(embed=embed)


def setup(bot):
    bot.add_cog(WumpusGame(bot))
