import discord
import os
from os import listdir
from os.path import isfile, join
import os
from dotenv import load_dotenv
from discord.ext import commands

from keep_alive import keep_alive

# Loads bots token from .env secrets
load_dotenv() # load all the variables from the env file

intents = discord.Intents.default()
intents.message_content = True
intents.bans = True
intents.members = True 
intents.guilds = True
intents.guild_messages = True


bot = discord.Bot(intents=discord.Intents.all())

client = bot

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")






TOKEN = os.getenv("DISCORD_TOKEN")


bot.load_extension("cogs.Music")
print("cogs proabbyl loaded")


bot.run(TOKEN)
