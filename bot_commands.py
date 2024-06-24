import os
import discord
import logging
import pycord
from discord.ext import commands
from dotenv import load_dotenv
from discord import Intents, Interaction
from discord import app_commands
import asyncio
import random



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
intents.bans = True
intents.members = True 
intents.guilds = True
intents.guild_messages = True


# Create the client object with the specified intents
client = commands.Bot(command_prefix='.', intents=intents)



bot = client




warnings = {}



@client.event
async def on_ready(message):
    logging.info(f'{client.user} has connected to Discord!')
    print("We have logged in as {0.user}".format(bot))
    try:
        synced = await client.tree.sync()
        logging.info(f"Synced {len(synced)} commands")
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        logging.error(e)
        print(e)
        

@client.tree.command(name="latency", description="Ping the bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Ping or Latency is {round(bot.latency * 1000)}ms")
    print(f'{client.user} has connected to Discord!')
   

#sync slash command
@client.tree.command(name="synccommands", description="madebyelfishhenrytosynccommandscuaseit takes forevaaaaaaaa to sync and i want to test faster")
@app_commands.checks.has_permissions(ban_members=True)
async def on_command(interaction: discord.Interaction):
    await interaction.response.send_message("synced loser, you can check bot.log for wtf happened")
    try:
        synced = await client.tree.sync()
        logging.info(f"Synced via command figureitout you shithead howevermany: {len(synced)}")
        print(f"Synced via command figureitout you shithead howevermany: {len(synced)}")
    except Exception as e:
        logging.error(e)
        print(e)


@bot.tree.command(name='copy_channels', description='Copy channels from one server to another')
@app_commands.describe(source_guild_id='The ID of the source guild', target_guild_id='The ID of the target guild')
async def copy_channels(interaction: discord.Interaction, source_guild_id: str, target_guild_id: str):
    try:
        source_guild_id = int(source_guild_id)
        target_guild_id = int(target_guild_id)
    except ValueError:
        await interaction.response.send_message("Invalid guild IDs provided. Please ensure you provide valid integers.", ephemeral=True)
        return

    source_guild = bot.get_guild(source_guild_id)
    target_guild = bot.get_guild(target_guild_id)

    if not source_guild or not target_guild:
        await interaction.response.send_message("Invalid guild IDs provided.", ephemeral=True)
        return

    # Copy categories
    category_mapping = {}
    for category in source_guild.categories:
        new_category = await target_guild.create_category(
            name=category.name,
            position=category.position,
            overwrites=category.overwrites,
            reason=f"Copied from {source_guild.name} by {interaction.user}"
        )
        category_mapping[category.id] = new_category

    # Copy text and voice channels
    for channel in source_guild.channels:
        if isinstance(channel, discord.TextChannel):
            new_channel = await target_guild.create_text_channel(
                name=channel.name,
                category=category_mapping.get(channel.category_id),
                position=channel.position,
                topic=channel.topic,
                nsfw=channel.nsfw,
                slowmode_delay=channel.slowmode_delay,
                overwrites=channel.overwrites,
                reason=f"Copied from {source_guild.name} by {interaction.user}"
            )
        elif isinstance(channel, discord.VoiceChannel):
            new_channel = await target_guild.create_voice_channel(
                name=channel.name,
                category=category_mapping.get(channel.category_id),
                position=channel.position,
                bitrate=channel.bitrate,
                user_limit=channel.user_limit,
                overwrites=channel.overwrites,
                reason=f"Copied from {source_guild.name} by {interaction.user}"
            )

    await interaction.response.send_message(f"Channels copied from {source_guild.name} to {target_guild.name} successfully.", ephemeral=True)

@bot.tree.command(name='rolescopy', description='Copy roles from one server to another')
@app_commands.describe(source_guild_id='The ID of the source guild', target_guild_id='The ID of the target guild')
async def copy_roles(interaction: discord.Interaction, source_guild_id: str, target_guild_id: str):
    try:
        source_guild_id = int(source_guild_id)
        target_guild_id = int(target_guild_id)
    except ValueError:
        await interaction.response.send_message("Invalid guild IDs provided. Please ensure you provide valid integers.", ephemeral=True)
        return

    source_guild = bot.get_guild(source_guild_id)
    target_guild = bot.get_guild(target_guild_id)

    if not source_guild or not target_guild:
        await interaction.response.send_message("Invalid guild IDs provided.", ephemeral=True)
        return

    for role in source_guild.roles:
        if role.is_default():
            continue  # Skip the @everyone role

        existing_role = discord.utils.get(target_guild.roles, name=role.name)
        if existing_role:
            await interaction.response.send_message(f"Role {role.name} already exists in the target server.", ephemeral=True)
            continue

        await target_guild.create_role(
            name=role.name,
            permissions=role.permissions,
            colour=role.colour,
            hoist=role.hoist,
            mentionable=role.mentionable,
            reason=f"Copied from {source_guild.name} by {interaction.user}"
        )

    await interaction.response.send_message(f"Roles copied from {source_guild.name} to {target_guild.name} successfully.", ephemeral=True)

@bot.command()
async def copyroles(ctx, source_server_id: str, destination_server_id: str):
    try:
        source_server_id = int(source_server_id)
        destination_server_id = int(destination_server_id)

        source_guild = bot.get_guild(source_server_id)
        destination_guild = bot.get_guild(destination_server_id)

        if not source_guild:
            await ctx.send(f"Source server with ID {source_server_id} not found.")
            return
        if not destination_guild:
            await ctx.send(f"Destination server with ID {destination_server_id} not found.")
            return

        # Fetch roles from the source guild
        source_roles = source_guild.roles

        # Create roles in the destination guild
        for role in source_roles:
            try:
                await destination_guild.create_role(
                    name=role.name,
                    permissions=role.permissions,
                    colour=role.colour,
                    hoist=role.hoist,
                    mentionable=role.mentionable,
                    reason=f"Copying role from {source_guild.name}"
                )
            except discord.Forbidden:
                await ctx.send(f"Missing permissions to create roles in {destination_guild.name}")
                return

        await ctx.send(f"Roles copied from {source_guild.name} to {destination_guild.name}")

    except ValueError:
        await ctx.send("Server IDs must be valid integers.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


@client.tree.command(name="testingaaaaaaaaaa", description="testingaaaaaaaaaa")
async def how_are_you(interaction: discord.Interaction):
    await interaction.response.send_message("testingaaaaaaaaaa")


@bot.tree.command(name="ban", description="Ban a user from the server")
@app_commands.checks.has_permissions(ban_members=True)
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
@bot.tree.command(name="unban", description="Unban a user from the server")
@app_commands.checks.has_permissions(ban_members=True)
async def unban(interaction: discord.Interaction, user_id: str, reason: str = "No reason provided"):
    try:
        user = await bot.fetch_user(user_id)
        
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

@bot.tree.command(name="kick", description="Kicks a user from the server and optionally logs the reason.")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    try:
        await member.kick(reason=reason)
        await interaction.response.send_message(f"User {member} has been kicked for: {reason}")
    except discord.Forbidden:
        await interaction.response.send_message("I do not have permission to kick this user.", ephemeral=True)
    except discord.HTTPException:
        await interaction.response.send_message("An error occurred while trying to kick this user.", ephemeral=True)

@bot.tree.command(name="mute", description="Mutes a user for a specified duration or indefinitely, with an optional reason.")
@app_commands.checks.has_permissions(manage_roles=True)
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


@bot.tree.command(name="unmute", description="Unmutes a user.")
@app_commands.checks.has_permissions(manage_roles=True)
async def unmute(interaction: discord.Interaction, member: discord.Member):
    role = discord.utils.get(interaction.guild.roles, name="Muted")
    if role in member.roles:
        await member.remove_roles(role)
        await interaction.response.send_message(f"User {member} has been unmuted.")
    else:
        await interaction.response.send_message(f"User {member} is not muted.", ephemeral=True)





@bot.tree.command(name="warn", description="Issues a warning to a user, with the reason logged.")
@commands.has_permissions(manage_messages=True)
async def warn(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    await interaction.response.send_message(f"User {member} has been warned for: {reason}")
    # Log the warning
    log_channel = discord.utils.get(interaction.guild.text_channels, name="log-channel")
    if log_channel:
        await log_channel.send(f"User {member} has been warned by {interaction.user} for: {reason}")



@bot.tree.command(name="timeout", description="Temporarily restricts a user from sending messages or participating in voice channels.")
@app_commands.checks.has_permissions(manage_roles=True)
async def timeout(interaction: discord.Interaction, member: discord.Member, duration: int, reason: str = "No reason provided"):
    role = discord.utils.get(interaction.guild.roles, name="Timeout")
    if not role:
        await interaction.response.send_message("Timeout role not found. Please create a 'Timeout' role.", ephemeral=True)
        return
    await member.add_roles(role, reason=reason)
    await interaction.response.send_message(f"User {member} has been put in timeout for {duration} seconds for: {reason}")
    await asyncio.sleep(duration)
    await member.remove_roles(role, reason="Timeout duration expired.")





@bot.tree.command(name="softban", description="Bans and immediately unbans a user, effectively kicking them and deleting their recent messages.")
@app_commands.checks.has_permissions(ban_members=True)
async def softban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    try:
        await interaction.guild.ban(member, reason=reason, delete_message_days=7)
        await interaction.guild.unban(member, reason="Softban complete")
        await interaction.response.send_message(f"User {member} has been softbanned for: {reason}")
    except discord.Forbidden:
        await interaction.response.send_message("I do not have permission to ban/unban this user.", ephemeral=True)
    except discord.HTTPException:
        await interaction.response.send_message("An error occurred while trying to softban this user.", ephemeral=True)

@bot.tree.command(name="purge", description="Deletes a specified number of messages from a channel.")
@app_commands.checks.has_permissions(manage_messages=True)
async def purge(interaction: discord.Interaction, number: int):
    await interaction.channel.purge(limit=number)
    log_channel = discord.utils.get(interaction.guild.text_channels, name="log-channel")
    if log_channel:
        await log_channel.send(f"Deleted {number} messages.")

@bot.tree.command(name="lockdown", description="Locks a channel for a specified duration or until manually unlocked, with an optional reason.")
@app_commands.checks.has_permissions(manage_channels=True)
async def lockdown(interaction: discord.Interaction, duration: int = None, reason: str = "No reason provided"):
    overwrite = discord.PermissionOverwrite(send_messages=False)
    await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
    await interaction.response.send_message(f"Channel locked down for {duration} seconds for: {reason}" if duration else f"Channel locked down indefinitely for: {reason}")
    if duration:
        await asyncio.sleep(duration)
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=None)
        await interaction.channel.send("Channel lockdown lifted.")

@bot.tree.command(name="unlock", description="Unlocks a previously locked channel.")
@app_commands.checks.has_permissions(manage_channels=True)
async def unlock(interaction: discord.Interaction):
    await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=None)
    await interaction.response.send_message("Channel unlocked.")

@bot.tree.command(name="slowmode", description="Sets slowmode for a channel to a specified duration.")
@app_commands.checks.has_permissions(manage_channels=True)
async def slowmode(interaction: discord.Interaction, duration: int):
    await interaction.channel.edit(slowmode_delay=duration)
    await interaction.response.send_message(f"Set slowmode to {duration} seconds.")

@bot.tree.command(name="userinfo", description="Displays information about a user, such as join date, roles, and infractions.")
async def userinfo(interaction: discord.Interaction, member: discord.Member):
    embed = discord.Embed(title=f"User Info - {member}", color=discord.Color.blue())
    embed.add_field(name="User ID", value=member.id, inline=True)
    embed.add_field(name="Joined", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    embed.add_field(name="Roles", value=", ".join([role.name for role in member.roles]), inline=True)
    await interaction.response.send_message(embed=embed)

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"Server Info - {guild.name}", color=discord.Color.green())
    embed.add_field(name="Server ID", value=guild.id, inline=True)
    embed.add_field(name="Owner", value=guild.owner, inline=True)
    embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    embed.add_field(name="Member Count", value=guild.member_count, inline=True)
    embed.set_thumbnail(url=guild.icon.url)
    await ctx.send(embed=embed)


@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"User Info - {member}", color=discord.Color.blue())
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Display Name", value=member.display_name, inline=True)
    embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    embed.set_thumbnail(url=member.avatar.url)
    await ctx.send(embed=embed)

@bot.tree.command(name="serverinfo", description="Provides information about the server, such as member count, region, and creation date.")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title=f"Server Info - {guild.name}", color=discord.Color.blue())
    embed.add_field(name="Server ID", value=guild.id, inline=True)
    embed.add_field(name="Members", value=guild.member_count, inline=True)
    embed.add_field(name="Region", value=guild.region, inline=True)
    embed.add_field(name="Created", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="roleinfo", description="Displays information about a specific role.")
async def roleinfo(interaction: discord.Interaction, role: discord.Role):
    embed = discord.Embed(title=f"Role Info - {role.name}", color=role.color)
    embed.add_field(name="Role ID", value=role.id, inline=True)
    embed.add_field(name="Color", value=str(role.color), inline=True)
    embed.add_field(name="Created", value=role.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    embed.add_field(name="Permissions", value=", ".join([perm[0] for perm in role.permissions if perm[1]]), inline=True)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="addrole", description="Adds a specified role to a user.")
@app_commands.checks.has_permissions(manage_roles=True)
async def addrole(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await interaction.response.send_message(f"Added role {role.name} to {member}.")



@bot.tree.command(name="removerole", description="Removes a specified role from a user.")
@app_commands.checks.has_permissions(manage_roles=True)
async def removerole(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await interaction.response.send_message(f"Removed role {role.name} from {member}.")

@bot.tree.command(name="createrole", description="Creates a new role with specified properties.")
@app_commands.checks.has_permissions(manage_roles=True)
async def createrole(interaction: discord.Interaction, name: str, color: int, permissions: int):
    if color < 0 or color > 16777215:
        await interaction.response.send_message("Invalid color value. Please provide a valid integer color value between 0 and 16777215.", ephemeral=True)
        return
    
    role_permissions = discord.Permissions(permissions)
    role = await interaction.guild.create_role(name=name, color=discord.Color(color), permissions=role_permissions)
    await interaction.response.send_message(f"Created role {role.name}.")



@bot.tree.command(name="deleterole", description="Deletes a specified role from the server.")
@app_commands.checks.has_permissions(manage_roles=True)
async def deleterole(interaction: discord.Interaction, role: discord.Role):
    await role.delete()
    await interaction.response.send_message(f"Deleted role {role.name}.")

@bot.tree.command(name="report", description="Allows users to report another user for inappropriate behavior, with the reason logged.")
async def report(interaction: discord.Interaction, member: discord.Member, reason: str):
    # Log the report
    log_channel = discord.utils.get(interaction.guild.text_channels, name="log-channel")
    if log_channel:
        await log_channel.send(f"User {member} has been reported by {interaction.user} for: {reason}")
    await interaction.response.send_message(f"Reported {member} for: {reason}", ephemeral=True)




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






@client.event  
async def on_tree_command_error(interaction: Interaction, error: discord.app_commands.AppCommandError):
    if isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message("You don't have the necessary permissions to use this command.")
    elif isinstance(error, commands.MemberNotFound):
        await interaction.response.send_message("Member not found.")
    else:
        print(error)  # Print the error in the console for debugging purposes



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

@bot.tree.command(name="joke", description="Sends a random joke.")
async def joke(interaction: discord.Interaction):
    jokes = ["Why don't scientists trust atoms? Because they make up everything!", "Why did the chicken join a band? Because it had the drumsticks!"]
    await interaction.response.send_message(random.choice(jokes))


# Command to send an embed



@bot.tree.command(name="ping", description="Checks the bot's responsiveness.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@bot.tree.command(name="roll", description="Rolls a virtual dice.")
@app_commands.describe(dice="The type of dice to roll (e.g., d6, d20)")
async def roll(interaction: discord.Interaction, dice: str):
    sides = int(dice[1:])
    result = random.randint(1, sides)
    await interaction.response.send_message(f'You rolled a {result}')

@bot.tree.command(name="eight_ball", description="Answers a yes/no question.")
@app_commands.describe(question="The question to ask the magic 8-ball")
async def eight_ball(interaction: discord.Interaction, question: str):
    responses = ["Yes", "No", "Maybe", "Ask again later"]
    await interaction.response.send_message(f'🎱 {random.choice(responses)}')



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


#  Run the client with the specified token
client.run(TOKEN)