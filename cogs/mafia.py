import asyncio
import random

import discord
from  discord.ext import commands

# THIS COG IS FAR FROM FINISHED
# This cog has not yet been tested (fml) 


'''
Here goes a feeble attempt at organizing my brain:

`Game`:
    functions:
        kill_player     # Finished
        add_player      # 
        start_game      # Finished
        first_night     # 
        night           # 
        day             # Finished
        choose_player   # 

`MafiaGames`:
    functions:
        find_player_game    # Finished
        find_guild_game     # Finished
        create_game         # Finished

    events:
        on_reaction_add     #
        on_message          #
'''

class AlreadyJoinedError(Exception):
    pass

class AlreadyPlayingError(Exception):
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
        '''
        players {playerIDstr: role, playerIDstr: role}
        dead {playerIDstr: role, playerIDstr: role}

        mafia [playerIDint, playerIDint]
        inv [playerIDint, playerIDint]

        channel     discord.TextChannel
        host        discord.User
        started     bool
        night       bool
        '''
        self.channel = channel
        self.host = host
        self.players = {}
        self.dead = {}
        self.players[host.id] = None

        self.mafia = []
        self.inv = []

        self.started = False
        self.night = False

    # Finished
    async def kill_player(self, userID: int):
        '''
        Kills a player and adds them to the `dead` list 
        '''
        uid = str(userID)
        if not uid in self.players:
            raise PlayerNotFoundError("The player was not found as an alive player in the game.")
        for p in self.players:
            if p == uid:
                self.dead[p] = self.players[p]
                del self.players[p]

            if self.players[p] == "mafia":
                for i in range(len(self.mafia)):
                    if self.mafia[i] == p:
                        del self.mafia[i]

            if self.players[p] == "investigator":
                for i in range(len(self.inv)):
                    if self.inv[i] == p:
                        del self.inv[i]

    # Finished
    async def add_player(self, member):
        '''
        Add a player to the game
        '''
        if len(self.players) >= 20:
            embed = discord.Embed(title="Too many people have already joined!", colour=0xff0000)
            await self.channel.send(embed=embed)

        if self.started: 
            raise AlreadyPlayingError("The game has already started")

        if str(member.id) in self.players:
            raise AlreadyJoinedError("The player is already in the game")

        self.players[member.id] = None

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
                raise NoGameInGuildError("There is no ongoing game in the current guild.")
            
        if self.games[guildID]["started"]:
            raise AlreadyPlayingError("The game has already started.")

        self.games[guildID]["players"][member.name] = None
'''


    # Finished
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
                u = int(p)
                self.mafia.append(u)

            if self.players[p] == "investigator":
                u = int(p)
                self.inv.append(u)

        await self.first_night()
        while self.players > 1:
            if not self.mafia:
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
        self.night = True
        await asyncio.sleep(20)
        # List of `discord.Message` sent to all DMs
        messages = []
        for m in self.mafia:
            u = await self.bot.fetch_user(m)
            votes.append(self.choose_player(channel=u, exclude="mafia"))
        
        votes = []
        for msg in votes:
            # Message Reactions
            mr = []
            for reaction in msg.reactions:
                mr.append(reaction.count)
            votes.append(mr)

        await self.channel.send(f"{killed} was murdered at night.")

    async def day(self):
        '''
        Normal day where villigers vote to lynch a player
        '''
        self.night = False

        letter = list("abcdefghijklmnopqrst")
        await self.channel.send("Good morning! Let the discussion period begin!")
        await asyncio.sleep(30)
        
        desc = ""
        i = 0
        for p in self.players:
            u = await self.bot.fetch_user(int(p))
            desc += f":regional_indicator_{letter[i]}: {u.name}\n"
            i += 1

        embed = discord.Embed(title="Vote for who to lynch", description=desc, colour=discord.Colour.blurple())
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
        
        vals = list(i for i in counts.values())
        if len(vals.count(max(vals))) == 1:
            for k, v in counts.list():
                if v == max(vals):
                    voted = k
        else:
            await self.channel.send("The day is now over. No one was lynched. Good night.")
            return

        rletter = str(voted.name)[-2]
        i = 0
        for l in lenletter:
            if l == rletter:
                # Player ID
                pid = int(list(self.players.items())[i][0])
                # Role
                self.players[list(self.players.items())[i][1]]

                role = embed = discord.Embed()
                u = await self.bot.fetch_user(pid)

                embed.set_author(f"<@{pid}> got lynched!", u.avatar_url)
                embed.add_field("Role:", role)
                await self.channel.send(embed=embed)

                self.kill_player(pid)
            else:
                i += 1
        await self.channel.send("The day is now over. Good night.")


    def choose_player(self, channel, exclude=None):
        '''
        Returns a `discord.Message` object

        The message has already been added the appropriate reactions.
        '''
        players_to_list = []
        if not exclude:
            [players_to_list.append(p) for p in self.players]
        elif exclude == "mafia":
            [players_to_list.append(p) for p in self.players if self.players[p] != "mafia"]
        elif exclude == "investigator":
            [players_to_list.append(p) for p in self.players if self.players[p] != "investigator"]

        letter = list("abcdefghijklmnopqrst")
        desc = ""

        i = 0
        for p in players_to_list:
            u = await self.bot.fetch_user(int(p))
            desc += f":regional_indicator_{letter[i]}: {u.name}\n"
            i += 1

        embed = discord.Embed(title="Vote for a player:", description=desc)
        vote_msg = await channel.send(embed=embed)
        for i in range(len(players_to_list)):
            await vote_msg.add_reaction(f":regional_indicator_{letter[i]}:")
        return vote_msg


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

    # Finished
    def find_player_game(self, user: int):
        game = None
        user = str(user)
        for guildID in self.games:
            if user in self.games[guildID].players:
                game = self.games[guildID]

        return game


    # Finished
    def find_guild_game(self, guildID:int):
        if str(guildID) in self.games:
            return self.games[str(guildID)]
        return None

    # Finished
    def create_game(self, channel=discord.TextChannel, host=discord.Member):
        guild = channel.guild
        if not str(guild.id) in self.games:
            self.games[guild.id] = Game(self.bot, channel, host)
        else:
            raise 


class Mafia(commands.Cog):
    def __init__(self, bot):
        '''
        Manages the events and pretty much just parses everything to `MafiaGames`
        '''
        self.bot = bot
        self.join_msgs = []
        self.game_manager = MafiaGames(bot)


    @commands.command(aliases=['play mafia', 'playm', 'pm'])
    async def playmafia(self, ctx):
        if self.games_manager.find_guild_game(ctx.guild):
            await ctx.send("A game is already running in the server")
            return
        if self.games_manager.find_player_game(ctx.author):
            await ctx.send("You are already in a game")
            return
        if not isinstance(ctx.channel, discord.TextChannel):
            return

        self.game_manager.create_game(ctx.channel, ctx.author)
        embed = discord.Embed(description="Join a game of mafia! Starts in 45 seconds if there are 5-20 players.", colour=ctx.author.colour or discord.Colour.blurple())
        embed.set_author(f"React to join {ctx.author.name}'s game of mafia")
        embed.add_field("Mafia count:", "1")
        embed.add_field("Total players:", "1")
        m = await ctx.send(embed=embed)
        self.join_msgs.append(m.id)
        await asyncio.sleep(45)
        del self.join_msgs[0]


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if not reaction.message in self.join_msgs:
            return
        
        game = (user.guild.id)


    @commands.Cog.listener()
    async def on_message(self, ctx):
        


def setup(bot):
    bot.add_cog(Mafia(bot))