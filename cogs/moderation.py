import discord
from discord.ext import commands
import asyncio

class moderation(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @commands.slash_command(name="ban", description="Ban a user from the server")
    @commands.has_permissions(ban_members=True)
    async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        dm_sent = True
        try:
            # Attempt to send a DM to the user
            await member.send(f"You have been banned from {interaction.guild.name} for: {reason}")
        except discord.Forbidden:
            dm_sent = False
            # Log the error or notify the command invoker
            await interaction.response.send_message("I cannot send a DM to this user.", ephemeral=True)
        
        try:
            # Ban the user
            await interaction.guild.ban(member, reason=reason)
            response_message = f"User {member} has been banned for: {reason}"
            if not dm_sent:
                response_message += "\nNote: Failed to send a DM to the user."
            await interaction.response.send_message(response_message)
        except discord.Forbidden:
            await interaction.response.send_message("I do not have permission to ban this user.", ephemeral=True)
        except discord.HTTPException:
            await interaction.response.send_message("An error occurred while trying to ban this user.", ephemeral=True)


    # Unban Command
    @commands.slash_command(name="unban", description="Unban a user from the server")
    @commands.has_permissions(ban_members=True)
    async def unban(interaction: discord.Interaction, user_id: str, reason: str = "No reason provided"):
        try:
            user = await commands.fetch_user(user_id)
            
            # Unban the user
            await interaction.guild.unban(user, reason=reason)
            
            # Create an invite link
            invite = await interaction.channel.create_invite(max_uses=1, unique=True)
            
            # Attempt to send a DM to the user
            try:
                await user.send(f"You have been unbanned from {interaction.guild.name}. Here is your invite link: {invite.url}")
            except discord.Forbidden:
                await interaction.response.send_message(f"User {user} has been unbanned for: {reason}, but I could not send them a DM.", ephemeral=True)
                return
            
            await interaction.response.send_message(f"User {user} has been unbanned for: {reason}. An invite link was sent to their DM.")
        except discord.NotFound:
            await interaction.response.send_message("User not found.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I do not have permission to unban this user.", ephemeral=True)
        except discord.HTTPException:
            await interaction.response.send_message("An error occurred while trying to unban this user.", ephemeral=True)

    @commands.slash_command(name="kick", description="Kicks a user from the server and optionally logs the reason.")
    @commands.has_permissions(kick_members=True)
    async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        try:
            await member.kick(reason=reason)
            await interaction.response.send_message(f"User {member} has been kicked for: {reason}")
        except discord.Forbidden:
            await interaction.response.send_message("I do not have permission to kick this user.", ephemeral=True)
        except discord.HTTPException:
            await interaction.response.send_message("An error occurred while trying to kick this user.", ephemeral=True)

    @commands.slash_command(name="mute", description="Mutes a user for a specified duration or indefinitely, with an optional reason.")
    @commands.has_permissions(manage_roles=True)
    async def mute(interaction: discord.Interaction, member: discord.Member, duration: int = None, reason: str = "No reason provided"):
        role = discord.utils.get(interaction.guild.roles, name="Muted")
        if not role:
            await interaction.response.send_message("Muted role not found. Please create a 'Muted' role.", ephemeral=True)
            return
        await member.add_roles(role, reason=reason)
        if duration:
            await interaction.response.send_message(f"User {member} has been muted for {duration} seconds for: {reason}")
            await asyncio.sleep(duration)
            await member.remove_roles(role, reason="Mute duration expired.")
        else:
            await interaction.response.send_message(f"User {member} has been muted indefinitely for: {reason}")


    @commands.slash_command(name="unmute", description="Unmutes a user.")
    @commands.has_permissions(manage_roles=True)
    async def unmute(interaction: discord.Interaction, member: discord.Member):
        role = discord.utils.get(interaction.guild.roles, name="Muted")
        if role in member.roles:
            await member.remove_roles(role)
            await interaction.response.send_message(f"User {member} has been unmuted.")
        else:
            await interaction.response.send_message(f"User {member} is not muted.", ephemeral=True)





    @commands.slash_command(name="warn", description="Issues a warning to a user, with the reason logged.")
    @commands.has_permissions(manage_messages=True)
    async def warn(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        await interaction.response.send_message(f"User {member} has been warned for: {reason}")
        # Log the warning
        log_channel = discord.utils.get(interaction.guild.text_channels, name="log-channel")
        if log_channel:
            await log_channel.send(f"User {member} has been warned by {interaction.user} for: {reason}")



    @commands.slash_command(name="timeout", description="Temporarily restricts a user from sending messages or participating in voice channels.")
    @commands.has_permissions(manage_roles=True)
    async def timeout(interaction: discord.Interaction, member: discord.Member, duration: int, reason: str = "No reason provided"):
        role = discord.utils.get(interaction.guild.roles, name="Timeout")
        if not role:
            await interaction.response.send_message("Timeout role not found. Please create a 'Timeout' role.", ephemeral=True)
            return
        await member.add_roles(role, reason=reason)
        await interaction.response.send_message(f"User {member} has been put in timeout for {duration} seconds for: {reason}")
        await asyncio.sleep(duration)
        await member.remove_roles(role, reason="Timeout duration expired.")





    @commands.slash_command(name="softban", description="Bans and immediately unbans a user, effectively kicking them and deleting their recent messages.")
    @commands.has_permissions(ban_members=True)
    async def softban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        try:
            await interaction.guild.ban(member, reason=reason, delete_message_days=7)
            await interaction.guild.unban(member, reason="Softban complete")
            await interaction.response.send_message(f"User {member} has been softbanned for: {reason}")
        except discord.Forbidden:
            await interaction.response.send_message("I do not have permission to ban/unban this user.", ephemeral=True)
        except discord.HTTPException:
            await interaction.response.send_message("An error occurred while trying to softban this user.", ephemeral=True)

    @commands.slash_command(name="purge", description="Deletes a specified number of messages from a channel.")
    @commands.has_permissions(manage_messages=True)
    async def purge(interaction: discord.Interaction, number: int):
        await interaction.channel.purge(limit=number)
        log_channel = discord.utils.get(interaction.guild.text_channels, name="log-channel")
        if log_channel:
            await log_channel.send(f"Deleted {number} messages.")

    @commands.slash_command(name="lockdown", description="Locks a channel for a specified duration or until manually unlocked, with an optional reason.")
    @commands.has_permissions(manage_channels=True)
    async def lockdown(interaction: discord.Interaction, duration: int = None, reason: str = "No reason provided"):
        overwrite = discord.PermissionOverwrite(send_messages=False)
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        await interaction.response.send_message(f"Channel locked down for {duration} seconds for: {reason}" if duration else f"Channel locked down indefinitely for: {reason}")
        if duration:
            await asyncio.sleep(duration)
            await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=None)
            await interaction.channel.send("Channel lockdown lifted.")

    @commands.slash_command(name="unlock", description="Unlocks a previously locked channel.")
    @commands.has_permissions(manage_channels=True)
    async def unlock(interaction: discord.Interaction):
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=None)
        await interaction.response.send_message("Channel unlocked.")



def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(moderation(bot)) # add the cog to the bot