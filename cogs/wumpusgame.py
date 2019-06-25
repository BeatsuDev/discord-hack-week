import asyncio
import os
import random

import discord
from discord.ext import commands
from PIL import Image


class WumpusGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.land = []


    @commands.command()
    async def play(self, ctx, difficulty="normal"):
        '''Play a game where you save Wumpus from Discord island'''
        msgs = []

        embed = discord.Embed(
            title="**Welcome to the Wumpus Game!**",
            description='''*Wumpus is stuck on Discord Island and needs help to get free! You need to tell the Discord staff team where to go to save Wumpus!*

Tell me where to send the Discord staff by sending x and y coordinates (using the format 0000x0000 and starting from the top left) to where it looks like Wumpus is!
*Good luck!* ***Let's get Wumpus back!*** :tada:''', 
            color=0x50ffff
        )
        
        msgs.append(await ctx.send(embed=embed))

        async with ctx.typing():
            # Open images
            wumpus = Image.open(os.path.join('images', 'WumpusLove.png'))
            if difficulty.lower() == "easy":
                wumpus = wumpus.resize((1200, 1200))
            elif difficulty.lower() == "normal":
                wumpus = wumpus.resize((750, 750))
            elif difficulty.lower() == "hard":
                wumpus = wumpus.resize((500, 500))
            dmap = Image.open(os.path.join('images', 'DiscordMap.png'))

            if not self.land:
                self.land = []
                m = await ctx.send("Hol' up. I just need to load the map. *(This may take a while)*")
                mpxs = dmap.load()
                # Iterate over every width pixel in the map
                for w in range(dmap.size[0]):
                    # Iterate over every height pixel in the map
                    for h in range(dmap.size[1]):
                        # If the average of R and G colour channels are higher than the B colour channel, regard it as land. Also takes away very white pixels
                        if int(sum(mpxs[w, h][:2])/2) > mpxs[w, h][2] and not sum(mpxs[w, h])/3 > 230:
                            self.land.append((w, h))

                await m.delete()

            rland = random.choice(self.land)
            topleftw = rland[0]-int(wumpus.size[0]/2)
            toplefth = rland[1]-wumpus.size[1]  # We want Wumpus to sit on the land
            poffset = (topleftw, toplefth)

            tmp = os.path.join('images', 'temp_map.png')
            dmap.paste(wumpus, poffset, wumpus)
            dmap.save(tmp, 'PNG')

            embed = discord.Embed(title="Free the Wumpus!", description="The map size is {0}x{1} (width x height) and Wumpus' size is {2}x{3}. Now quick! Send a pixel location to save Wumpus!".format(dmap.size[0], dmap.size[1], wumpus.size[0], wumpus.size[1]), color=0x42f4ee)
            msgs.append(await ctx.send(embed=embed))
            msgs.append(await ctx.send(file=discord.File(open(tmp, 'rb'))))

        try:
            msg = await ctx.bot.wait_for('message', check=lambda msg: msg.author == ctx.author, timeout=45)
        except asyncio.TimeoutError:
            errmsg = await ctx.send("Took too long. You need to be fast!")
            [await m.delete() for m in msgs]
            await asyncio.sleep(20)
            await errmsg.delete()
            return

        upx = msg.content.split('x')
        if not len(upx) == 2:
            errmsg = await ctx.send("This doesn't seem to be a valid syntax, please start over again. Use the format **0000x0000**, for example **481x1299**")
            await asyncio.sleep(20)
            [await m.delete() for m in msgs]
            await errmsg.delete()
            return

        try:
            upx = (int(upx[0]), int(upx[1]))
        except TyperError:
            errmsg = await ctx.send("Doesn't seem like you parsed numbers. Use the format **0000x0000**, for example **481x1299**")
            await asyncio.sleep(20)
            [await m.delete() for m in msgs]
            await errmsg.delete()
            return

        uw, uh = upx
        if uw > dmap.size[0] or uh > dmap.size[1]: 
            errmsg = await ctx.send("The pixel you have chosen is out of bounds! Select wone within the specified image size.")
            await asyncio.sleep(20)
            [await m.delete() for m in msgs]
            await errmsg.delete()
            return

        if uw > topleftw and uw < (topleftw+wumpus.size[0]):
            # User point is within wumpus width
            if uh > toplefth and uh < (toplefth+wumpus.size[1]):
                # User point is within wumpus height
                await ctx.send("Congratulations! You saved Wumpus! This is where you sent the discord team:")
            else:
                await ctx.send("That was close! Check out underneath! We *must* save Wumpus!!")

        else:
            await ctx.send("Oh no! You didn't get it right... That was unfortunate. Next time we must save Wumpus! Here was your attempt:")

        target = Image.open(os.path.join('images', 'target.png'))
        poffset = (uw-int(target.size[0]/2), uh-int(target.size[1]/2))
        
        dmap.paste(target, poffset, target)
        dmap.save(tmp, 'PNG')

        await ctx.send(file=discord.File(open(tmp, 'rb')))


def setup(bot):
    bot.add_cog(WumpusGame(bot))
