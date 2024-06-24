import discord
from discord.ext import commands
import random

class fun(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot
    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @commands.slash_command(name="avatar", description="Show the avatar of a specified user.")
    async def avatar(ctx, user: discord.User = None):
        if user is None:
            user = ctx.author
        await ctx.send(user.avatar_url)


    @commands.slash_command(name="flip", description="Flip a coin to get heads or tails.")
    async def flip(ctx):
        coin = ['Heads', 'Tails']
        await ctx.send(f"You got: {random.choice(coin)}")

    @commands.slash_command(name="quote", description="Quote a specific message in the channel.")
    async def quote(ctx, message: discord.Message = None):
        if message is None:
            await ctx.send("Please provide a valid message ID or mention a user.")
        else:
            await ctx.send(f"Quoting message: {message.content}")

    @commands.slash_command(name="calc", description="Calculate a mathematical expression.")
    async def calc(ctx, expression: str):
        try:
            result = eval(expression)
            await ctx.send(f"Result: {result}")
        except Exception as e:
            await ctx.send(f"Error: {e}")

    @commands.slash_command(name="joke", description="Sends a random joke.")
    async def joke(interaction: discord.Interaction):
        jokes = ["Why don't scientists trust atoms? Because they make up everything!", "Why did the chicken join a band? Because it had the drumsticks!"]
        await interaction.response.send_message(random.choice(jokes))


    @commands.slash_command(name="roll", description="Rolls a virtual dice.")
    #@app_commands.describe(dice="The type of dice to roll (e.g., d6, d20)")
    async def roll(interaction: discord.Interaction, dice: str):
        sides = int(dice[1:])
        result = random.randint(1, sides)
        await interaction.response.send_message(f'You rolled a {result}')

    @commands.slash_command(name="eight_ball", description="Answers a yes/no question.")
    #@app_commands.describe(question="The question to ask the magic 8-ball")
    async def eight_ball(interaction: discord.Interaction, question: str):
        responses = ["Yes", "No", "Maybe", "Ask again later"]
        await interaction.response.send_message(f'🎱 {random.choice(responses)}')

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(fun(bot)) # add the cog to the bot