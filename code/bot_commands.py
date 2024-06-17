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

@client.event
async def on_ready():
    logging.info(f'{client.user} has connected to Discord!')
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "hello" in message.content.lower():
        await message.channel.send("hey")
        logging.info(f"Responded with 'hey' to {message.author} in {message.channel}")
    elif "bye" in message.content.lower():
        await message.channel.send("goodbye")
        logging.info(f"Responded with 'goodbye' to {message.author} in {message.channel}")
    elif "how are you" in message.content.lower():
        await message.channel.send("I'm a bot, I don't have feelings, but thanks for asking!")
        logging.info(f"Responded with 'I'm a bot, I don't have feelings, but thanks for asking!' to {message.author} in {message.channel}")

# Run the client with the specified token
client.run(TOKEN)
