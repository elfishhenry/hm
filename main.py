import discord
import os
from os import listdir
from os.path import isfile, join
import os
from dotenv import load_dotenv
from discord.ext import commands
from keep_alive import keep_alive
import logging

log_dir = r"C:\Users\User\Documents\lets try making a bot again\hm"



log_file = os.path.join(log_dir, 'bot.log')
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Loads bots token from .env secrets
load_dotenv() # load all the variables from the env file

intents = discord.Intents.default()
intents.message_content = True
intents.bans = True
intents.members = True 
intents.guilds = True
intents.guild_messages = True


bot = discord.ext.commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    logging.info(f'{bot.user} has connected to Discord!')
    print(bot._pending_application_commands)
    print(bot._application_commands)
    print(bot.commands)
    logging.info(f"Ping or Latency is {round(bot.latency * 1000)}ms")

keep_alive()


#TOKEN = os.getenv("DISCORD_TOKEN")
TOKEN = os.getenv("elft")

#credit to this repo"https://github.com/micfun123/Simplex_bot" for the snippit of code below.

#def start_bot(bot):
#    lst = [f for f in listdir("hm/cogs/") if isfile(join("cogs/", f))]
#    no_py = [s.replace(".py", "") for s in lst]
#    startup_extensions = ["cogs." + no_py for no_py in no_py]
#    try:
#        for filename in os.listdir('hm/cogs/'):
#            if filename.endswith('.py'):
#                bot.load_extension(f'cogs.{filename[:-3]}')
#                print(f"{filename}, the cog of the century, has been loaded")
#
#        print("\nAll Cogs Loaded\n===============\nLogging into Discord...")
#        bot.run(
#            TOKEN
#        )  # Token do not change it here. Change it in the .env if you do not have a .env make a file and put DISCORD_TOKEN=Token

#    except Exception as e:
#        print(
#            f"\n###################\nPOSSIBLE FATAL ERROR:\n{e}\nTHIS MEANS THE BOT HAS NOT STARTED CORRECTLY!"
#        )

 
#start_bot(bot)


cogs_list = [
    'fun',
    'admin',
    'greetings',
    'moderation',
    'economy',
    'info',
    'Music',
    'ping',
    'qol'
]


for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')
    print(f'loaded the cog of the century: {cog}')
    logging.info(f'the cog of the century {cog} has been loaded')
bot.run(TOKEN)

   
        # Delete the log file after the processes are done
if os.path.exists(log_file):
    os.remove(log_file)
print("Log file deleted.")