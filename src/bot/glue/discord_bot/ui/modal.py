from discord import ui
import discord
import traceback


class Questionnaire(ui.Modal, title='Setup Project'):
    name = ui.TextInput(label='Name')
    canister_id = ui.TextInput(label='Canister ID',
                               placeholder="aaaaa-aaaaa-aaaaa-aaaa-aaa")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Thanks for your response, {self.name}!', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_tb(error.__traceback__)
