import discord
from discord.ext import commands
import os
import sqlite3
import random
import time

# The coinflip command
@bot.command()
async def flip(ctx, amount: int):
    user_id = str(ctx.author.id)
    c.execute('SELECT balance, cap FROM money WHERE user_id=?', (user_id,))
    result = c.fetchone()

    if result is None:
        await ctx.send("You need to use the daily command to start playing.")
        return 
    balance, cap = result

    if balance + amount > cap:
        await ctx.send("You have reached your money cap. Use `!upgrade_cap` command to increase your cap.")
        return

    outcome = random.choice(["heads", "tails"])
    if outcome == "heads":
        new_balance = balance + amount
        await ctx.send(f"Congratulations! You won {amount} coins! Your new balance is {new_balance} coins.")
    else:
        new_balance = balance - amount
        await ctx.send(f"Sorry, you lost {amount} coins. Your new balance is {new_balance} coins.")

    c.execute('UPDATE money SET balance = ? WHERE user_id = ?', (new_balance, user_id))
    conn.commit()