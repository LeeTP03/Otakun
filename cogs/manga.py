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
            await ctx.send(
                f"Manga not hosted on MangaDex :( \nRead here instead {self.chapter_link}"
            )
            return
        self.message = await ctx.send(view=self)
        await self.update_message(self.items[self.current_page - 1])

    def create_embed(self, data):
        embed = Embed(
            title=self.manga_title,
            description=f"Chapter {self.chapter_number} {'' if self.chapter_title is None else ':' + self.chapter_title}",
        )
        embed.set_image(url=data)

        embed.set_footer(text=f"Page {self.current_page}/{len(self.items)}")
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
        await ctx.send(f"Searching for {message.title()}")

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

        if not result.latest_chapter_id == "No Chapters Found":
            read_here_button = Button(
                label="Read Here",
                style=ButtonStyle.blurple,
                custom_id="read_here_button",
            )
            read_here_button.callback = self.read_here
            view.add_item(read_here_button)

        self.latest_chapter = result.latest_chapter_id
        self.manga = result

        open_website_button = Button(label="Open Website", url=result.get_manga_site())
        view.add_item(open_website_button)

        if not result.latest_chapter_id == "No Chapters Found":
            latest_chapter_button = Button(
                label="Latest Chapter", url=result.latest_chapter
            )
            view.add_item(latest_chapter_button)

        await ctx.send(embed=embed, view=view)

    async def read_here(self, interaction):
        await interaction.response.defer()
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
        view.chapter_link = self.manga.latest_chapter
        view.items = pages
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
