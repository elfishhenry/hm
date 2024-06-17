# bot.py
import os
from discord.ext import commands
import discord
from dotenv import load_dotenv
from discord import Intents


# Enable all standard intents and message content
# (prefix commands generally require message content)
intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# improting token from dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# gets client object
#client = discord.Client()
bot = discord.Client(intents=discord.Intents.default())

# connects the bot
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.event
async def on_message(message):
	if message.content == "hello":
		await message.channel.send("hello")

bot.run(TOKEN)