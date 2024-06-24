import discord
from discord.ext import commands
import json
import os
import random
from datetime import datetime, timedelta
import discord
import json



            # File to store user data
DATA_FILE = 'economy_data.json'
# Load user data from file
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        user_data = json.load(f)
else:
    user_data = {}
    with open(DATA_FILE, 'w') as f:
        json.dump(user_data, f)

def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(user_data, f)

def get_balance(user_id):
    return user_data.get(user_id, {}).get('balance', 0)

def update_balance(user_id, amount):
    if user_id not in user_data:
        user_data[user_id] = {'balance': 0, 'bank': 0, 'inventory': [], 'last_daily': None, 'xp': 0, 'level': 1, 'achievements': []}
    user_data[user_id]['balance'] += amount
    add_xp(user_id, amount // 10)
    save_data()

def add_xp(user_id, amount):
    user = user_data.get(user_id, {})
    user['xp'] = user.get('xp', 0) + amount
    while user['xp'] >= user['level'] * 100:
        user['xp'] -= user['level'] * 100
        user['level'] += 1
        user['balance'] += 25  # Reward for leveling up
        user_data[user_id] = user
        save_data()
        return True
    return False



class economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



# Command to check balance
    @commands.command(name='balance')
    async def balance(ctx):
        user_id = str(ctx.author.id)
        balance = get_balance(user_id)
        bank_balance = user_data[user_id].get('bank', 0)
        level = user_data[user_id].get('level', 1)
        xp = user_data[user_id].get('xp', 0)
        await ctx.send(f"{ctx.author.mention}, your balance is ${balance}, you have ${bank_balance} in the bank, you are level {level} with {xp} XP.")

    @commands.command(name='ecolist')
    async def ecolist(ctx):
        commands_list = """
    **Economy Commands:**
    - `!balance`: Check your balance and bank balance.
    - `!earn`: Earn a random amount of money.
    - `!daily`: Claim your daily reward.
    - `!work`: Work a random job to earn money.
    - `!deposit <amount>`: Deposit money into your bank.
    - `!withdraw <amount>`: Withdraw money from your bank.
    - `!gamble <amount>`: Gamble an amount of money.
    - `!inventory`: Check your inventory.
    - `!buy <item>`: Buy an item from the shop.
    - `!shop`: Display available shop items.
    - `!give <@user> <amount>`: Give money to another user.
    - `!leaderboard`: Display the leaderboard.
    - `!trade <@user> <your_item> <their_item>`: Trade items with another user.
    - `!use <item>`: Use an item from your inventory.
    - `!reset`: Reset all balances (Admin only).

    **Description of Commands:**
    - **balance**: Displays your current balance, bank balance, level, and XP.
    - **earn**: Earns a random amount of money and adds XP.
    - **daily**: Claims a daily reward (once every 24 hours).
    - **work**: Earns money by working a random job.
    - **deposit**: Deposits specified amount of money into your bank.
    - **withdraw**: Withdraws specified amount of money from your bank.
    - **gamble**: Gambles a specified amount of money with a 50% chance to win or lose.
    - **inventory**: Shows the items you currently own.
    - **buy**: Buys an item from the shop using your balance.
    - **shop**: Lists all available items in the shop.
    - **give**: Transfers specified amount of money to another user.
    - **leaderboard**: Displays the top users based on their total wealth.
    - **trade**: Trades items between users.
    - **use**: Uses an item from your inventory.
    - **reset**: Resets all users' balances (Admin only).
    """
        await ctx.send(commands_list)



    # Command to earn money
    @commands.command(name='earn')
    async def earn(ctx):
        user_id = str(ctx.author.id)
        earnings = random.randint(1, 10)
        update_balance(user_id, earnings)
        leveled_up = add_xp(user_id, earnings // 10)
        level_message = " You leveled up!" if leveled_up else ""
        await ctx.send(f"{ctx.author.mention}, you earned ${earnings}! Your new balance is ${get_balance(user_id)}.{level_message}")

    # Command for daily rewards
    @commands.command(name='daily')
    async def daily(ctx):
        user_id = str(ctx.author.id)
        if user_id not in user_data:
            user_data[user_id] = {'balance': 0, 'bank': 0, 'inventory': [], 'last_daily': None, 'xp': 0, 'level': 1, 'achievements': []}
        
        last_daily = user_data[user_id].get('last_daily')
        now = datetime.utcnow()
        if last_daily:
            last_daily = datetime.fromisoformat(last_daily)
            if now - last_daily < timedelta(hours=24):
                await ctx.send(f"{ctx.author.mention}, you have already claimed your daily reward. Try again later.")
                return

        reward = 100
        user_data[user_id]['last_daily'] = now.isoformat()
        update_balance(user_id, reward)
        leveled_up = add_xp(user_id, reward // 10)
        level_message = " You leveled up!" if leveled_up else ""
        await ctx.send(f"{ctx.author.mention}, you claimed your daily reward of ${reward}! Your new balance is ${get_balance(user_id)}.{level_message}")

    # Command to work and earn money
    @commands.command(name='work')
    async def work(ctx):
        user_id = str(ctx.author.id)
        jobs = ["developer", "designer", "manager", "writer", "teacher"]
        job = random.choice(jobs)
        earnings = random.randint(1, 100)
        update_balance(user_id, earnings)
        leveled_up = add_xp(user_id, earnings // 10)
        level_message = " You leveled up!" if leveled_up else ""
        await ctx.send(f"{ctx.author.mention}, you worked as a {job} and earned ${earnings}! Your new balance is ${get_balance(user_id)}.{level_message}")

    # Command to deposit money into the bank
    @commands.command(name='deposit')
    async def deposit(ctx, amount: int):
        user_id = str(ctx.author.id)
        balance = get_balance(user_id)
        if amount > balance:
            await ctx.send(f"{ctx.author.mention}, you don't have enough money to deposit.")
            return
        user_data[user_id]['balance'] -= amount
        user_data[user_id]['bank'] += amount
        save_data()
        await ctx.send(f"{ctx.author.mention}, you deposited ${amount} into your bank. Your new balance is ${get_balance(user_id)} and you have ${user_data[user_id]['bank']} in the bank.")

    # Command to withdraw money from the bank
    @commands.command(name='withdraw')
    async def withdraw(ctx, amount: int):
        user_id = str(ctx.author.id)
        bank_balance = user_data[user_id].get('bank', 0)
        if amount > bank_balance:
            await ctx.send(f"{ctx.author.mention}, you don't have enough money in the bank to withdraw.")
            return
        user_data[user_id]['bank'] -= amount
        user_data[user_id]['balance'] += amount
        save_data()
        await ctx.send(f"{ctx.author.mention}, you withdrew ${amount} from your bank. Your new balance is ${get_balance(user_id)} and you have ${user_data[user_id]['bank']} in the bank.")

    # Command to gamble money
    @commands.command(name='gamble')
    async def gamble(ctx, amount: int):
        user_id = str(ctx.author.id)
        balance = get_balance(user_id)
        if amount > balance:
            await ctx.send(f"{ctx.author.mention}, you don't have enough money to gamble.")
            return

        if random.choice([True, False]):
            user_data[user_id]['balance'] += amount
            result = f"won ${amount}"
        else:
            user_data[user_id]['balance'] -= amount
            result = f"lost ${amount}"
        
        leveled_up = add_xp(user_id, amount // 10)
        level_message = " You leveled up!" if leveled_up else ""
        save_data()
        await ctx.send(f"{ctx.author.mention}, you gambled and {result}. Your new balance is ${get_balance(user_id)}.{level_message}")

    # Command to check inventory
    @commands.command(name='inventory')
    async def inventory(ctx):
        user_id = str(ctx.author.id)
        inventory = user_data.get(user_id, {}).get('inventory', [])
        if not inventory:
            await ctx.send(f"{ctx.author.mention}, your inventory is empty.")
        else:
            await ctx.send(f"{ctx.author.mention}, your inventory: {', '.join(inventory)}")

    # Command to buy items from the shop
    @commands.command(name='buy')
    async def buy(ctx, item: str):
        user_id = str(ctx.author.id)
        shop_items = {
            "laptop": 1000,
            "phone": 500,
            "car": 20000,
            "boost": 10000  # This could be an item that boosts earnings
        }

        if item not in shop_items:
            await ctx.send(f"{ctx.author.mention}, item not found in the shop.")
            return

        cost = shop_items[item]
        balance = get_balance(user_id)
        if balance < cost:
            await ctx.send(f"{ctx.author.mention}, you don't have enough money to buy {item}.")
            return

        user_data[user_id]['balance'] -= cost
        user_data[user_id].setdefault('inventory', []).append(item)
        save_data()
        await ctx.send(f"{ctx.author.mention}, you bought {item} for ${cost}. Your new balance is ${get_balance(user_id)}.")

    # Command to display shop items
    @commands.command(name='shop')
    async def shop(ctx):
        shop_items = {
            "laptop": 1000,
            "phone": 500,
            "car": 20000,
            "boost": 10000  # This could be an item that boosts earnings
        }
        shop_message = "**Shop Items:**\n"
        for item, cost in shop_items.items():
            shop_message += f"**{item.capitalize()}**: ${cost}\n"
        await ctx.send(shop_message)

    # Command to give money to another user
    @commands.command(name='give')
    async def give(ctx, member: discord.Member, amount: int):
        giver_id = str(ctx.author.id)
        receiver_id = str(member.id)

        if amount <= 0:
            await ctx.send(f"{ctx.author.mention}, you need to give a positive amount.")
            return

        if giver_id not in user_data or user_data[giver_id]['balance'] < amount:
            await ctx.send(f"{ctx.author.mention}, you don't have enough money.")
            return
        
        if receiver_id not in user_data:
            user_data[receiver_id] = {'balance': 0, 'bank': 0, 'inventory': [], 'last_daily': None, 'xp': 0, 'level': 1, 'achievements': []}
        
        user_data[giver_id]['balance'] -= amount
        user_data[receiver_id]['balance'] += amount
        save_data()
        await ctx.send(f"{ctx.author.mention} gave ${amount} to {member.mention}. Your new balance is ${get_balance(giver_id)}.")

    # Command to display leaderboard
    @commands.command(name='leaderboard')
    async def leaderboard(ctx):
        sorted_users = sorted(user_data.items(), key=lambda x: x[1]['balance'] + x[1].get('bank', 0), reverse=True)
        leaderboard_message = "**Leaderboard:**\n"
        for i, (user_id, data) in enumerate(sorted_users):
            user = await commands.fetch_user(user_id)
            total = data['balance'] + data.get('bank', 0)
            leaderboard_message += f"{i + 1}. **{user.name}**: ${total} (Balance: ${data['balance']}, Bank: ${data.get('bank', 0)}, Level: {data['level']})\n"
        await ctx.send(leaderboard_message)

    # Command to reset everyone's balance (for admin use)
    @commands.command(name='reset')
    @commands.has_permissions(administrator=True)
    async def reset(ctx):
        global user_data
        user_data = {}
        save_data()
        await ctx.send("All balances have been reset.")

    # Command to trade items with another user
    @commands.command(name='trade')
    async def trade(ctx, member: discord.Member, your_item: str, their_item: str):
        user_id = str(ctx.author.id)
        receiver_id = str(member.id)

        if your_item not in user_data[user_id]['inventory']:
            await ctx.send(f"{ctx.author.mention}, you don't have {your_item}.")
            return

        if their_item not in user_data[receiver_id]['inventory']:
            await ctx.send(f"{ctx.author.mention}, {member.mention} doesn't have {their_item}.")
            return

        user_data[user_id]['inventory'].remove(your_item)
        user_data[receiver_id]['inventory'].remove(their_item)

        user_data[user_id]['inventory'].append(their_item)
        user_data[receiver_id]['inventory'].append(your_item)

        save_data()
        await ctx.send(f"{ctx.author.mention} traded {your_item} with {member.mention} for {their_item}.")

    # Command to use an item
    @commands.command(name='use')
    async def use(ctx, item: str):
        user_id = str(ctx.author.id)
        if item not in user_data[user_id]['inventory']:
            await ctx.send(f"{ctx.author.mention}, you don't have {item}.")
            return

        if item == "boost":
            user_data[user_id]['balance'] += 1000
            await ctx.send(f"{ctx.author.mention}, you used a {item} and gained $1000!")
        
        user_data[user_id]['inventory'].remove(item)
        save_data()

def setup(bot):
    bot.add_cog(economy(bot))