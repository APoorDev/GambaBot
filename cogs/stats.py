from discord.ext import commands
import sqlite3

conn = sqlite3.connect('money.db')
c = conn.cursor()

class Stats(commands.Cog):
    @commands.command()
    async def stats(self, ctx):
        user_id = str(ctx.author.id)
        c.execute('SELECT balance, cap FROM money WHERE user_id=?', (user_id,))
        result = c.fetchone()
        if result is None:
            await ctx.send("You need to use the daily command to start playing.")
            return
        balance,cap=result
        await ctx.send(f"Your balance is {balance} coins. \nYour maximum capacity is {cap}.")

async def setup(bot):
    await bot.add_cog(Stats(bot))