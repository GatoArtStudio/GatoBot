import discord
from src.helpers.colors import ColorDiscord
from src.log import Logger

# Instancia el debug
logger = Logger().get_logger()

async def color_autocomplete(interaction: discord.Interaction, current: str):
    color_names = [color.name.lower() for color in ColorDiscord]
    return [
        discord.app_commands.Choice(name=color_name, value=color_name)
        for color_name in color_names if current.lower() in color_name
    ][:25]

async def msg_del(message: discord.Message, colors: ColorDiscord):
    '''
    Elimina el mensaje del autor, guarda registro y envia mensaje de notificacion del mensaje eliminado
    '''
    await message.delete()
    logger.warning(f'El usuario: {message.author.display_name}, ID: {message.author.id} Esta haciendo spam, mensaje: {message.content}')
    await message.channel.send(f'{message.author.mention}',embed=discord.Embed(title='Spam', description=f'Mensaje eliminado por spam, {message.author.mention}', color=colors.value))

async def msg_advertence(message: discord.Message, colors: ColorDiscord):
    '''
    Guarda registo y envia mensaje de advertencia al autor del mensaje.
    '''
    logger.warning(f'El usuario: {message.author.display_name}, ID: {message.author.id} se le dio advertencia de spam, mensaje: {message.content}')
    await message.channel.send(f'{message.author.mention}',embed=discord.Embed(title='Advertencia', description=f'Evita hacer spam, puede ser sancionado, {message.author.mention}', color=colors.value))