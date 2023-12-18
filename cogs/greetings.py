from discord.ext import commands

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send('Hello!!!!')

    @commands.command()
    async def bye(self, ctx):
        await ctx.send('Bye!')
        
async def setup(bot):
    await bot.add_cog(Greetings(bot))