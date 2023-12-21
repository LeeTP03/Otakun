from discord.ext import commands
from mangadex import MangaDexAPI
from discord import Embed, ActionRow, ButtonStyle, SelectOption
from discord.ui import Button, View, Select
import discord.ui

class MangaSelect(Select):
    def __init__(self, data):
        options = [SelectOption(label=f"{data[i].title}", value=f"{i}") for i in range(len(data))]
        super().__init__(placeholder="Select an option", options=options)
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.view.set_selected_option(interaction, self.values)

class MangaView(View):
    selected_option = None
        
    async def send(self, ctx):
        self.add_item(MangaSelect(self.items))
        self.message = await ctx.send(view=self)        
        await self.update_message(self.items)
    
    def create_embed(self, data):
        if self.selected_option is None:
            embed = Embed(title="Search Results")
            for i in range(len(data)):
                embed.add_field(name=f"{i + 1}) {data[i].title}", value="", inline=False)
        else:
            self.add_item(Button(label="Open Website", url=data[int(self.selected_option)].get_manga_site()))
            self.add_item(Button(label="Latest Chapter", url=data[int(self.selected_option)].get_latest_link()[0]))
            read_here_button = Button(label="Read Here", style=ButtonStyle.blurple)
            self.add_item(read_here_button)
            
            mangaCog = self.bot.get_cog("Manga")
            read_here_button.callback = mangaCog.read_here
            
                     
            data = data[int(self.selected_option)]
            embed = Embed(
                title=data.title,
                description=data.description,
                color=0x00FF00,
            )
            embed.set_image(url=data.get_cover())
            embed.add_field(name="Author", value=data.author, inline=True)
            embed.add_field(name="Status", value=data.get_status(), inline=False)
            embed.add_field(name="Chapters", value=data.chapter_number, inline=True)
            embed.add_field(name="Volumes", value=data.volume_number, inline=True)
            embed.add_field(name="Genres", value=data.get_tags(), inline=False)
            embed.add_field(name="Demographic", value=data.get_demographic(), inline=True)
        return embed
    
    async def update_message(self, data):
        self.clear_items()
        self.add_item(MangaSelect(self.items))
        await self.message.edit(embed=self.create_embed(data), view=self)
    
    async def set_selected_option(self, interaction, value):
        self.selected_option = value[0]
        await self.update_message(self.items)


class ChapterSelect(Select):
    def __init__(self, data):
        self.data = data
        options = [SelectOption(label=f"{data[i].chapter_number}", value=f"{i}") for i in range(len(data))]
        super().__init__(placeholder="Select an option", options=options)
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.view.set_selected_option(interaction, self.values, self.data)


class PaginationView(View):
    current_page = 1
    selected_option = 0
    
    async def send(
        self,
        ctx,
    ):
        if self.items[0].get_data() == "Error":
            await ctx.send(
                f"Manga not hosted on MangaDex :(\nCheck it out here: {self.items[0].chapter_link}"
            )
            return
        self.message = await ctx.send(view=self)
        await self.update_message(self.items[self.selected_option])

    def create_embed(self, data):
        embed = Embed(
            title=self.manga_title,
            description=f"{data.chapter_number} - {data.chapter_title}",
        )
        pages = data.get_data()
        embed.set_image(url=pages[self.current_page - 1])
        embed.set_footer(text=f"Page {self.current_page}/{len(pages)}")
        return embed

    async def update_message(self, data):
        self.update_buttons()
        await self.message.edit(embed=self.create_embed(data), view=self)
    
    async def set_selected_option(self, interaction, value, data):
        self.selected_option = int(value[0])
        self.current_page = 1
        await self.update_message(data[int(value[0])])

    def update_buttons(self):
        if self.current_page == 1:
            self.first_page_button.disabled = True
            self.prev_button.disabled = True
            self.first_page_button.style = discord.ButtonStyle.gray
            self.prev_button.style = discord.ButtonStyle.gray
        else:
            self.first_page_button.disabled = False
            self.prev_button.disabled = False
            self.first_page_button.style = discord.ButtonStyle.green
            self.prev_button.style = discord.ButtonStyle.primary

        if self.current_page == len(self.items):
            self.next_button.disabled = True
            self.last_page_button.disabled = True
            self.last_page_button.style = discord.ButtonStyle.gray
            self.next_button.style = discord.ButtonStyle.gray
        else:
            self.next_button.disabled = False
            self.last_page_button.disabled = False
            self.last_page_button.style = discord.ButtonStyle.green
            self.next_button.style = discord.ButtonStyle.primary

    @discord.ui.button(label="First", style=ButtonStyle.blurple)
    async def first_page_button(self, interaction, button):
        await interaction.response.defer()
        self.current_page = 1
        await self.update_message(self.items[self.selected_option])

    @discord.ui.button(label="Previous", style=ButtonStyle.blurple)
    async def prev_button(self, interaction, button):
        await interaction.response.defer()
        self.current_page -= 1
        await self.update_message(self.items[self.selected_option])

    @discord.ui.button(label="Next", style=ButtonStyle.blurple)
    async def next_button(self, interaction, button):
        await interaction.response.defer()
        self.current_page += 1
        await self.update_message(self.items[self.selected_option])

    @discord.ui.button(label="Last", style=ButtonStyle.blurple)
    async def last_page_button(self, interaction, button):
        await interaction.response.defer()
        self.current_page = len(self.items)
        await self.update_message(self.items[self.selected_option])


class Manga(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.latest_chapter = None
        self.manga_data = None
        self.manga_view = None
        self.ctx = None

    @commands.command()
    async def manga(self, ctx, *, message):
        
        delim = message.split("~")
        await ctx.send(f"Searching for {delim[0].title()}")
        # Getting manga
        api_fetcher = MangaDexAPI()
        if len(delim) == 2:
            result = api_fetcher.get_manga(delim[0].strip(), delim[1].strip())
        else:
            result = api_fetcher.get_manga(delim[0])

        if result == "No results found":
            await ctx.send("No results found")
            return
        
        view = MangaView()
        view.items = result
        view.bot = self.bot
        self.manga_view = view
        
        await view.send(ctx)

    async def read_here(self, interaction: discord.Interaction):
        self.manga_data = self.manga_view.items[int(self.manga_view.selected_option)]
        await interaction.response.defer()        
        
        view = PaginationView()
        view.manga_title = self.manga_data.title
        self.manga_data.get_manga_feed()
        view.items = self.manga_data.all_chapters
        
        
        chapter_selector = ChapterSelect(self.manga_data.all_chapters)
        
        view.add_item(chapter_selector)
        await view.send(interaction.channel)

    @commands.command()
    async def testmanga(self, ctx, arg):
        data = [
            "https://fxmangadex.org/data-saver/9e8730cd7cc45637b7ee0173418374cc/1-dbf32b8bda59b3700c18b54a2f9b58559f3565bc1458a4501794fef4e13fa40f.jpg",
            "https://fxmangadex.org/data-saver/9e8730cd7cc45637b7ee0173418374cc/2-3e73682c18cbce64f666740cc0bb0b49660988ff3c607b2a0968b6ac9b813324.jpg",
            "https://fxmangadex.org/data-saver/9e8730cd7cc45637b7ee0173418374cc/3-d443d3824cb3f86ef076e1aaedeecb16431a4364fc6e651339df2f6ee3d0ba8f.jpg",
            "https://fxmangadex.org/data-saver/9e8730cd7cc45637b7ee0173418374cc/4-67a3bb5719c67427faebee1a35bb6dc021ff40e7b6b8bb2cbe671c9ac81a7a7d.jpg",
        ]
        view = PaginationView()
        view.chapter_title = self.manga.latest_chapter_title
        view.chapter_number = self.manga.latest_chapter_number
        view.manga_title = self.manga.title
        view.chapter_link = self.manga.latest_chapter
        view.items = data
        await view.send(ctx)


async def setup(bot):
    await bot.add_cog(Manga(bot))
