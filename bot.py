import discord
from discord.ext import commands, tasks
import os
import sqlite3
import random
import asyncio

bot = commands.Bot(command_prefix=os.getenv('DISCORD_PREFIX'),intents=discord.Intents.all())
bot = bot

# Connect to Database
conn = sqlite3.connect('money.db')
c = conn.cursor()
# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS money
            (user_id TEXT PRIMARY KEY, balance INTEGER, last_daily INTEGER, cap INTEGER)''')

@tasks.loop(minutes=1.0)
async def status_task() -> None:
    statuses = ["Stealing your money!", "Come on, bet a little more.", "!daily"]
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))

# Load all the commands
async def load_cogs() -> None:
    for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                await bot.load_extension(f"cogs.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")

asyncio.run(load_cogs())
bot.run(os.getenv('DISCORD_TOKEN'))
    