from discord.ext import tasks
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


class Bot(commands.Bot):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents, command_prefix="")

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)
        self.check_ownership.start()

        # to add a cog do the following
        # self.add_cog()

    # loop
    @tasks.loop(seconds=1)
    async def check_ownership(self):
        print("moin")

    # called when bot is ready
    async def on_ready(self):
        print(f"We have logged in as {self.user}.")

    # on_message event is called when a message is sent
    async def on_message(self, message):
        # ignore our own messages
        if message.author == self.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

    # called when bot is added to guild
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
