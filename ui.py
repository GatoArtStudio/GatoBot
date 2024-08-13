import discord
from discord.utils import MISSING
import typing

class UIEMBED(discord.ui.Modal, title='Crea Embed'):
    title_input = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label='Titulo - Embed',
        required=False,
        placeholder='Coloca el titulo del Embed'
    )
    color = discord.ui.Select(
        placeholder='Select',
        options=[discord.SelectOption(label='color', value='color')]
    )
    async def on_submit(self, interaction: discord.Integration):
        await interaction.response.send_message(f'Ejecutado, {self.title_input.value}')