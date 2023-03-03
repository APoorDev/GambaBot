import discord
from discord.ext import commands
import os
import sqlite3
import time

@bot.command()
async def upgrade_cap(ctx):
    user_id = str(ctx.author.id)
    c.execute('SELECT cap, balance FROM money WHERE user_id=?', (user_id,))
    result = c.fetchone()

    if result is None:
        await ctx.send("You need to use the daily command to start playing.")
        return

    cap, balance = result

    if balance < cap * 0.8:
        await ctx.send("You need to have at least 80% of your current cap to upgrade your cap.")
        return

    new_cap = int(cap * 2.5)
    new_balance = balance - int(cap * 0.8)
    await ctx.send(f"You upgraded your money cap to {new_cap} coins by paying {int(cap * 0.8)} coins.")

    c.execute('UPDATE money SET balance = ?, cap = ? WHERE user_id = ?', (new_balance, new_cap, user_id))
    conn.commit()