import discord
from discord.ext import commands

class help(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot


    @discord.slash_command(name="what_is_this_thing", description="Explains what all these words before commands are")
    async def what_is_this_thing(self, ctx):
        embed = discord.Embed(
            title="Groups and subgroups",
            description="Explains what all the words are before all the commands.",
            color=discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
        )
        embed.add_field(name="Groups", value="So the first word in commands is called the group, I use it so that my code is much easier to use, but it's there for you to help you find commands easier.")

        embed.add_field(name="Sub-Groups", value="A sub-group is usually the second word in a command, and it divides groups into smaller groups, it's also to help you find commands.", inline=True)

        embed.add_field(name="Economy??!!?!", value="Be warned! This feature sucks! Surprisingly this bot has a economy system, but you might be thinking, I don't see any of these commands in the list of slash commands, well it's because they're prefixed commands, ugh, so old-school right? If you want to view the economy commands then just, use the command '!ecolist', and the bot will tell you more.")

        embed.set_author(name="elfishhenry", icon_url="https://cdn.discordapp.com/avatars/844984362008838244/237afcecc535e8cfb7b556a5eb97c5b6.png")


        await ctx.respond("Heres some information for you!", embed=embed) # Send the embed with some text

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(help(bot)) # add the cog to the bot