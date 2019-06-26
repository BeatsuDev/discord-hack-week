import datetime
import json
import os
import time
import asyncio

import aiofiles
import discord
from discord.ext import commands


class SpecialDay(commands.Cog):

    def __init__(self, bot):
        '''
        A cog to set special days and get notified when it's a special day. 
        Contains the following commands:
            - `specialday`, aliases= `sd`
            - `addevent`, aliases= `aevent`, `eventadd`, `ae`
            - `removeevent`, aliases= `revent`, `eventremove`, `re`
            - `viewevents`, aliases= `events`, `days`
            - `setchannel`, aliases= `channelset`
        '''
        self.bot = bot
        self.loop = asyncio.get_event_loop()
        self.jfile = os.path.join(os.getcwd(), 'data', 'events.json')

        # Create data directory if it does not exist
        direc = self.jfile = os.path.join(os.getcwd(), 'data')
        if not os.path.isdir(direc): os.mkdir(direc)

        # Create json file if it does not exist or is empty
        if not os.path.isfile(self.jfile) and os.path.getsize(self.jfile) > 0:
            data = {}
            data["guilds"] = {}
            with open(self.jfile, "w") as f:
                json.dump(data, f)
                f.close()

        '''
        JSON structure:
        "guilds": {
            guildID: {
                "channel": channel,
                "events": {
                    event_name: {
                        "title": name,
                        "date": date
                    },
                    event_name2: {
                        "title": name,
                        "date": date
                    }
                }
            },
        }
        '''


    @commands.guild_only()
    @commands.command(aliases=['sd'])
    async def specialday(self, ctx):
        '''
        Help command for the special days module
        ''' 
        # Create available commands embed
        embed = discord.Embed(
            title='Available Commands',
            description='Say a command followed by the parameters.',
            color=discord.Colour.blurple()
        )
        # Add a field for every command
        embed.add_field(name='f!setchannel <#channel>', value='Use this command to set what channel special days are notified in.')
        embed.add_field(name='f!addevent <day> <name>', value='Add a special day, please use MM/DD/YYYY format.', inline=False)
        embed.add_field(name='f!removeevent <day>', value='Remove a special day, please use MM/DD/YYYY format.', inline=False)
        embed.add_field(name='f!viewevent', value='View all special days.', inline=False)
        await ctx.send(embed=embed)

        # Warn the user if they don't have admin privileges
        if not ctx.author.permissions_in(channel=ctx.channel).administrator:
            embed = discord.Embed(title='You require admin privileges permission to use most of these commands.', color=0xff0000)
            await ctx.send(embed=embed)


    @commands.guild_only()
    @commands.command(aliases=['aevent', 'eventadd', 'ae'])
    @commands.has_permissions(administrator=True)
    async def addevent(self, ctx, day, *, name: str = None):
        '''
        Add a special day. Use the `MM/DD/YYYY` format.
        '''
        today = datetime.datetime.now().strftime("%m/%d/%Y")

        # Check if the day is valid
        if len(day) != 10 or False in list(map(lambda part: part.isdigit(), day.split("/"))):
            embed = discord.Embed(title=f'Please use the format MM/DD/YYYY for the date. Example: {today}', color=0xff0000)
            await ctx.send(embed=embed)
            return

        # Check if there is a name for the event
        if not name:
            embed = discord.Embed(title='Please enter a name for the event', color=0xff0000)
            await ctx.send(embed=embed)
            return

        # Set the event data (which is to be put in the events["guilds"]["events"] dict)
        event_data = {
            name.lower(): {
                "set": time.time(),
                "set_by": ctx.message.author.id,
                "name": name,
                "date": day
            }
        }

        # Create embed for successfull addition of event
        embed = discord.Embed(color=0x00ff00)
        embed.set_author(name=f'{ctx.author.display_name} sucessfully added a special day!', icon_url=ctx.author.avatar_url)
        embed.add_field(name='Title', value=name, inline=True)
        embed.add_field(name='Date', value=day, inline=True)
        await ctx.send(embed=embed)
        
        # Load data from json file
        async with aiofiles.open(self.jfile, mode='r') as f:
            data = json.loads(await f.read())
            await f.close()

        # Check if events are already registered in this guild
        if ctx.guild.id in data["guilds"]:
            data["guilds"]["events"][name.lower()] = event_data[name.lower()]

        else:
            data["guilds"][ctx.guild.id] = {}
            data["guilds"][ctx.guild.id]["events"] = {}
            data["guilds"]["events"][name.lower()] = event_data[name.lower()]

        # Dump data into file
        async with aiofiles.open(self.jfile, mode="w") as f:
            await f.write(json.dumps(data))
            await f.close()
    
    @commands.guild_only()
    @commands.command(aliases=['revent', 'eventremove', 're'])
    @commands.has_permissions(administrator=True)
    async def removeevent(self, ctx, name):
        '''
        Remove a special day.
        '''
        # Load data
        async with aiofiles.open(self.jfile, mode='r') as f:
            data = json.loads(await f.read(f))
            await f.close()

        # Set the embed straight away as it will be used in the following two if statements
        embed = discord.Embed(title='There are no speical days added yet.', color=0xff0000)

        # Check if the guild is registered
        if not ctx.guild.id in data["guilds"]:
            await ctx.send(embed=embed)
            return

        # Check if there are no registered events
        if not data["guilds"][ctx.guild.id]["events"]:
            await ctx.send(embed=embed)
            return
        
        # Check if an event with the given name exists
        events = data["guilds"][ctx.guild.id]["events"]
        if name.lower() in events:
            # Delete the event
            del events[name.lower()]

            # Create the embed for a successfull delete
            embed = discord.Embed(colour=0x00ff00)
            embed.set_author(name=f'{author.display_name} has successfully removed a special day.', icon_url=author.avatar_url)
            embed.add_field(name='Title', value=data_title, inline=True)
            embed.add_field(name='Date', value=data_day, inline=True)
            await ctx.send(embed=embed)
            return
        else:
            # Create the embed for if the event is not found
            embed = discord.Embed(colour=0xff0000)
            embed.set_author(name='The event you tried to remove was not found.')
            await ctx.send(embed=embed)
            return
    
    @commands.guild_only()
    @commands.command(aliases=['events', 'days'])
    async def viewevents(self, ctx):
        '''
        View all events that is set in the guild
        '''
        # Load data
        async with aiofiles.open(self.jfile, mode='r') as f:
            data = json.loads(await f.read(f))
            await f.close()

        # Set the embed straight away as it will be used in the following two if statements
        embed = discord.Embed(title='There are no speical days added yet.', color=0xff0000)

        # Check if the guild is registered
        if not ctx.guild.id in data["guilds"]:
            await ctx.send(embed=embed)
            return

        # Check if there are no registered events
        if not data["guilds"][ctx.guild.id]["events"]:
            await ctx.send(embed=embed)
            return

        # Creating embed to show all registered events 
        embed = discord.Embed(title='Special Days', color=discord.Colour.blurple())
        events = data["guilds"][ctx.guild.id]["events"]
        for event in events:
            name = event["name"]
            date = event["date"]
            embed.add_field(name=name, value=date, inline=True)
        await ctx.send(embed=embed)
    
    @commands.guild_only()
    @commands.command(aliases=['channelset'])
    @commands.has_permissions(administrator=True)
    async def setchannel(self, ctx, channelset):
        '''
        Set the channel in which you will get notified of the special day!
        '''
        if channelset.lower() == "None":
            embed = discord.Embed(title="This guild will no longer be notified about events.", colour=0xffff00)
            await ctx.send(embed=embed)
            return

        # We want to be able to work with the channel id which will lie between <# and >
        if not channelset or not (channelset.beginswith("<#") and channelset.endswith(">")):
            embed = discord.Embed(title="Please enter the channel you want events to be posted in by tagging it with the `#` symbol, like this: <#{0.channel.id}>".format(ctx))
            await ctx.send(embed=embed)
            return

        # Load data
        async with aiofiles.open(self.jfile, mode='r') as f:
            data = json.loads(await f.read(f))
            await f.close()

        # Change data
        data["guilds"][ctx.guild.id]["channel"] = int(channelset[2:-1])

        # Save data
        async with aiofiles.open(self.jfile, "w") as f:
            await f.write(json.dumps(data))
            await f.close()

        # Create embed for success message
        embed = discord.Embed(description=f'<#{channelID}> will now be used for all special day notifications.', colour=0x00ff00)
        embed.set_author(name=f'{author.display_name} has successfully changed the special day notification channel.', icon_url=author.avatar_url)
        await ctx.send(embed=embed)


    # Error handling
    @addevent.error
    async def add_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Please give all required arguments.', colour=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title='You do not have permission to use this command.', colour=0xff0000)
            await ctx.send(embed=embed)
        else:
            print(error)

    @removeevent.error
    async def remove_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Please give all required arguments.', colour=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title='You do not have permission to use this command.', colour=0xff0000)
            await ctx.send(embed=embed)
        else:
            print(error)
    
    @setchannel.error
    async def setchannel_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Please give all required arguments.', colour=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title='You do not have permission to use this command.', colour=0xff0000)
            await ctx.send(embed=embed)
        else:
            print(error.traceback)


def setup(bot):
    bot.add_cog(SpecialDay(bot))
