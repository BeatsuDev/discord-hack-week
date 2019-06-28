import discord
from googlesearch import search
from discord.ext import commands


class Gsearch(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gsearch(self, ctx, *, query):
        search_results = []
        count = 0
        embed_count = 1
        index = 0
        for i in search(query=query, tld='com', lang='en', num=5, stop=5, pause=0.5):
            search_results.append(i)
            count += 1
        if count == 0:
            embed = discord.Embed(title=f'Could not find any results for "{query}"', color=0x42f4ee)
            return await ctx.send(embed=embed)
        embed = discord.Embed(
            title='Search Results',
            description='\u200b',
            color=0x42f4ee
        )
        while embed_count <= count:
            embed.add_field(name=f'**{embed_count}.** {search_results[index]}', value='\u200b', inline=False)
            embed_count += 1
            index += 1
        await ctx.send(embed=embed)

    @gsearch.error
    async def gsearch_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Please specify what to search.', color=0x42f4ee)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Gsearch(bot))