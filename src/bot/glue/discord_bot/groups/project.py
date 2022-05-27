from discord import app_commands
import discord
from glue.database.database import Database
from glue.discord_bot.groups.button import Button
from glue.discord_bot.groups.select import DropdownView
from glue.discord_bot.groups.modal import Questionnaire
from typing import Literal, Optional

# connection to database
db = Database('database.db')


class Project(app_commands.Group):
    """Manage general commands"""

    def __init__(self, client: discord.Client):
        super().__init__()
        self.client = client

    @app_commands.command()
    async def add(self, interaction: discord.Interaction, name: str, canister_id: str, standard: Literal['ext', 'dip721'], min: int = 1, max: Optional[int] = None):
        """Set up an NFT project"""
        try:
            db.insert_project(canister_id, standard, min, max, name)
            await interaction.response.send_message(f'Added project {name} to database')
        except Exception as e:
            await interaction.response.send_message(f'Error: {e}')

    @app_commands.command()
    async def list(self, interaction: discord.Interaction):
        """List all projects"""
        projects = db.fetch_projects()
        await interaction.response.send_message(f'{projects}')

    @app_commands.command()
    async def modal(self, interaction: discord.Interaction):
        """open modal"""
        await interaction.response.send_modal(Questionnaire())

    @app_commands.command()
    async def button(self, interaction: discord.Interaction):
        """open select"""
        await interaction.response.send_message("moin", view=Button())

    @app_commands.command()
    async def select(self, interaction: discord.Interaction):
        """open select"""
        await interaction.response.send_message("moin", view=DropdownView())

    @app_commands.command()
    async def remove(self, interaction: discord.Interaction, canister_id: str):
        """Remove a project"""
        try:
            db.remove_project(canister_id)
            await interaction.response.send_message(f'Removed project {canister_id} from database')
        except Exception as e:
            await interaction.response.send_message(f'Error: {e}')
