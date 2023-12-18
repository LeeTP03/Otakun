from dotenv import load_dotenv
import os
import logging
import asyncio
import discord
from discord.ext import commands

load_dotenv()
bot_token = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=">", intents=intents)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
 
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    await load()
    

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("<"):
        if message.content.endswith(">"):
            manga = bot.get_cog("Manga")
            if manga is not None:
                await manga.search(message[1:-1])
            await message.channel.send("Hello!")
    
    await bot.process_commands(message)

@bot.command()
async def rcog(ctx, arg):
    await bot.reload_extension(f"cogs.{arg}")
    await ctx.send(f"Reloaded {arg} Cog")

asyncio.run(main())
bot.run(bot_token, log_handler=handler)