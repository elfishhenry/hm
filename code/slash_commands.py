import os
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord import Intents

# Configure logging
script_dir = r"C:\Users\User\Documents\lets try making a bot again\hm"
log_file = os.path.join(script_dir, 'bot.log')
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Load the environment variables from the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Enable intents
intents = Intents.default()
intents.message_content = True

# Create the client object with the specified intents
client = commands.Bot(command_prefix='!', intents=intents)


# Run the client with the specified token
client.run(TOKEN)
