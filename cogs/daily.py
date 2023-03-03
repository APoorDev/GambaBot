from discord.ext import commands
import time
import sqlite3

conn = sqlite3.connect('money.db')
c = conn.cursor()

class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def init_user(self, user_id):
        balance = 0
        last_daily = 0
        cap = 10000
        c.execute('REPLACE INTO money (user_id, balance, last_daily, cap) VALUES (?, ?, ?, ?)', (user_id, balance, 0, cap))
        return

    # Daily reward command
    @commands.command()
    async def daily(self, ctx):
        user_id = str(ctx.author.id)
        c.execute('SELECT balance, last_daily, cap FROM money WHERE user_id=?', (user_id,))
        result = c.fetchone()
        amount = 100
        if result is None:
            self.init_user(user_id)
            c.execute('SELECT balance, last_daily, cap FROM money WHERE user_id=?', (user_id,))
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

        c.execute('UPDATE money SET balance = ?, last_daily = ? WHERE user_id = ?', (new_balance, int(time.time()), user_id))
        conn.commit()
    
async def setup(bot):
    await bot.add_cog(Daily(bot))