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
intents.bans = True


# Create the client object with the specified intents
client = commands.Bot(command_prefix='.', intents=intents)

bot = client

@client.event
async def on_ready():
    logging.info(f'{client.user} has connected to Discord!')
    print(f'{client.user} has connected to Discord!')


@client.command()
async def help(ctx, command=None):
    if command:
        # Get specific command help
        cmd = client.get_command(command)
        if not cmd:
            await ctx.send(f'Command "{command}" not found.')
            return
        command_help = f'**Command Name:** {cmd.name}\n'
        if cmd.description:
            command_help += f'**Description:** {cmd.description}\n'
        if cmd.usage:
            command_help += f'**Usage:** `{cmd.usage}`\n'
        await ctx.send(command_help)
    else:
        # Get list of all commands
        command_list = []
        for command in client.commands:
            if not command.hidden:  # You can set command.hidden=True for commands you want to hide from help
                command_list.append(f'**{command.name}** - {command.description or "No description provided."}')
        
        help_message = '\n'.join(command_list)
        embed = discord.Embed(
            title="Command List",
            description=help_message,
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)


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
async def on_ready():
    print(f'Logged in as {client.user} and mod commands should be ready to use.')

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} has been banned.')

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} has been kicked.')



@client.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    # Replace with your custom warning logic (e.g., logging warnings)
    await ctx.send(f'{member.mention} has been warned for: {reason}')

@client.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")  # Replace with your muted role name
    if not muted_role:
        # Create muted role if it doesn't exist
        muted_role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, speak=False, send_messages=False)
    
    await member.add_roles(muted_role)
    await ctx.send(f'{member.mention} has been muted.')








@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the necessary permissions to use this command.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Member not found.")
    else:
        print(error)  # Print the error in the console for debugging purposes




# Run the client with the specified token
client.run(TOKEN)