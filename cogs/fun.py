import discord
from discord.ext import commands
import random

class fun(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot
    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot


    fun = discord.SlashCommandGroup("fun", "fun commands") # create a Slash Command Group called "Fun"
    randomfun = fun.create_subgroup(
        "randomfun",
        "randomfun commands"
    )
    mathfun = fun.create_subgroup(
        "mathfun",
        "fun math commands"
    )

    @randomfun.command(description="Flip a coin to get heads or tails.")
    async def flip(self, ctx):
        coin = ['Heads', 'Tails']
        await ctx.send(f"You got: {random.choice(coin)}")

    @fun.command(description="Quote a specific message in the channel.")
    async def quote(self, ctx, message: discord.Message = None):
        if message is None:
            await ctx.send("Please provide a valid message ID or mention a user.")
        else:
            await ctx.send(f"Quoting message: {message.content}")

    @mathfun.command(description="Calculate a mathematical expression.")
    async def calc(self, ctx, expression: str):
        try:
            result = eval(expression)
            await ctx.send(f"Result: {result}")
        except Exception as e:
            await ctx.send(f"Error: {e}")

    @randomfun.command(description="Sends a random joke.")
    async def joke(self, ctx):
        interaction = ctx
        jokes = ["Why don't scientists trust atoms? Because they make up everything!", "Why did the chicken join a band? Because it had the drumsticks!"]
        await interaction.response.send_message(random.choice(jokes))


    @randomfun.command(description="Rolls a virtual dice.")
    #@app_commands.describe(dice="The type of dice to roll (e.g., d6, d20)")
    async def roll(self, ctx, dice: str):
        interaction = ctx
        sides = int(dice[1:])
        result = random.randint(1, sides)
        await interaction.response.send_message(f'You rolled a {result}')

    @randomfun.command(description="Answers a yes/no question.")
    #@app_commands.describe(question="The question to ask the magic 8-ball")
    async def eight_ball(self, ctx, question: str):
        interaction = ctx
        responses = ["Yes", "No", "Maybe", "Ask again later"]
        await interaction.response.send_message(f'🎱 {random.choice(responses)}')



def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(fun(bot)) # add the cog to the bot