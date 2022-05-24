import logging
from dotenv import load_dotenv
from glue.discord_bot.client import Client
from glue.database.database import Database
from glue.discord_bot.cogs.on_join import OnJoin
import os
import discord

# add logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# add variable from .env file
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# connection to database
db = Database('database.db')

# setup bot
intents = discord.Intents(guilds=True, members=True,)
bot = Client(command_prefix="$", intents=intents)
bot.add_cog(OnJoin(bot))
bot.run(DISCORD_TOKEN)
