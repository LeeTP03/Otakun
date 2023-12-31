from dotenv import load_dotenv
import os
import logging
import asyncio
import discord
from discord.ext import commands
import json

load_dotenv()
bot_token = os.getenv("BOT_DEV_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

with open("settings.json", "r") as f:
    settings = json.load(f)
    bot_prefix = settings["prefix"]

bot = commands.Bot(command_prefix=bot_prefix, intents=intents, status=discord.Status.online, activity=discord.Game(name=f"prefix is {bot_prefix}"), help_command=None)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    await load()

@bot.command()
async def rcog(ctx, arg):
    await bot.reload_extension(f"cogs.{arg}")
    await ctx.send(f"Reloaded {arg} Cog")

asyncio.run(main())
bot.run(bot_token, log_handler=handler)