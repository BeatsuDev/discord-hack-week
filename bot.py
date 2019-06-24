import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands

# keys.py is in the gitignore file so it does not get uploaded to the github repository
# the api key must stay hidden
from keys import API_KEY

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="f!")
        self.remove_command("help")
        self.add_command(self.help)
        self.add_command(self.ping)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(":ping_pong: Pong!")

    @commands.command()
    async def help(self, ctx):
        message = """Hello! My name is Frizzler! I am a bot created for Discord's Hack Week! 
        
        Prefix: **f!**

        Commands:
        `ping`
        Pings the bot"""

        embed = discord.Embed(description=message)
        embed.set_author(icon_url=ctx.message.author.avatar_url, name=ctx.message.author.display_name + " has requested help!")
        embed.colour = ctx.message.author.colour if hasattr(ctx.message.author, "colour") else discord.Colour.default()
        await ctx.send(embed=embed)

    async def on_ready(self):
        print('Logged in as ' + self.user.name + ' (ID:' + str(self.user.id) + ') | Connected to ' + str(len(self.guilds)) + ' servers | Connected to ' + str(len(set(self.get_all_members()))) + ' users')
        print('--------')
        print('Use this link to invite {}:'.format(self.user.name))
        print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(str(self.user.id)))

        # cogs are loaded here
        # examplecog.py is loaded as 'examplecog'
        # append cogs to the list to load your code
        # ex: cogs = ['examplecog', 'frankscog', 'beatsuscog']
        cogs = ['examplecog', 'wumpusgame']
        for cog in cogs:
            self.load_extension("cogs.{}".format(cog))

# don't touch this
async def run():
    bot = Bot()
    try:
        await bot.start(API_KEY)
    except KeyboardInterrupt:
        await bot.logout()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
