import discord
from discord.ext import commands

class ping(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @commands.slash_command(name="ping", description="Checks the bot's responsiveness.")
    async def ping(interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")

    @commands.slash_command(name="serverinfo", description="Provides information about the server, such as member count, region, and creation date.")
    async def serverinfo(interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(title=f"Server Info - {guild.name}", color=discord.Color.blue())
        embed.add_field(name="Server ID", value=guild.id, inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Region", value=guild.region, inline=True)
        embed.add_field(name="Created", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        await interaction.response.send_message(embed=embed)

    @commands.slash_command(name="latency", description="Ping the bot")
    async def ping(interaction: discord.Interaction):
        await interaction.response.send_message(f"Ping or Latency is {round(commands.latency * 1000)}ms")
        print('has connected to Discord!')

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(ping(bot)) # add the cog to the bot