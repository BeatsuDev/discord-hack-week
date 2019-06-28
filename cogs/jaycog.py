import discord
import asyncio
from discord.ext import commands
from discord import FFmpegPCMAudio
import random


class JayCog(commands.Cog):

    client = discord.Client()

    def __init__(self, bot):
        self.bot = bot
        self.bot_message = None
        self.ready = None

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

    @commands.command(aliases=["pt", "piano", "playpiano"])
    async def pianotime(self, ctx):
        self.ready = False
        try:
            vc = ctx.message.author.voice.channel
            self.vcl = await vc.connect()
        except:
            embed = discord.Embed(colour=0xff0000)
            embed.set_author(icon_url=ctx.message.author.avatar_url, name=ctx.message.author.display_name + ", you're not in a vc! Please connect to one before playing the piano")
            await ctx.send(embed=embed)
            return

        self.notes = ['🎹', '🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬']
        msg = """Heyy {} it's Piano Time! It's Discord's Hack Week, Let's get Frizzy! 
        
        Reactions: 
        :musical_keyboard:
        :regional_indicator_a:
        :regional_indicator_b:
        :regional_indicator_c:
        :regional_indicator_d:
        :regional_indicator_e:
        :regional_indicator_f:
        :regional_indicator_g:

        React to this message to play!""".format(ctx.message.author.display_name)
        embed = discord.Embed(description=msg)
        embed.set_author(icon_url=ctx.message.author.avatar_url, name=ctx.message.author.display_name + " brought a piano!")
        embed.colour = ctx.message.author.colour if hasattr(ctx.message.author, "colour") else discord.Colour.default()
        self.bot_message = await ctx.send(embed=embed)

        for note in self.notes:
            await self.bot_message.add_reaction(note)

        
        
        source = FFmpegPCMAudio('music/better sounds/call_ringing_beat.wav')
        self.vcl.play(source)
        await ctx.send("You will be able to play in just a sec ;)")
        await asyncio.sleep(12)
        self.ready = True
    
    @commands.command(aliases=["stop"])     
    async def pianostop(self, ctx):
        await self.vcl.disconnect()


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if not reaction.message == self.bot_message and not self.ready:
            return
        
        if reaction.emoji not in self.notes:
            await reaction.delete()

        if not user.voice.channel.id:
            embed = discord.Embed(colour=0xff0000)
            embed.set_author(icon_url=user.avatar_url, name=user.display_name + ", you're not in a vc! Please connect to one before playing the piano")
            await reaction.message.channel.send(embed=embed)

        try:
            if reaction.emoji == "🎹":
                g3 = FFmpegPCMAudio('music/better sounds/c5.wav')
                self.vcl.play(g3)

            elif reaction.emoji == "🇦":
                a4 = FFmpegPCMAudio('music/better sounds/d5.wav')
                self.vcl.play(a4)

            elif reaction.emoji == "🇧":
                b4 = FFmpegPCMAudio('music/better sounds/e5.wav')
                self.vcl.play(b4)

            elif reaction.emoji == "🇨":
                c4 = FFmpegPCMAudio('music/better sounds/f5.wav')
                self.vcl.play(c4)

            elif reaction.emoji == "🇩":
                d4 = FFmpegPCMAudio('music/better sounds/g5.wav')
                self.vcl.play(d4)

            elif reaction.emoji == "🇪":
                e4 = FFmpegPCMAudio('music/better sounds/a6.wav')
                self.vcl.play(e4)

            elif reaction.emoji == "🇫":
                f4 = FFmpegPCMAudio('music/better sounds/b6.wav')
                self.vcl.play(f4)

            elif reaction.emoji == "🇬":
                g4 = FFmpegPCMAudio('music/better sounds/c6.wav')
                self.vcl.play(g4)
        except discord.errors.ClientException:
            pass


    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if not reaction.message == self.bot_message and not self.ready:
            return

        if not user.voice.channel.id:
            embed = discord.Embed(colour=0xff0000)
            embed.set_author(icon_url=user.avatar_url, name=user.display_name + "You're not in a vc! Please connect to one before playing the piano")
            await reaction.message.channel.send(embed=embed)
        try:
            if reaction.emoji == "🎹":
                c5 = FFmpegPCMAudio('music/better sounds/c5.wav')
                self.vcl.play(c5)

            elif reaction.emoji == "🇦":
                d5 = FFmpegPCMAudio('music/better sounds/d5.wav')
                self.vcl.play(d5)

            elif reaction.emoji == "🇧":
                e5 = FFmpegPCMAudio('music/better sounds/e5.wav')
                self.vcl.play(e5)

            elif reaction.emoji == "🇨":
                f5 = FFmpegPCMAudio('music/better sounds/f5.wav')
                self.vcl.play(f5)

            elif reaction.emoji == "🇩":
                g5 = FFmpegPCMAudio('music/better sounds/g5.wav')
                self.vcl.play(g5)

            elif reaction.emoji == "🇪":
                a6 = FFmpegPCMAudio('music/better sounds/a6.wav')
                self.vcl.play(a6)

            elif reaction.emoji == "🇫":
                b6 = FFmpegPCMAudio('music/better sounds/b6.wav')
                self.vcl.play(b6)

            elif reaction.emoji == "🇬":
                c6 = FFmpegPCMAudio('music/better sounds/c6.wav')
                self.vcl.play(c6)
        except discord.errors.ClientException:
            pass
        

        
def setup(bot):
    bot.add_cog(JayCog(bot))
