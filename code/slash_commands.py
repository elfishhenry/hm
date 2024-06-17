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
    try:
        synced = await client.tree.sync()
        logging.info(f"Synced {len(synced)} commands")
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        logging.error(e)
        print(e)

# Define a slash command to respond to "hello"
@client.tree.command(name="hello", description="Responds with 'hey'")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("hey")
    logging.info(f"Slash command 'hello' used by {interaction.user} in {interaction.channel}")

# Define a slash command to respond to "goodbye"
@client.tree.command(name="goodbye", description="Responds with 'goodbye'")
async def goodbye(interaction: discord.Interaction):
    await interaction.response.send_message("goodbye")
    logging.info(f"Slash command 'goodbye' used by {interaction.user} in {interaction.channel}")

# Define a slash command to respond to "how are you"
@client.tree.command(name="how_are_you", description="Responds with a bot's status")
async def how_are_you(interaction: discord.Interaction):
    await interaction.response.send_message("I'm a bot, I don't have feelings, but thanks for asking!")
    logging.info(f"Slash command 'how_are_you' used by {interaction.user} in {interaction.channel}")

# Run the client with the specified token
client.run(TOKEN)
