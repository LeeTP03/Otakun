from discord.ext import commands
from discord import Embed, ActionRow, ButtonStyle, SelectOption

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send('Hello!!!!')

    @commands.command()
    async def bye(self, ctx):
        await ctx.send('Bye!') 
    
    @commands.command()
    async def commands(self, ctx):
        embed = Embed(title="Commands", description=f"**Prefix is {self.bot.command_prefix}**\nList of commands:", color="0xff0000")
        embed.add_field(name="manga", value="Search for manga", inline=False)
        embed.add_field(name="anime", value="Search for anime", inline=False)
        await ctx.send(embed=embed)
        
        
async def setup(bot):
    await bot.add_cog(Greetings(bot))