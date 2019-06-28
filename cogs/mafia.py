import asyncio
import random

import discord
from  discord.ext import commands

# This cog has not yet been tested (fml) 


'''
Here goes a feeble attempt at organizing my brain:

`Game`:
    functions:
        kill_player     # Finished
        add_player      # Finished
        start_game      # Finished
        first_night     # Finished
        nighttime       # Finished
        day             # Finished
        choose_player   # Finished

`MafiaGames`:
    functions:
        find_player_game    # Finished
        find_guild_game     # Finished
        create_game         # Finished

    events:
        on_reaction_add     # Finished
        on_message          # Finished

    commands:
        playmafia           # Finished
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

class GameNotFoundError(Exception):
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

        self.bot = bot

    # Finished
    async def kill_player(self, userID: int):
        '''
        Kills a player and adds them to the `dead` list 
        '''
        uid = userID
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

        if member.id in self.players:
            raise AlreadyJoinedError("The player is already in the game")

        self.players[member.id] = None
        await member.send("You have now been added to the game! There is no way for you to leave now...")


    # Finished
    async def start_game(self):
        '''
        Start the game
        '''
        if len(self.players) < 3:
            raise NotEnoughPlayersError("Not enough players are registered to this class for the game to start")
        
        if len(self.players) > 20:
            raise NotEnoughPlayersError("Too many players are registered to this class for the game to start")

        
        if self.started:
            raise AlreadyPlayingError("The game has already started")
        
        mafia_count = int(len(self.players)/3.5)
        inv_count = int(round(len(self.players)/5, 0))
        vil_count = len(self.players) - mafia_count - inv_count

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
        while len(self.players) > 1:
            if not self.mafia:
                break
            if len(self.mafia) == len(self.players):
                break
            await self.day()
            await self.nighttime()
            
        if self.mafia == len(self.players):
            embed = discord.Embed(colour=0xed6868)
            embed.set_author(name="The mafia won!")
            await self.channel.send(embed=embed)
        else:
            embed = discord.Embed(colour=0xb7e887)
            embed.set_author(name="The villagers won!")
            await self.channel.send(embed=embed)
        

    # Finished
    async def first_night(self):
        '''
        Same as a normal night, just with introduction to role and what to do.
        '''
        for p in self.players:
            u = await self.bot.fetch_user(int(p))
            await u.send(f"You got the role: **{self.players[p]}**\n")
            if self.players[p] == "villager":
                await u.send('''Your job is to lynch suspicious players at day time by convincing others to vote them off. You're a good person!''')
            elif self.players[p] == "investigator":
                await u.send('''Your job is to investigate players at night time. You will be allowed to choose one person every night and will find out whether they are the mafia or not.
Be careful with sharing what you know however! Or else, next night you may be dead.\n\n*(You win with the villagers)*''')
            elif self.players[p] == "mafia":
                await u.send('''Your goal is to kill every non-mafia in the game. Try to stay undetected for as long as you can while silently killing at night.
*There are investigators in the game who can see what crimes you do, so killing them first will help you out.*''')

        await asyncio.sleep(10)
    

    # Finished
    async def nighttime(self):
        '''
        Normal night where mafia choose who to kill and investigators choose who to check
        '''
        self.night = True
        if len(self.mafia) > 1:
            for m in self.mafia:
                u = await self.bot.fetch_user(m)
                await u.send("You may now speak with the other mafia by sending messages here")
        await asyncio.sleep(45)
        # List of `discord.Message` sent to all the mafia's DMs
        messages = []
        for m in self.mafia:
            u = await self.bot.fetch_user(m)
            msgid = await self.choose_player(channel=u, exclude="mafia")
            messages.append(msgid)
        
        # List of `discord.Message` sent to all investigator's DMs
        inv_messages = []
        for i in self.inv:
            u = await self.bot.fetch_user(i)
            msgid = await self.choose_player(channel=u, exclude="investigator")
            inv_messages.append(msgid)

        
        await asyncio.sleep(15)

        # For the mafia
        votes = []
        for msg in messages:
            # Message Reactions
            mr = []
            for reaction in msg.reactions:
                mr.append(reaction.count)
            votes.append(mr)
        
        votes = [sum(i) for i in zip(*votes)]
        if len([a for a in votes if a == max(votes)]) != 1:
            killed = "No one"
        else:
            i = 0
            for p in self.players:
                if self.players[p] == "mafia":
                    continue
                if votes[i] == max(votes):
                    killed = f"<@{p}>" 
                    self.kill_player(int(p))
                    break
                i+=1

        
        # For the investigators
        votes = []
        for msg in votes:
            # Message Reactions
            mr = []
            for reaction in msg.reactions:
                mr.append(reaction.count)
            votes.append(mr)

        votes = [sum(i) for i in zip(*votes)]
        if len([a for a in votes if a == max(votes)]) != 1:
            imsg = "You couldn't decide who to check"
        else:
            i = 0
            for p in self.players:
                if self.players[p] == "investigator":
                    continue
                if votes[i] == max(votes):
                    if self.players[p] == "mafia":
                        imsg = f"<@{p}> ***is a mafia***"
                    else:
                        imsg = f"<@{p}> is **not** a mafia"
        
        for i in self.inv:
            u = await self.bot.fetch_user(i)
            await u.send(imsg)
        await self.channel.send(f"{killed} was murdered at night.")

    
    async def day(self):
        '''
        Normal day where villigers vote to lynch a player
        '''
        self.night = False

        letter = "abcdefghijklmnopqrst"
        regletters = []
        # Regional Indicator A
        reg_A = 0x0001f1e6
        for i in range(20):
            e = f'\\U{base + i :08x}'.encode().decode("unicode-escape")
            regletters.append(e)


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
            await vote_msg.add_reaction({regletters[i]})

        await asyncio.sleep(15)
        counts = {}
        for r in vote_msg.reactions:
            reactions = 0
            async for u in r.users():
                reactions += 1
            counts[r.emoji] = reactions
        
        vals = list(i for i in counts.values())
        if len(vals.count(max(vals))) == 1:
            for k, v in counts.items():
                if v == max(vals):
                    voted = k
        else:
            await self.channel.send("The day is now over. No one was lynched. Good night.")
            return

        for i in range(len(counts)):
            if voted == regletters[i]:
                rletter = letter[i]

        i = 0
        for l in letter:
            if l == rletter:
                # Player ID
                pid = int(list(self.players.items())[i][0])
                # Role
                self.players[list(self.players.items())[i][1]]

                role = embed = discord.Embed()
                u = await self.bot.fetch_user(pid)

                embed.set_author(name=f"<@{pid}> got lynched!", icon_url=u.avatar_url)
                embed.add_field(name="Role:", value=role)
                await self.channel.send(embed=embed)

                self.kill_player(pid)
            else:
                i += 1
        await self.channel.send("The day is now over. Good night.")


    async def choose_player(self, channel, exclude=None):
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
    def find_player_game(self, user: discord.User):
        print("FIND PLAYER GAME IS BEING INVOKED NOW")
        game = None
        try:
            guildID = user.guild.id
        except AttributeError:
            for g in self.games:
                if user.id in self.games[g].players:
                    guildID = g


        for guildID in self.games:
            if user.id in self.games[guildID].players:
                game = self.games[guildID]

        return game


    # Finished
    def find_guild_game(self, guildID:int):
        if guildID in self.games:
            return self.games[guildID]
        return None

    # Finished
    def create_game(self, channel:discord.TextChannel, host:discord.Member):
        guild = channel.guild
        if not guild.id in self.games:
            game = Game(self.bot, channel, host)
            self.games[guild.id] = game
            return game
        else:
            raise AlreadyPlayingError("There is already an ongoing game in the guild")


    def delete_game(self, guildID: int):
        guildID = guildID
        try:
            del self.games[guildID]
        except KeyError:
            raise GameNotFoundError("The game you tried to delete was not found")



class Mafia(commands.Cog):
    def __init__(self, bot):
        '''
        Manages the events and pretty much just parses everything to `MafiaGames`
        '''
        self.bot = bot
        self.join_msgs = []
        self.games_manager = MafiaGames(bot)


    @commands.command(aliases=['play mafia', 'playm', 'pm'])
    async def playmafia(self, ctx):
        if self.games_manager.find_guild_game(ctx.guild.id):
            await ctx.send("A game is already running in the server")
            return
        if self.games_manager.find_player_game(ctx.author):
            await ctx.send("You are already in a game")
            return
        if not isinstance(ctx.channel, discord.TextChannel):
            return

        game = self.games_manager.create_game(ctx.channel, ctx.author)
        
        embed = discord.Embed(description="Join a game of mafia! Starts in 45 seconds if there are 5-20 players.", colour=ctx.author.colour or discord.Colour.blurple())
        embed.set_author(name=f"React to join {ctx.author.name}'s game of mafia", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Mafia count:", value="1")
        embed.add_field(name="Total players:", value="1")
        
        m = await ctx.send(embed=embed)
        await m.add_reaction("✅")
        self.join_msgs.append(m.id)
        
        await asyncio.sleep(20)
        del self.join_msgs[0]

        try:
            await game.start_game()
        except NotEnoughPlayersError:
            embed = discord.Embed(title="Too few people to start", colour=0xff0000)
            await ctx.send(embed=embed)
            self.games_manager.delete_game(ctx.guild.id)

        except TooManyPlayersError:
            embed = discord.Embed(title="Too many people to start", colour=0xff0000)
            await ctx.send(embed=embed)
            self.games_manager.delete_game(ctx.guild.id)
            


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if not isinstance(reaction.message.channel, discord.TextChannel): return
        if not reaction.message.id in self.join_msgs: return
        if user.bot: return
        if reaction.emoji != "✅":
            await reaction.remove(user)
            return
        
        game = self.games_manager.find_guild_game(user.guild.id)
        try:
            if not self.games_manager.find_player_game(user):
                await game.add_player(user)
                embed = reaction.message.embeds[0]
                embed.clear_fields()
                embed.add_field(name="Mafia count:", value=int(len(game.players)/3.5))
                embed.add_field(name="Total players:", value=len(game.players))
                await reaction.message.edit(embed=embed)
            else:
                await user.send("You are already in a game on another server!")
        except AlreadyJoinedError:
            await user.send("You are already in the game!")



    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author == self.bot.user:
            return
        if not isinstance(ctx.channel, discord.DMChannel):
            return
        
        game = self.games_manager.find_player_game(ctx.author)
        if game.night:
            if game.players[ctx.author.id] == "mafia":
                for m in game.players:
                    if game.players[m] == "mafia":
                        u = self.bot.fetch_user(int(m))
                        await u.send(f"**[MAFIA]** `{ctx.author.name + ctx.author.discriminator}`: {ctx.content}")

            elif game.players[ctx.author.id] == "investigator":
                for i in game.players:
                    if game.players[i] == "investigator":
                        u = self.bot.fetch_user(int(i))
                        await u.send(f"**[INVESTIGATOR]** `{ctx.author.name + ctx.author.discriminator}`: {ctx.content}")


def setup(bot):
    bot.add_cog(Mafia(bot))