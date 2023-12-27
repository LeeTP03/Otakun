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
        
    # @commands.Cog.listener()
    # async def on_reaction_add(self, reaction, user):
    #     if user == self.bot.user:
    #         return
        
    #     if reaction.emoji == "\U0001F1EF\U0001F1F5":
    #         deepl_bot = self.bot.get_cog("DeeplAPI")
    #         await reaction.message.reply(f":flag_jp: : {deepl_bot.translate_jp(reaction.message.content)}", mention_author=False)
        
    #     if reaction.emoji == "\U0001F1EC\U0001F1E7":
    #         deepl_bot = self.bot.get_cog("DeeplAPI")
    #         await reaction.message.reply(f":flag_gb: : {deepl_bot.translate_en(reaction.message.content)}", mention_author=False)
            
    #     if reaction.emoji == "\U0001F1E9\U0001F1EA":
    #         deepl_bot = self.bot.get_cog("DeeplAPI")
    #         await reaction.message.reply(f":flag_de: : {deepl_bot.translate_ge(reaction.message.content)}", mention_author=False)
            
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = self.bot.get_user(payload.user_id)
        
        if user == self.bot.user:
            return
        
        if payload.emoji.name == "\U0001F1EF\U0001F1F5":
            deepl_bot = self.bot.get_cog("DeeplAPI")
            await message.reply(f":flag_jp: : {deepl_bot.translate_jp(message.content)}", mention_author=False)
        
        if payload.emoji.name == "\U0001F1EC\U0001F1E7":
            deepl_bot = self.bot.get_cog("DeeplAPI")
            await message.reply(f":flag_gb: : {deepl_bot.translate_en(message.content)}", mention_author=False)
            
        if payload.emoji.name == "\U0001F1E9\U0001F1EA":
            deepl_bot = self.bot.get_cog("DeeplAPI")
            await message.reply(f":flag_de: : {deepl_bot.translate_ge(message.content)}", mention_author=False)

async def setup(bot):
    await bot.add_cog(Events(bot))