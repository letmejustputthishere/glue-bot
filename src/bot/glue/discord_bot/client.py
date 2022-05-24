from discord.ext import commands
from dotenv import load_dotenv
import os

# read token from .env file
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# discord bot class


class Client(commands.Bot):
    # register an event, on_ready event is called when bot finished logging in and settings things up
    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self))

    # on_message event is called when a message is sent
    async def on_message(self, message):
        # ignore our own messages
        if message.author == self.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')
