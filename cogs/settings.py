from discord.ext import commands
import json

class Settings(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def prefix(self, ctx, prefix):
        self.bot.command_prefix = prefix
        await ctx.send(f"Prefix changed to {prefix}")
        
        settingsJson = None
        with open("settings.json", "r") as f:
            settingsJson = json.load(f)
            settingsJson["prefix"] = prefix
            
        with open("settings.json", "w") as f:
            json.dump(settingsJson, f)
        
async def setup(bot):
    await bot.add_cog(Settings(bot))