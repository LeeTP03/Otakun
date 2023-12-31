from discord.ext import commands
import deepl
import os
import pykakasi


class Translator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def translate(self, ctx, *, message):
        await ctx.send(f"Translated message: {message}")
        
        
class DeeplAPI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = os.getenv("DEEPL_API_TOKEN")
        self.translator = deepl.Translator(self.api_key)
        self.kks = pykakasi.kakasi()

    def translate_en(self, message):
        result = self.translator.translate_text(message, target_lang="EN-GB")
        return result
    
    def translate_jp(self, message):
        translated = self.translator.translate_text(message, target_lang="JA")
        result = self.kks.convert(translated.text)
        romaji = " ".join([item["hepburn"] for item in result])
        return f"{translated} ({romaji})"
    
    def translate_ge(self, message):
        result = self.translator.translate_text(message, target_lang="DE")
        return result
    
    
        
async def setup(bot):
    await bot.add_cog(Translator(bot))
    await bot.add_cog(DeeplAPI(bot))