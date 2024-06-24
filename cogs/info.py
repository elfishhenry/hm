import discord
from discord.ext import commands

class info(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @commands.slash_command(name="uptime", description="Display how long the bot has been online since its last restart.")
    async def uptime(ctx):
        uptime_seconds = int(commands.uptime().total_seconds())
        await ctx.send(f"Uptime: {uptime_seconds} seconds")
    
    @commands.slash_command(name="serverinfo", description="Provides information about the server, such as member count, region, and creation date.")
    async def serverinfo(interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(title=f"Server Info - {guild.name}", color=discord.Color.blue())
        embed.add_field(name="Server ID", value=guild.id, inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Region", value=guild.region, inline=True)
        embed.add_field(name="Created", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        await interaction.response.send_message(embed=embed)

    @commands.slash_command(name="roleinfo", description="Displays information about a specific role.")
    async def roleinfo(interaction: discord.Interaction, role: discord.Role):
        embed = discord.Embed(title=f"Role Info - {role.name}", color=role.color)
        embed.add_field(name="Role ID", value=role.id, inline=True)
        embed.add_field(name="Color", value=str(role.color), inline=True)
        embed.add_field(name="Created", value=role.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        embed.add_field(name="Permissions", value=", ".join([perm[0] for perm in role.permissions if perm[1]]), inline=True)
        await interaction.response.send_message(embed=embed)   

    @commands.slash_command(name="userinfo", description="Displays information about a user, such as join date, roles, and infractions.")
    async def userinfo(interaction: discord.Interaction, member: discord.Member):
        embed = discord.Embed(title=f"User Info - {member}", color=discord.Color.blue())
        embed.add_field(name="User ID", value=member.id, inline=True)
        embed.add_field(name="Joined", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        embed.add_field(name="Roles", value=", ".join([role.name for role in member.roles]), inline=True)
        await interaction.response.send_message(embed=embed)

    @commands.slash_command(name="serverinfooooo", description="Provide information about the current server.")
    async def serverinfo(ctx):
        guild = ctx.guild
        member_count = guild.member_count
        channel_count = len(guild.channels)
        await ctx.send(f"Server Name: {guild.name}\nMember Count: {member_count}\nChannel Count: {channel_count}")

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(info(bot)) # add the cog to the bot