import discord
import asyncio
from discord.ext import commands
import time

class Party(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.parties = []

        f1 = ":confetti_ball: :large_orange_diamond: :large_blue_diamond: :small_red_triangle_down: PARTY :small_red_triangle:  :large_blue_diamond: :large_orange_diamond: :confetti_ball:"
        f2 = ":confetti_ball: :large_blue_diamond: :large_orange_diamond: :large_blue_diamond: PARTY :large_blue_diamond: :large_orange_diamond: :large_blue_diamond: :confetti_ball:"
        f3 = ":confetti_ball: :small_red_triangle: :large_blue_diamond: :large_orange_diamond: PARTY :large_orange_diamond: :large_blue_diamond: :small_red_triangle_down: :confetti_ball:"
        f4 = ":confetti_ball: :large_blue_diamond: :small_red_triangle: :large_blue_diamond: PARTY :large_blue_diamond: :small_red_triangle_down: :large_blue_diamond: :confetti_ball:"
        f5 = ":confetti_ball: :large_orange_diamond: :large_blue_diamond: :small_red_triangle: PARTY :small_red_triangle_down: :large_blue_diamond: :large_orange_diamond: :confetti_ball:"
        f6 = ":confetti_ball: :large_blue_diamond: :large_orange_diamond: :large_blue_diamond: PARTY :large_blue_diamond: :large_orange_diamond: :large_blue_diamond: :confetti_ball:"
        f7 = ":confetti_ball: :small_red_triangle_down: :large_blue_diamond: :large_orange_diamond: PARTY :large_orange_diamond: :large_blue_diamond: :small_red_triangle: :confetti_ball:"
        f8 = ":confetti_ball: :large_blue_diamond: :small_red_triangle_down: :large_blue_diamond: PARTY :large_blue_diamond: :small_red_triangle: :large_blue_diamond: :confetti_ball:"
        self.frames = [f1, f2, f3, f4, f5, f6, f7, f8]


    @commands.guild_only()
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def party(self, ctx, *, celebration=None):
        '''
        Set a channel to party mode!
        '''
        title = "Welcome to the party channel! :tada:"
        colour = ctx.author.colour if hasattr(ctx.author, 'colour') else discord.Colour.blurple()
        if celebration:
            message = "This channel is now in party mode, authorized by {0.author.display_name}. They're celebrating {1}!\n\nEnjoy! :tada:".format(ctx, celebration) 
        else:
            message = "This channel is now in party mode, authorized by {0.author.display_name}.\n\nEnjoy! :tada:".format(ctx)

        embed = discord.Embed(title=title, description=message)
        embed.set_author(icon_url=ctx.message.author.avatar_url, name=ctx.message.author.display_name+ " just activated PARTY MODE!")

        emsg = await ctx.send(embed=embed)
        pmsg = await ctx.send("It's time for a party!")

        await asyncio.sleep(5)
        end = time.time() + 5*60
        while time.time() < end:
            await self.animate(pmsg)


    async def animate(self, message):
        async for f in asyncio.gather(map(lambda x: x, self.frames)):
            await asyncio.sleep(1)
            await message.edit(content=f)



def setup(bot):
    bot.add_cog(Party(bot))