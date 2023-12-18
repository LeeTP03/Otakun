from discord.ext import commands
from mangadex import MangaDexAPI
from discord import Embed, ActionRow, ButtonStyle
from discord.ui import Button, View
import discord.ui


class PaginationView(View):
    current_page = 1

    async def send(
        self,
        ctx,
    ):
        if self.items[0] == "Error":
            await ctx.send("Manga not hosted on MangaDex :(")
            return
        self.message = await ctx.send(view=self)
        await self.update_message(self.items[self.current_page - 1])

    def create_embed(self, data):
        embed = Embed(title=self.manga_title, description=f"Chapter {self.chapter_number} {'' if self.chapter_title is None else ':' + self.chapter_title}")
        embed.set_image(url=data)

        embed.set_footer(text=f"Page {self.current_page}")
        return embed

    async def update_message(self, data):
        self.update_buttons()
        await self.message.edit(embed=self.create_embed(data), view=self)

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
        await self.update_message(self.items[self.current_page - 1])

    @discord.ui.button(label="Previous", style=ButtonStyle.blurple)
    async def prev_button(self, interaction, button):
        await interaction.response.defer()
        self.current_page -= 1
        await self.update_message(self.items[self.current_page - 1])

    @discord.ui.button(label="Next", style=ButtonStyle.blurple)
    async def next_button(self, interaction, button):
        await interaction.response.defer()
        self.current_page += 1
        await self.update_message(self.items[self.current_page - 1])

    @discord.ui.button(label="Last", style=ButtonStyle.blurple)
    async def last_page_button(self, interaction, button):
        await interaction.response.defer()
        self.current_page = len(self.items)
        await self.update_message(self.items[self.current_page - 1])


class Manga(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.latest_chapter = None
        self.manga = None
        self.ctx = None

    @commands.command()
    async def search(self, ctx, *, message):
        await ctx.send(f"Searching for manga {message}")

        # Getting manga
        api_fetcher = MangaDexAPI()
        result = api_fetcher.get_manga(message)

        if result == "No results found":
            await ctx.send("No results found")
            return

        embed = Embed(
            title=result.title,
            description=result.description,
            color=0x00FF00,
        )
        embed.set_image(url=result.get_cover())
        embed.add_field(name="Author", value=result.author, inline=True)
        embed.add_field(name="Status", value=result.get_status(), inline=False)
        embed.add_field(name="Chapters", value=result.number_of_chapters, inline=True)
        embed.add_field(name="Volumes", value=result.number_of_volumes, inline=True)
        embed.add_field(name="Genres", value=result.get_tags(), inline=False)
        embed.add_field(name="Demographic", value=result.get_demographic(), inline=True)

        # Buttons
        view = View()
        open_website_button = Button(label="Open Website", url=result.get_manga_site())
        latest_chapter_button = Button(
            label="Latest Chapter", url=result.latest_chapter
        )
        read_here_button = Button(
            label="Read Here", style=ButtonStyle.blurple, custom_id="read_here_button"
        )

        read_here_button.callback = self.read_here
        self.latest_chapter = result.latest_chapter_id
        self.manga = result

        view.add_item(read_here_button)
        view.add_item(open_website_button)
        view.add_item(latest_chapter_button)

        await ctx.send(embed=embed, view=view)

    async def read_here(self, interaction):
        pages = self.manga.get_chapter_pages()
        pages = [
            i.replace(
                "https://uploads.mangadex.org/data-saver/",
                "https://fxmangadex.org/data-saver/",
            )
            for i in pages
        ]
        print(pages)
        view = PaginationView()
        view.chapter_title = self.manga.latest_chapter_title
        view.chapter_number = self.manga.latest_chapter_number
        view.manga_title = self.manga.title
        view.items = pages
        await view.send(interaction.channel)

    @commands.command()
    async def testmanga(self, ctx, arg):
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        view = PaginationView()
        view.items = data
        await view.send(ctx)


async def setup(bot):
    await bot.add_cog(Manga(bot))
