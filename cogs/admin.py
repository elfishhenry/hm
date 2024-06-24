import discord
from discord.ext import commands

class admin(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @commands.slash_command(name="addrole", description="Adds a specified role to a user.")
    @commands.has_permissions(manage_roles=True)
    async def addrole(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        await member.add_roles(role)
        await interaction.response.send_message(f"Added role {role.name} to {member}.")



    @commands.slash_command(name="removerole", description="Removes a specified role from a user.")
    @commands.has_permissions(manage_roles=True)
    async def removerole(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        await member.remove_roles(role)
        await interaction.response.send_message(f"Removed role {role.name} from {member}.")

    @commands.slash_command(name="createrole", description="Creates a new role with specified properties.")
    @commands.has_permissions(manage_roles=True)
    async def createrole(interaction: discord.Interaction, name: str, color: int, permissions: int):
        if color < 0 or color > 16777215:
            await interaction.response.send_message("Invalid color value. Please provide a valid integer color value between 0 and 16777215.", ephemeral=True)
            return
        
        role_permissions = discord.Permissions(permissions)
        role = await interaction.guild.create_role(name=name, color=discord.Color(color), permissions=role_permissions)
        await interaction.response.send_message(f"Created role {role.name}.")



    @commands.slash_command(name="deleterole", description="Deletes a specified role from the server.")
    @commands.has_permissions(manage_roles=True)
    async def deleterole(interaction: discord.Interaction, role: discord.Role):
        await role.delete()
        await interaction.response.send_message(f"Deleted role {role.name}.")

    @commands.slash_command(name="report", description="Allows users to report another user for inappropriate behavior, with the reason logged.")
    async def report(interaction: discord.Interaction, member: discord.Member, reason: str):
        # Log the report
        log_channel = discord.utils.get(interaction.guild.text_channels, name="log-channel")
        if log_channel:
            await log_channel.send(f"User {member} has been reported by {interaction.user} for: {reason}")
        await interaction.response.send_message(f"Reported {member} for: {reason}", ephemeral=True)


def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(admin(bot)) # add the cog to the bot