from discord import app_commands
import discord
from glue.database.database import Database
from glue.discord_bot.ui.button import Button
from glue.discord_bot.ui.select import DropdownView
from glue.discord_bot.ui.modal import Questionnaire
from typing import Literal, Optional
from glue.database.database import GlueGuild

# connection to database
db = Database()


class Project(app_commands.Group):
    """Manage general commands"""

    def __init__(self, client: discord.Client):
        super().__init__()
        self.client = client

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.default_permissions()
    async def add(self, interaction: discord.Interaction, name: str, canister_id: str, standard: Literal['ext', 'dip721'], min: int = 1, max: Optional[int] = None):
        """Set up an NFT project"""
        try:
            if interaction.guild_id:
                document: GlueGuild = {
                    "server_id": interaction.guild_id,
                    "canisters": [
                        {
                            "canister_id": canister_id,
                            "standard": standard,
                            "min": min,
                            "max": max,
                            "name": name,
                            "users": []
                        }
                    ]

                }
                db.insert(document)
                await interaction.response.send_message(f'Added project {name} to database')
        except Exception as e:
            await interaction.response.send_message(f'Error: {e}')

    @app_commands.command()
    async def list(self, interaction: discord.Interaction):
        """List all projects"""
        projects = db.find({})
        if not projects:
            await interaction.response.send_message('No projects found')
        for project in projects:
            await interaction.response.send_message(f'{project}')

    @app_commands.command()
    async def modal(self, interaction: discord.Interaction):
        """open modal"""
        await interaction.response.send_modal(Questionnaire())

    @app_commands.command()
    async def button(self, interaction: discord.Interaction):
        """open button"""
        await interaction.response.send_message("moin", view=Button())

    @app_commands.command()
    async def select(self, interaction: discord.Interaction):
        """open select"""
        await interaction.response.send_message("moin", view=DropdownView())

    @app_commands.command()
    async def remove(self, interaction: discord.Interaction, canister_id: str):
        """Remove a project"""
        try:
            result = db.delete_canister(interaction.guild_id, canister_id)
            await interaction.response.send_message(f'Removed project {canister_id} from database. {result}')
        except Exception as e:
            await interaction.response.send_message(f'Error: {e}')
