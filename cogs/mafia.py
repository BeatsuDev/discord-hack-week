import asyncio
import random

import discord
from  discord.ext import commands

# THIS COG IS FAR FROM FINISHED
# This cog has not yet been tested (fml) 


class AlreadyJoinedError(Exception):
    pass

class AlreadyPlayingError(Exception):
    pass

class NoGamesInGuildError(Exception):
    pass

class NotEnoughPlayersError(Exception):
    pass

class TooManyPlayersError(Exception):
    pass

class PlayerNotInGameError(Exception):
    pass

class NoGameInGuildError(Exception):
    pass
        
class PlayerNotFoundError(Exception):
    pass


class Game:
    def __init__(self, bot, channel: discord.TextChannel, host: discord.User):
        self.channel = channel
        self.host = await self.bot.fetch_user(host.id)
        self.players = {}
        self.dead = {}
        self.players[host.id] = None

        self.mafia = []
        self.inv = []

        self.started = False
        self.night = False

    
    async def player_kill(self, user: discord.User):
        if not str(user.id) in self.players:
            raise PlayerNotFoundError("The player was not found as an alive player in the game.")
        for p in self.players:
            if p == str(user.id):
                self.dead[p] = self.players[p]
                del self.players[p]

    async def add_player(self, member):
        if len(self.players) >= 20:
            embed = discord.Embed(title="Too many people have already joined!", colour=0xff0000)
            await self.channel.send(embed=embed)

        if self.started: 
            raise AlreadyPlayingError("The game has already started")


    async def start_game(self):
        '''
        Start the game
        '''
        if len(self.players) < 5:
            embed = discord.Embed(title="Too few people to start", colour=0xff0000)
            await self.channel.send(embed=embed)
            raise NotEnoughPlayersError("Not enough players are registered to this class for the game to start")
        
        if self.started:
            raise AlreadyPlayingError("The game has already started")
        
        mafia_count = int(len(self.players)/3.5)
        inv_count = int(round(len(self.players)/5, 0))
        vil_count = len(self.player) - mafia_count - inv_count

        assignable = []
        [assignable.append("mafia") for i in range(mafia_count)]
        [assignable.append("investigator") for i in range(inv_count)]
        [assignable.append("villager") for i in range(vil_count)]

        random.shuffle(assignable)

        for p in self.players:
            self.players[p] = assignable.pop(0)
            if self.players[p] == "mafia":
                u = await self.bot.fetch_user(int(p))
                self.mafia.append(u)

            if self.players[p] == "investigator":
                u = await self.bot.fetch_user(int(p))
                self.inv.append(u)

        await self.first_night()
        while self.players > 1:
            if self.mafia:
                break
            if len(self.mafia) == len(self.players):
                break
            await self.day()
            await self.night()
            
        if self.mafia == len(self.players):
            embed = discord.Embed(colour=0xed6868)
            embed.set_author("The mafia won!", self.mafia[0].avatar_url)
            await self.channel.send(embed=embed)
        else:
            embed = discord.Embed(colour=0xb7e887)
            embed.set_author("The villagers won!", self.players[0].avatar_url)
            await self.channel.send(embed=embed)
        


    async def first_night(self):
        '''
        Same as a normal night, just with introduction to role and what to do.
        '''
        pass
    

    async def night(self):
        '''
        Normal night where mafia choose who to kill and investigators choose who to check
        '''
        pass

    async def day(self):
        '''
        Normal day where villigers vote to lynch a player
        '''
        letter = list("abcdefghijklmnopqrst")
        await self.channel.send("Discussion period!")
        await asyncio.sleep(30)
        
        desc = ""
        i = 0
        for p in self.players:
            u = await self.bot.fetch_user(int(p))
            desc += f":regional_indicator_{letter[i]}: {u.display_name}\n"
            i += 1

        embed = discord.Embed(description=desc, colour=discord.Colour.blurple())
        vote_msg = await self.channel.send(embed=embed)
        for i in range(len(self.players)):
            await vote_msg.add_reaction(f":regional_indicator_{letter[i]}:")

        await asyncio.sleep(15)
        counts = {}
        for r in vote_msg.reactions:
            reactions = 0
            async for u in r.users():
                reactions += 1
            counts[str(r.emoji)] = reactions


class MafiaGames:
    def __init__(self, bot):
        '''
        Manages all games run on the bot

        self.games {
            guildID: `Frizzler.cogs.Game`,
            guildID: `Frizzler.cogs.Game`,
            guildID: 'Frizzler.cogs.Game`
        }
        '''
        self.bot = bot
        self.games = {}
    
    def add_player(self, member: discord.Member):
        '''
        Add a player to a guild game
        '''
        player = member
        playerID = str(member.id)
        guild = member.guild
        guildID = str(guild.id)

        try:
            _ = self.games[guildID]["players"][playerID]
            raise AlreadyJoinedError("This player is already in the game.")
        except KeyError:
            if not guildID in self.games:
                raise NoGamesInGuildError("There is no ongoing game in the current guild.")
            
        if self.games[guildID]["started"]:
            raise AlreadyPlayingError("The game has already started.")

        self.games[guildID]["players"][member.name] = None


    def find_player_game(self, member: discord.Member):
        return game
        return None


    async def find_guild_game(self, guild=discord.Guild):
        return game
        return None


class Mafia(commands.Cog):
    def __init__(self, bot):
        '''
        Manages the events and pretty much just parses them to `MafiaGames`
        '''
        self.bot = bot
        self.join_msgs = {}


    @commands.command(aliases=['play mafia', 'playm', 'pm'])
    async def playmafia(self, ctx):
        self.active_guilds.append(ctx.guild.id)
        try:
            embed = discord.Embed(description="Join a game of mafia!", colour=ctx.author.colour or discord.Colour.blurple())
            embed.set_author(f"React to join {ctx.author.name}'s game of mafia")
            embed.add_field("Mafia count:", "1")
            embed.add_field("Total players:", "1")
            m = await ctx.send(embed=embed)
            self.join_msgs[m.id] = ctx.guild.id
        except asyncio.TimeoutError:
            await m.delete()
            errmsg = await ctx.send("")


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if str(reaction.message.id) in self.join_msgs:
            self.active_users.append()


    @commands.Cog.listener()
    async def on_message(self, ctx):
        


def setup(bot):
    bot.add_cog(Mafia(bot))