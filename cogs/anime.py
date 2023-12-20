from jikanpy import Jikan
import json
from discord.ext import commands
from discord import Embed, ActionRow, ButtonStyle, SelectOption
from discord.ui import Button, View, Select
import discord.ui

class AnimeSelect(Select):
    def __init__(self, data):
        options = [SelectOption(label=f"{data[i].anime_title}", value=f"{i}") for i in range(len(data))]
        super().__init__(placeholder="Select an option", options=options)
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.view.set_selected_option(interaction, self.values)

class AnimeView(View):
    selected_option = None
    
    async def send(self, ctx):
        self.add_item(AnimeSelect(self.items))
        self.message = await ctx.send(view=self)        
        await self.update_message(self.items)
    
    def create_embed(self, data):
        if self.selected_option is None:
            embed = Embed(title="Search Results")
            for i in range(len(data)):
                embed.add_field(name=f"{i + 1}) {data[i].anime_title}", value="", inline=False)
        else:
            data = data[int(self.selected_option)]
            embed = Embed(title=data.anime_title, description=data.description, url=data.anime_url)
            embed.add_field(name="Episodes", value=data.anime_episodes, inline=True)
            embed.add_field(name="Status", value=data.anime_status, inline= True)
            embed.add_field(name="Type", value=data.anime_type, inline=True)
            embed.add_field(name="Rating", value=data.rating,inline=False)
            embed.add_field(name="Score", value=f"{data.anime_score} :star:", inline=True)
            embed.add_field(name="Ranked", value=f"#{data.anime_rank}", inline=True)
            embed.add_field(name="Popularity", value=f"#{data.anime_popularity}", inline=True)
            embed.set_image(url=data.image_link)
        return embed
    
    async def update_message(self, data):
        await self.message.edit(embed=self.create_embed(data), view=self)
    
    async def set_selected_option(self, interaction, value):
        self.selected_option = value[0]
        await self.update_message(self.items)
    

class JikanAPI(commands.Cog):
    
    def __init__(self, bot) -> None:
        self.jikan = Jikan()
        self.bot = bot

    async def get_by_title(self, ctx, title):
        response = self.jikan.search(search_type="anime", query=title, parameters={"limit": 3})
        query_anime = [AnimeData(i) for i in response["data"]]
        
        view = AnimeView()
        view.items = query_anime
        embed = Embed(title = "Search Results")
        
        counter = 1
        for item in response["data"]:
            embed.add_field(name=f"{counter}) {item['title']}", value="", inline=False)
            counter += 1
        
        await view.send(ctx)
        
    def get_anime(self, id):
        pass

class AnimeData:
    def __init__(self,data) -> None:
        self.data = data
        self.init_data()
        
    def init_data(self):
        self.description = self.data["synopsis"]
        self.anime_id = self.data["mal_id"]
        self.anime_url = self.data["url"]
        self.image_link = self.data["images"]["jpg"]["image_url"]
        self.anime_title = self.data["title"]
        self.anime_type = self.data["type"]
        self.anime_episodes = self.data["episodes"]
        self.anime_status = self.data["status"]
        self.rating = self.data["rating"]
        self.anime_rating = self.data["rating"]
        self.anime_score = self.data["score"]
        self.anime = self.data["scored_by"]
        self.anime_rank = self.data["rank"]
        self.anime_popularity = self.data["popularity"]
        
    def __str__(self) -> str:
        return self.anime_title

class Anime(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.command()
    async def anime(self, ctx, *, arg):
        api_search = self.bot.get_cog("JikanAPI")
        await api_search.get_by_title(ctx, arg)
       
        
async def setup(bot):
    await bot.add_cog(Anime(bot))
    await bot.add_cog(JikanAPI(bot))