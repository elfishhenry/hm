import discord
from discord.ext import commands

class ping(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    testing = discord.SlashCommandGroup("testing", "testing") # create a Slash Command Group called "testing"
   

    @testing.command(name="ping", description="Checks the bot's responsiveness.")
    async def ping(self, ctx):
        interaction = ctx
        await interaction.response.send_message("Pong!")


def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(ping(bot)) # add the cog to the bot