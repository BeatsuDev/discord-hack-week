import stackexchange
import asyncio
import discord
from discord.ext import commands
from stackauth import StackAuth
from stackexchange import Site, StackOverflow, Sort, DESC
from key import SO_API


class SOverflow(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=['so', 'soverflow'])
    async def stackoverflow(self, ctx):
        so = stackexchange.Site(stackexchange.StackOverflow, SO_API)
        so.impose_throttling = True
        so.throttle_stop = False
        await ctx.send(
        '''
        ```ml
StackOverflow

[1] View user detals
[2] View recent questions
[3] View most recent question
[4] Search for specific questions

Choose an option.
```
        ''')
        def check(msg):
            return msg.author.id == ctx.author.id and msg.content.isdigit()
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=15)
        except asyncio.TimeoutError:
            await ctx.send('''```ml
No option was chosen. Now cancelling.
```''')
        if msg.content == '1':
            await ctx.send('''```ml
Enter a StackOverflow user's ID to view details about them. 
Example: 11167750
```''')
            try:
                msg = await self.bot.wait_for('message', check=check, timeout=30)
            except asyncio.TimeoutError:
                await ctx.send('''```ml
No ID was given. Now cancelling.
```''')     
            user_id = msg.content.strip()
            user = so.user(user_id)
            questions_answers = user.answers.count
            total_questions = len(user.questions.fetch())
            unaccepted_questions = len(user.unaccepted_questions.fetch())
            accepted = total_questions - unaccepted_questions
            rate = 0
            if not total_questions is 0:
                rate = accepted / float(total_questions) * 100
            await ctx.send(f'''```ml
{user.display_name}

Questions Answered: {questions_answers}
Questions Asked: {total_questions}
Unaccepted Questions: {unaccepted_questions}
Accepted Questions: {accepted}
Accept Rate: {rate}%
```''')

        elif msg.content == '2':
            questions = so.recent_questions(pagesize=5)
            question_count = 1
            count = 0
            embed = discord.Embed(
                title='Recent Questions on StackOverflow',
                description='\u200b',
                color=0x7289da
            )
            for question in questions:
                embed.add_field(name=f'{question_count}. {question.title}', value=question.url, inline=False)
                count += 1
                question_count += 1
                if count == 5:
                    await ctx.send(embed=embed)
                    return

        elif msg.content == '3':
            q = so.questions(sort=Sort.Creation, order=DESC)[0]
            await ctx.send(f'''```md
<Title> {q.title}
<URL> {q.url}

< Stats >
<Views> {q.view_count}
<Score> {q.score}
<Answers> {len(q.answers)}
<Tags> {', '.join(q.tags)}
```''')
            return
        
        elif msg.content == '4':
            await ctx.send('''```ml
Enter a question to search.
```''')
            def three_check(msg):
                return msg.author.id == ctx.author.id
            try:
                msg = await self.bot.wait_for('message', check=three_check, timeout=30)
            except asyncio.TimeoutError:
                await ctx.send('''```ml
No question given. Now cancelling.                
''')
            term = str(msg.content).strip()
            qs = so.search(intitle=term, pagesize=5)
            embed = discord.Embed(
                title='Search Results on StackOverflow',
                description='\u200b',
                color=0x7289da
            )
            count = 0
            question_count = 1
            for q in qs:
                embed.add_field(name=f'{question_count}. {q.title}', value=f'{q.url} \u200b', inline=False)
                count += 1
                question_count += 1
                if count == 5:
                    return await ctx.send(embed=embed)
            if count == 0:
                embed = discord.Embed(title=f'Could not find any results for "{term}"', color=0x42f4ee)
                return await ctx.send(embed=embed)
            await ctx.send(embed=embed)
        
        elif msg.content == 'cancel':
            await ctx.send('''```ml
Now cancelling.
```''')
    
    @stackoverflow.error
    async def stackoverflow_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Please give all required arguments.', color=0x42f4ee)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(SOverflow(bot))