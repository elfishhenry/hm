#not that qol
import discord
from discord.ext import commands


class qol(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot
    
    copy = discord.SlashCommandGroup("copy", "copying something from discord") # create a Slash Command Group called "copy"
    oqol = copy.create_subgroup(
        "noncopyqol",
        "nodes"
    )


    @copy.command(name='copy_channels', description='Copy channels from one server to another')
    @commands.has_permissions(administrator=True)
    #@commands.command.describe( source_guild_id='The ID of the source guild', target_guild_id='The ID of the target guild')
    async def copy_channels(self, ctx, source_guild_id: str, target_guild_id: str):
        interaction = ctx
        try:
            source_guild_id = int(source_guild_id)
            target_guild_id = int(target_guild_id)
        except ValueError:
            await interaction.response.send_message("Invalid guild IDs provided. Please ensure you provide valid integers.", ephemeral=True)
            return

        source_guild = commands.get_guild(source_guild_id)
        target_guild = commands.get_guild(target_guild_id)

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



    @copy.command(name="copy_role_positions")
    @commands.has_permissions(administrator=True)
    async def copyroles(self, ctx, source_server_id: str, destination_server_id: str):
        try:
            source_server_id = int(source_server_id)
            destination_server_id = int(destination_server_id)

            source_guild = commands.get_guild(source_server_id)
            destination_guild = commands.get_guild(destination_server_id)

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


    @oqol.command(name='rolescopy', description='Copy roles from one server to another')
    @commands.has_permissions(administrator=True)
    #@app_commands.describe(source_guild_id='The ID of the source guild', target_guild_id='The ID of the target guild')
    async def copy_roles(self, ctx, source_guild_id: str, target_guild_id: str):
        interaction = ctx
        try:
            source_guild_id = int(source_guild_id)
            target_guild_id = int(target_guild_id)
        except ValueError:
            await interaction.response.send_message("Invalid guild IDs provided. Please ensure you provide valid integers.", ephemeral=True)
            return

        source_guild = commands.get_guild(source_guild_id)
        target_guild = commands.get_guild(target_guild_id)

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


def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(qol(bot)) # add the cog to the bot