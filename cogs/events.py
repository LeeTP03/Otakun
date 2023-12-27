from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"We have logged in as {self.bot.user}")
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return    
        
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user == self.bot.user:
            return
        
        if reaction.emoji == "\U0001F1EF\U0001F1F5":
            deepl_bot = self.bot.get_cog("DeeplAPI")
            await reaction.message.channel.send(f":flag_jp: : {deepl_bot.translate_jp(reaction.message.content)}")
        
        if reaction.emoji == "\U0001F1EC\U0001F1E7":
            deepl_bot = self.bot.get_cog("DeeplAPI")
            await reaction.message.channel.send(f":flag_gb: : {deepl_bot.translate_en(reaction.message.content)}")

async def setup(bot):
    await bot.add_cog(Events(bot))