import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # Bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name='join', description='Joins a voice channel')
    async def join(self, ctx):
        if ctx.voice_client:
            await ctx.respond('Already connected to a voice channel, or I joined the voice channel', ephemeral=True)
        else:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
                await ctx.respond('Joined the voice channel.', ephemeral=True)
            else:
                await ctx.respond("You are not connected to a voice channel.", ephemeral=True)

    @discord.slash_command(name='leave', description='Leaves the voice channel')
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.respond('Disconnected from the voice channel.', ephemeral=True)
        else:
            await ctx.respond('I am not connected to a voice channel.', ephemeral=True)

    @discord.slash_command(name='play', description='Plays a song from a URL')
    async def play(self, ctx, url: str):
        await ctx.defer()  # Acknowledge the interaction immediately
        try:
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            if ctx.voice_client is None:
                if ctx.author.voice:
                    await ctx.author.voice.channel.connect()
                else:
                    await ctx.followup.send("You are not connected to a voice channel.", ephemeral=True)
                    return

            ctx.voice_client.play(player, after=lambda e: print(f"Playback error: {e}") if e else None)
            await ctx.followup.send(f'Now playing: {player.title}', ephemeral=True)
        except Exception as e:
            await ctx.followup.send(f"An error occurred: {str(e)}", ephemeral=True)
            print(f"Error in play command: {e}")
        

    @discord.slash_command(name='pause', description='Pauses the current song')
    async def pause(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.respond('Paused the song.', ephemeral=True)
        else:
            await ctx.respond('No song is currently playing.', ephemeral=True)

    @discord.slash_command(name='resume', description='Resumes the current song')
    async def resume(self, ctx):
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.respond('Resumed the song.', ephemeral=True)
        else:
            await ctx.respond('The song is not paused.', ephemeral=True)

    @discord.slash_command(name='stop', description='Stops the current song')
    async def stop(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.respond('Stopped the song.', ephemeral=True)
        else:
            await ctx.respond('No song is currently playing.', ephemeral=True)

    @play.before_invoke
    @join.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.respond("You are not connected to a voice channel.", ephemeral=True)
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

def setup(bot):
    bot.add_cog(Music(bot))
