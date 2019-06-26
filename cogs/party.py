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
        # Check if there's a party in the channel already
        if ctx.channel.id in self.parties: 
            embed = discord.Embed(description="Party in <@{}> already!".format(ctx.channel.id))
            embed.set_author(icon_url=ctx.author.avatar_url, text="You're missing out {}! There's already a party in here!".format())
            e = await ctx.send(embed=embed)
            await asyncio.sleep(10)
            await e.delete()
            return

        # Setting variables for the embed
        title = "Welcome to the party channel! :tada:"
        colour = ctx.author.colour if hasattr(ctx.author.avatar_url, "colour") else discord.Colour.blurple()
        if celebration:
            message = "This channel is now in party mode, authorized by {0.author.display_name}. They're celebrating {1}!\n\nEnjoy! :tada:".format(ctx, celebration) 
        else:
            message = "This channel is now in party mode, authorized by {0.author.display_name}.\n\nEnjoy! :tada:".format(ctx)

        # Create the embed
        embed = discord.Embed(title=title, description=message)
        embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.display_name+ " just activated PARTY MODE!")

        # Send the embed and message that will be edited as an animation
        emsg = await ctx.send(embed=embed)
        pmsg = await ctx.send("It's time for a party!")

        await asyncio.sleep(5)

        # Set the end time by adding x minutes times 60 (for seconds) to the current time.
        end = time.time() + 5*60
        while time.time() < end:
            await self.animate(pmsg)

        # Remove the channel ID from self.parties.
        async for i in range(len(self.parties)):
            if i == ctx.channel.id:
                del self.parties[i]
                return


    async def animate(self, message):
        '''
        Animate the message by going through 
        '''
        async for f in asyncio.gather(map(lambda x: x, self.frames)):
            await asyncio.sleep(1)
            await message.edit(content=f)



def setup(bot):
    bot.add_cog(Party(bot))