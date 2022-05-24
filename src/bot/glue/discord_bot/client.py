from discord.ext import commands
from discord import app_commands
from discord import Guild
import discord
from dotenv import load_dotenv
import os

# read token from .env file
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

MY_GUILD = discord.Object(id=974261271857860649)  # replace with your guild id


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

    async def on_ready(self):
        print(f"We have logged in as {self.user}.")

    # on_message event is called when a message is sent
    async def on_message(self, message):
        # ignore our own messages
        if message.author == self.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

    async def on_guild_join(self, guild: Guild):
        # get the owner of a guild, this needs the "members" intent
        owner = guild.owner
        # send a message to the owner if it exists
        if owner:
            await owner.send(
                f"Hey there, thanks for having me 🥳\n"
                f"If you want to setup an NFT project to grant holder roles to members, run the `/setup` command in a channel of the respective server.\n"
                f"If you feel lost, you can always run `/help` to get and overview of what I can do 😊\n"
            )
