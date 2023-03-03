import discord
from discord.ext import commands
import os
import sqlite3
import time

class Gamba(commands):
    def __init__(self, bot):
        self.bot = commands.Bot(command_prefix=os.getenv('DISCORD_PREFIX'),intents=discord.Intents.all())
        self.conn = sqlite3.connect('money.db')
        self.c = self.conn.cursor()

        # Create table if it doesn't exist
        self.c.execute('''CREATE TABLE IF NOT EXISTS money
             (user_id TEXT PRIMARY KEY, balance INTEGER, last_daily INTEGER, cap INTEGER)''')

    # Init the user if it is their first message
    def init_user(self,user_id):
        balance = 0
        last_daily = 0
        cap = 10000
        self.c.execute('REPLACE INTO money (user_id, balance, last_daily, cap) VALUES (?, ?, ?, ?)', (user_id, balance, 0, cap))
        return

    # Daily reward command
    @commands.command()
    async def daily(self, ctx):
        user_id = str(ctx.author.id)
        self.c.execute('SELECT balance, last_daily, cap FROM money WHERE user_id=?', (user_id,))
        result = c.fetchone()
        amount = 100
        if result is None:
            self.init_user(user_id)
            self.c.execute('SELECT balance, last_daily, cap FROM money WHERE user_id=?', (user_id,))
            result = c.fetchone()
        balance, last_daily, cap = result

        if time.time() - last_daily < 86400:
            await ctx.send("You can only claim your daily reward once every 24 hours.")
            return
    
        if balance + amount > cap:
            await ctx.send("You have reached your money cap. Use `!upgrade_cap` command to increase your cap.")
            return
    
        new_balance = balance + amount
        await ctx.send(f"You claimed your daily reward of 100 coins! Your new balance is {new_balance} coins.")

        self.c.execute('UPDATE money SET balance = ?, last_daily = ? WHERE user_id = ?', (new_balance, int(time.time()), user_id))
        self.conn.commit()
        
def setup(bot):
    bot.run(os.getenv('DISCORD_TOKEN'))