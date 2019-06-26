import datetime
import json
import os
import discord
from discord.ext import commands


class SpecialDay(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command()
    async def specialday(self, ctx):
        author = ctx.message.author
        channel = ctx.message.channel
        now = datetime.datetime.now()
        now = now.strftime("%m/%d/%Y")
        if author.permissions_in(channel=channel).administrator is True:
            day_embed = discord.Embed(
                title='Available Commands',
                description='Say a command followed by the parameters.',
                color=0x42f4ee
            )
            day_embed.add_field(name='f!setchannel <#channel>', value='Use this command to set what channel special days are notified in.')
            day_embed.add_field(name='f!add <day> <name>', value='Add a special day, please use MM/DD/YYYY format.', inline=False)
            day_embed.add_field(name='f!remove <day>', value='Remove a special day, please use MM/DD/YYYY format.', inline=False)
            day_embed.add_field(name='f!view', value='View all special days.', inline=False)
            await ctx.send(embed=day_embed)
        else:
            embed = discord.Embed(title='You do not have permission to use this command.', color=0x42f4ee)
            await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, day, *, name: str = None):
        author = ctx.message.author
        guild = ctx.guild
        now = datetime.datetime.now()
        now = now.strftime("%m/%d/%Y")
        jfile = os.path.join(os.getcwd(), 'data', 'specialdays.json')
        if len(day) != 10:
            embed = discord.Embed(
                title=f'Please use MM/DD/YYYY format for date. Example: {now}',
                color=0x42f4ee
            )
            await ctx.send(embed=embed)
            return
        if name is None:
            embed = discord.Embed(
                title='Please give a name for the day.',
                color=0x42f4ee
            )
            await ctx.send(embed=embed)
            return
        data = {}
        data['guilds'] = []
        data['guilds'].append(
            {
                str(guild): 
                {
                    'date': day, 
                    'title': name
                }
            }
        )
        embed = discord.Embed(
            color=0x42f4ee
        )
        embed.set_author(name=f'{author.display_name} has added a special day.', icon_url=author.avatar_url)
        embed.add_field(name='Title', value=name, inline=True)
        embed.add_field(name='Date', value=day, inline=True)
        num = 0
        with open(jfile, 'r') as r:
            data_load = json.load(r)
            for server in data['guilds']:
                if str(guild) in server:
                    num += 1
        if num == 0:
            with open(jfile, 'w') as f:
                json.dump(data, f, indent=4)
            await ctx.send(embed=embed)
        else:
            tdata = json.load(open(jfile, 'r'))
            for g in data['guilds']:
                tdata['guilds'].append(g)
            json.dump(tdata, open(jfile, 'w'), indent=4)
            await ctx.send(embed=embed)
    
    @commands.guild_only()
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx, date):
        author = ctx.message.author
        channel = ctx.message.channel
        guild = self.bot.get_guild(ctx.guild.id)
        now = datetime.datetime.now()
        now = now.strftime("%m/%d/%Y")
        jfile = os.path.join(os.getcwd(), 'data', 'specialdays.json')
        if len(date) != 10:
            embed = discord.Embed(
                title=f'Please use MM/DD/YYYY format for date. Example: {now}',
                color=0x42f4ee
            )
            await ctx.send(embed=embed)
            return
        count = 0
        with open(jfile, 'r') as f:
            data = json.load(f)
            for server in data['guilds']:
                if str(guild) in server:
                    count += 1
                    g = server.get(str(guild))
                    for _ in g:
                        data_day = g.get('date')
                        data_title = g.get('title')
                        if date == data_day:
                            embed = discord.Embed(color=0x42f4ee)
                            embed.set_author(name=f'{author.display_name} has removed a special day.', icon_url=author.avatar_url)
                            embed.add_field(name='Title', value=data_title, inline=True)
                            embed.add_field(name='Date', value=data_day, inline=True)
                            del g['date']
                            del g['title']
                            with open(jfile, 'w') as f:
                                json.dump(data, f, indent=4)
                            await ctx.send(embed=embed)
                            return
            if count == 0:
                embed = discord.Embed(title='There are no speical days added yet.', color=0x42f4ee)
                await ctx.send(embed=embed)
    
    @commands.guild_only()
    @commands.command()
    async def view(self, ctx):
        jfile = os.path.join(os.getcwd(), 'data', 'specialdays.json')
        guild = self.bot.get_guild(ctx.guild.id)
        num = 0
        with open(jfile, 'r') as f:
            data = json.load(f)
            for g in data['guilds']:
                if str(guild) in g:
                    for _ in g.get(str(guild)):
                        num += 1
        if num == 0:
            embed = discord.Embed(title='There are no speical days added yet.', color=0x42f4ee)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='Special Days', color=0x42f4ee)
            with open(jfile, 'r') as f:
                data = json.load(f)
                for day in data['days']:
                    data_day = day.get('date')
                    data_title = day.get('title')
                    embed.add_field(name=data_title, value=data_day, inline=True)
            await ctx.send(embed=embed)
    
    @commands.guild_only()
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setchannel(self, ctx, channelset):
        channel = ctx.message.channel
        author = ctx.messge.author
        guild = ctx.guild
        channel_id = ''
        channelset = str(channelset[2:-1])
        set_channel = ''
        jfile = os.path.join(os.getcwd(), 'data', 'specialdaysconfig.json')
        data = {}
        data['channels'] = []
        data['channels'].append(
            {
                'channel': channelset
            }
        )
        with open(jfile, 'w') as f:
            json.dump(data, f, indent=4)
        with open(jfile, 'r') as f:
            for g in data['channels']:
                set_thing = g.get('channel')
                channel_id = set_thing
                set_channel = self.bot.get_channel(int(set_thing))
        embed = discord.Embed(
            description=f'<#{channel_id}> will now be used for all special day notifications.',
            color=0x42f4ee
        )
        embed.set_author(
            name=f'{author.display_name} has changed the special day notification channel.',
            icon_url=author.avatar_url
        )
        await ctx.send(embed=embed)

    @add.error
    async def add_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Please give all required arguments.', color=0x42f4ee)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title='You do not have permission to use this command.', color=0x42f4ee)
            await ctx.send(embed=embed)

    @remove.error
    async def remove_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Please give all required arguments.', color=0x42f4ee)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title='You do not have permission to use this command.', color=0x42f4ee)
            await ctx.send(embed=embed)
    
    @setchannel.error
    async def setchannel_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Please give all required arguments.', color=0x42f4ee)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title='You do not have permission to use this command.', color=0x42f4ee)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(SpecialDay(bot))
