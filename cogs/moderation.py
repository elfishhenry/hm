import discord
from discord.ext import commands
import asyncio
import sqlite3
from datetime import datetime

class Moderation(commands.Cog): # create a class for our cog that inherits from commands.Cog

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot
        self.conn = sqlite3.connect('moderation.db')
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS command_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    command_name TEXT,
                    user_id TEXT,
                    user_name TEXT,
                    target_id TEXT,
                    target_name TEXT,
                    reason TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

    def log_command(self, command_name, user_id, user_name, target_id=None, target_name=None, reason=None):
        with self.conn:
            self.conn.execute('''
                INSERT INTO command_logs (command_name, user_id, user_name, target_id, target_name, reason)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (command_name, user_id, user_name, target_id, target_name, reason))

    
    mod = discord.SlashCommandGroup("mod", "Moderation commands") # create a Slash Command Group called "Mod"
    removal = mod.create_subgroup(
        "removal",
        "commands that remove SOMETHING from the server"
    )
    
    @removal.command(name="ban", description="Ban a user from the server")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, reason: str = "No reason provided"):
        interaction = ctx
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
            self.log_command('ban', ctx.author.id, str(ctx.author), member.id, str(member), reason)
        except discord.Forbidden:
            await interaction.response.send_message("I do not have permission to ban this user.", ephemeral=True)
        except discord.HTTPException:
            await interaction.response.send_message("An error occurred while trying to ban this user.", ephemeral=True)


    # Unban Command
    @removal.command(name="unban", description="Unban a user from the server")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: str, reason: str = "No reason provided"):
        try:
            user = await commands.fetch_user(user_id)
            
            # Unban the user
            await ctx.guild.unban(user, reason=reason)
            
            # Create an invite link
            invite = await ctx.channel.create_invite(max_uses=1, unique=True)
            
            # Attempt to send a DM to the user
            try:
                await user.send(f"You have been unbanned from {ctx.guild.name}. Here is your invite link: {invite.url}")
            except discord.Forbidden:
                await ctx.response.send_message(f"User {user} has been unbanned for: {reason}, but I could not send them a DM.", ephemeral=True)
                return
            
            await ctx.response.send_message(f"User {user} has been unbanned for: {reason}. An invite link was sent to their DM.")
            self.log_command('unban', ctx.author.id, str(ctx.author), user_id, str(user), reason)
        except discord.NotFound:
            await ctx.response.send_message("User not found.", ephemeral=True)
        except discord.Forbidden:
            await ctx.response.send_message("I do not have permission to unban this user.", ephemeral=True)
        except discord.HTTPException:
            await ctx.response.send_message("An error occurred while trying to unban this user.", ephemeral=True)

    @removal.command(name="kick", description="Kicks a user from the server and optionally logs the reason.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, reason: str = "No reason provided"):
        interaction = ctx
        try:
            await member.kick(reason=reason)
            await interaction.response.send_message(f"User {member} has been kicked for: {reason}")
            self.log_command('kick', ctx.author.id, str(ctx.author), member.id, str(member), reason)
        except discord.Forbidden:
            await interaction.response.send_message("I do not have permission to kick this user.", ephemeral=True)
        except discord.HTTPException:
            await interaction.response.send_message("An error occurred while trying to kick this user.", ephemeral=True)

    @mod.command(name="mute", description="Mutes a user for a specified duration or indefinitely, with an optional reason.")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, duration: int = None, reason: str = "No reason provided"):
        interaction = ctx
        role = discord.utils.get(interaction.guild.roles, name="Muted")
        if not role:
            await interaction.response.send_message("Muted role not found. Please create a 'Muted' role.", ephemeral=True)
            return
        await member.add_roles(role, reason=reason)
        self.log_command('mute', ctx.author.id, str(ctx.author), member.id, str(member), reason)
        if duration:
            await interaction.response.send_message(f"User {member} has been muted for {duration} seconds for: {reason}")
            await asyncio.sleep(duration)
            await member.remove_roles(role, reason="Mute duration expired.")
            self.log_command('unmute (auto)', ctx.author.id, str(ctx.author), member.id, str(member), "Mute duration expired")
        else:
            await interaction.response.send_message(f"User {member} has been muted indefinitely for: {reason}")

    @mod.command(name="unmute", description="Unmutes a user.")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        interaction = ctx
        role = discord.utils.get(interaction.guild.roles, name="Muted")
        if role in member.roles:
            await member.remove_roles(role)
            await interaction.response.send_message(f"User {member} has been unmuted.")
            self.log_command('unmute', ctx.author.id, str(ctx.author), member.id, str(member))
        else:
            await interaction.response.send_message(f"User {member} is not muted.", ephemeral=True)

    @mod.command(name="warn", description="Issues a warning to a user, with the reason logged.")
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, reason: str = "No reason provided"):
        interaction = ctx
        await interaction.response.send_message(f"User {member} has been warned for: {reason}")
        # Log the warning
        self.log_command('warn', ctx.author.id, str(ctx.author), member.id, str(member), reason)
        log_channel = discord.utils.get(interaction.guild.text_channels, name="log-channel")
        if log_channel:
            await log_channel.send(f"User {member} has been warned by {interaction.user} for: {reason}")

    @mod.command(name="timeout", description="Temporarily restricts a user from sending messages or participating in voice channels.")
    @commands.has_permissions(manage_roles=True)
    async def timeout(self, ctx, member: discord.Member, duration: int, reason: str = "No reason provided"):
        interaction = ctx
        role = discord.utils.get(interaction.guild.roles, name="Timeout")
        if not role:
            await interaction.response.send_message("Timeout role not found. Please create a 'Timeout' role.", ephemeral=True)
            return
        await member.add_roles(role, reason=reason)
        await interaction.response.send_message(f"User {member} has been put in timeout for {duration} seconds for: {reason}")
        self.log_command('timeout', ctx.author.id, str(ctx.author), member.id, str(member), reason)
        await asyncio.sleep(duration)
        await member.remove_roles(role, reason="Timeout duration expired.")
        self.log_command('untimeout', ctx.author.id, str(ctx.author), member.id, str(member), "Timeout duration expired")

    @removal.command(name="softban", description="Bans and immediately unbans a user, effectively kicking them and deleting their recent messages.")
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, member: discord.Member, reason: str = "No reason provided"):
        interaction = ctx
        try:
            await interaction.guild.ban(member, reason=reason, delete_message_days=7)
            await interaction.guild.unban(member, reason="Softban complete")
            await interaction.response.send_message(f"User {member} has been softbanned for: {reason}")
            self.log_command('softban', ctx.author.id, str(ctx.author), member.id, str(member), reason)
        except discord.Forbidden:
            await interaction.response.send_message("I do not have permission to ban/unban this user.", ephemeral=True)
        except discord.HTTPException:
            await interaction.response.send_message("An error occurred while trying to softban this user.", ephemeral=True)

    @removal.command(name="purge", description="Deletes a specified number of messages from a channel.")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, number: int):
        interaction = ctx
        await interaction.channel.purge(limit=number)
        await interaction.response.send_message(f"Deleted {number} messages.")
        self.log_command('purge', ctx.author.id, str(ctx.author), reason=f"Deleted {number} messages")
        log_channel = discord.utils.get(interaction.guild.text_channels, name="log-channel")
        if log_channel:
            await log_channel.send(f"Deleted {number} messages.")

    @mod.command(name="lockdown", description="Locks a channel for a specified duration or until manually unlocked, with an optional reason.")
    @commands.has_permissions(manage_channels=True)
    async def lockdown(self, ctx, duration: int = None, reason: str = "No reason provided"):
        interaction = ctx
        overwrite = discord.PermissionOverwrite(send_messages=False)
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        await interaction.response.send_message(f"Channel locked down for {duration} seconds for: {reason}" if duration else f"Channel locked down indefinitely for: {reason}")
        self.log_command('lockdown', ctx.author.id, str(ctx.author), reason=reason)
        if duration:
            await asyncio.sleep(duration)
            await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=None)
            await interaction.channel.send("Channel lockdown lifted.")
            self.log_command('unlock (auto)', ctx.author.id, str(ctx.author))

    @mod.command(name="unlock", description="Unlocks a previously locked channel.")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        interaction = ctx
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=None)
        await interaction.response.send_message("Channel unlocked.")
        self.log_command('unlock', ctx.author.id, str(ctx.author))

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Moderation(bot)) # add the cog to the bot
