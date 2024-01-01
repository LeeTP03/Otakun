from discord.ext import commands
from discord import app_commands
import discord

class SlashCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def sync(self, ctx: commands.Context):
        ctx.bot.tree.copy_global_to(guild=ctx.guild)
        synced = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"Synced {len(synced)} commands")
    
    @app_commands.command(name="manga", description="find manga")
    async def manga_slash(self, interaction: discord.Interaction, manga: str, amount:str):
        await interaction.response.defer(thinking=False)
        mangaCogs = self.bot.get_cog("Manga")
        await mangaCogs.manga_helper(interaction.channel , manga, amount)
        await interaction.followup.send("Complete")
        
    @app_commands.command(name="anime", description="find anime")
    async def anime_slash(self, interaction: discord.Interaction, anime: str, amount:str):
        await interaction.response.defer(thinking=False)
        animeCogs = self.bot.get_cog("Anime")
        await animeCogs.anime_helper(interaction.channel , anime, amount)
        await interaction.followup.send("Complete")
        
    @app_commands.command(name="jdict", description="lookup japanese term")
    async def jdict_slash(self, interaction: discord.Interaction, term: str):
        await interaction.response.defer(thinking=False)
        jdictCogs = self.bot.get_cog("JDict")
        await interaction.followup.send("Complete")
        await jdictCogs.jdict(interaction.channel , term)
        
    @app_commands.command(name="translate", description="Translate a sentence")
    async def translate_slash(self, interaction: discord.Interaction, term: str, lang:str):
        english = ["en", "english", "eng"]
        japanese = ["ja", "japanese", "jp"]
        german = ["de", "german", "ge"]
        await interaction.response.defer(thinking=False)
        translateCogs = self.bot.get_cog("DeeplAPI")
        if lang in english :
            await interaction.channel.send(f":flag_gb: : {translateCogs.translate_en(term)}")
            await interaction.followup.send("Complete")
            return
        elif lang in japanese:
            await interaction.channel.send(f":flag_jp: : {translateCogs.translate_jp(term)}")
            await interaction.followup.send("Complete")
            return
        elif lang in german:
            await interaction.channel.send(f":flag_de: : {translateCogs.translate_ge(term)}")
            await interaction.followup.send("Complete")
            return
        await interaction.followup.send("Invalid language")
        return
        
async def setup(bot):
    await bot.add_cog(SlashCommands(bot))