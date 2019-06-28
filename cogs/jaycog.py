import discord
import asyncio
from discord.ext import commands
from discord import FFmpegPCMAudio
import random


class JayCog(commands.Cog):

    client = discord.Client()

    def __init__(self, bot):
        self.bot = bot

    # commands for your cog go here
    @commands.command()
    async def rps(self, ctx, rlt : str):
        possible = ["rock", "paper", "scissors"]
        r_choice = random.choice(possible)
        if rlt:
            if rlt == 'rock':
                if r_choice == 'paper':
                    await ctx.send('I won! I picked '+r_choice)
                elif r_choice == 'scissors':
                    await ctx.send('I lost :( I picked '+r_choice)

            elif rlt == 'paper':
                if r_choice == 'rock':
                    await ctx.send('I lost :( I picked '+r_choice)
                elif r_choice == 'scissors':
                    await ctx.send('I won! I picked '+r_choice)

            elif rlt == 'scissors':
                if r_choice == 'rock':
                    await ctx.send('I won! I picked '+r_choice)
                elif r_choice == 'paper':
                    await ctx.send('I lost :( I picked '+r_choice)

            elif rlt == r_choice:
                await ctx.send('Draw!')
            else:
                await ctx.send('You must write rock, paper or scissors')
        else:
            await ctx.send('You must write rock, paper or scissors')

    @commands.command()
    async def pianotime(self, ctx):
        global vcl
        vc = ctx.message.author.voice.channel
        notes = {'⚽', '🏀', '🏈', '⚾', '🎾', '🏐'}
        msg = """Heyy {} it's Piano Time! It's Discord's Hack Week, Let's get Frizzy! 
        
        Reactions: 
        :soccer:
        :basketball:
        :football:
        :baseball:
        :tennis:
        :volleyball:
        How it works:

        React to this message to play!""".format(ctx.message.author.display_name)
        embed = discord.Embed(description=msg)
        embed.set_author(icon_url=ctx.message.author.avatar_url, name=ctx.message.author.display_name + " brought a piano!")
        embed.colour = ctx.message.author.colour if hasattr(ctx.message.author, "colour") else discord.Colour.default()
        bot_message = await ctx.send(embed=embed)
        for note in notes:
            await bot_message.add_reaction(note)
        if not vc:
            await ctx.send("You are not connected to a voice channel!")
            return
        else:
            vcl = await vc.connect()
            source = FFmpegPCMAudio('music/a4.wav')
            player = vcl.play(source)
            player.start()
            rea = on_reaction_add()
            await print(rea.emoji)
    @commands.command()     
    async def pianostop(self, ctx):
        global vcl
        await vcl.disconnect()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, ctx):
            source = FFmpegPCMAudio('music/a4.wav')
            player = vcl.play(source)
            await print(reaction.emoji)
        

        
def setup(bot):
    bot.add_cog(JayCog(bot))
