from discord import app_commands
from discord.ext import commands
import discord


class Project(app_commands.Group):
    """Manage general commands"""

    def __init__(self, client: discord.Client):
        super().__init__()
        self.client = client

    @app_commands.command()
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message('Hello')

    @app_commands.command()
    async def version(self, interaction: discord.Interaction):
        """tells you what version of the bot software is running."""
        await interaction.response.send_message('This is an untested test version')
