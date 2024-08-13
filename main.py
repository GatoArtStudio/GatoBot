import discord
from discord.ext import commands
from discord import app_commands
import socket
import aiohttp
from aiohttp import client_exceptions
import time
import ping3
from config import TOKEN
import typing
import logging
import ui
import utils
import datetime
import random
import asyncio
from types_utils import ColorDiscord
# import api_sql

logging.basicConfig(
    filename='app_discord.log',
    level=logging.DEBUG,
    encoding='utf-8',
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Clases

intents = discord.Intents.default()
intents.message_content = True  # Habilitar la intención de recibir contenido de mensajes
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix='/', intents=intents)
# Evento de inicio
@bot.event
async def on_ready() -> None:
    """Evento de inicio, se activa cuando el bot se conecta a un servidor.

    Imprime en la consola el nombre del bot y su ID, y tambien actualiza
    la presencia del bot con un texto y un emoji personalizados.

    Verifica si se han sincronizado comandos y si hay un error, imprime en la
    consola el tipo de error.

    Args:
        None
    """
    logging.info(f'Conectado como {bot.user.name} ({bot.user.id})')
    # custom_emoji = discord.PartialEmoji(name='😎', animated=False)
    # presence = discord.CustomActivity(
    #         name='😎 ¡Estoy programando! | Bot de Discord en beta y desarrollo | Desarrollador: @GatoArtStudio',
    #     emoji=custom_emoji
    # )

    presence = discord.Activity(
        name = 'tu video en 4🥵',
        url = 'https://linktr.ee/gatoartstudio',
        type = discord.ActivityType.watching,
        state = 'Bot de Discord en beta y en desarrollo, actualmente en 4🥵',
        details = 'Bot',
        platform = 'Discord',
        assets = {
            'large_image': 'logo_fondo_circular',
            'large_text': 'GatoArtStudio',
        },
        buttons = ['/kill', '/t', '/create_embed', '/purge']
    )


    try:
        synced = await bot.tree.sync()
        logging.info(f'synced {len(synced)} commands (s)')
    except Exception as e:
        logging.error(f'Tipo de error {e}')
    await bot.change_presence(activity=presence)

data_msg = {}

# Evento de mensaje
@bot.event
async def on_message(message: discord.Message):
    """Evento de mensaje, se activa cuando se recibe un mensaje en un canal de texto.

    Verifica si el mensaje no es de un bot y si el autor no tiene permisos de administrador.
    Verifica si el mensaje contiene @everyone y si el autor no tiene permiso para mencionar a @everyone, elimina el mensaje de spam.
    Agrega el mensaje o nombre de adjunto a data_msg.
    Si ya tiene 2 mensajes registrados, verifica si el ultimo mensaje es igual al semi-ultimo mensaje o al tercer-avo mensaje ultimo y elimina el mensaje de spam o manda advertencia.


    Args:
        message (discord.Message): El mensaje que se ha recibido.
    """
    # Verifica si el autor del mensaje es un bot
    if message.author.bot:
        return

    # Verifica si el autor del mensaje tiene permisos de administrador
    if message.author.guild_permissions.administrator:
        return

    # Verifica si el mensaje contiene @everyone y si el autor no tiene permiso para mencionar a @everyone
    if not message.author.guild_permissions.mention_everyone and '@everyone' in message.content:
        await utils.msg_del(message, logging, ColorDiscord.RED)
        return

    # Agrega el mensaje o nombre de adjunto a data_msg
    if message.content:
        data_msg[message.author.id].append(message.content)
    elif message.attachments:
        for adjunt in message.attachments:
            data_msg[message.author.id].append(adjunt.filename)
    else:
        return

    # Verifica si ya tiene 2 mensajes registrados
    if len(data_msg[message.author.id]) >= 2:
        # Verifica si el ultimo mensaje es igual al semi-ultimo mensaje
        if data_msg[message.author.id][-1] == data_msg[message.author.id][-2]:
            # Verifica si el ultimo mensaje es igual al tercer-avo mensaje ultimo
            if len(data_msg[message.author.id]) >= 3 and data_msg[message.author.id][-1] == data_msg[message.author.id][-3]:
                await utils.msg_del(message, logging, ColorDiscord.RED)
            else:
                await utils.msg_advertence(message, logging, ColorDiscord.YELLOW)

# Comando personalizado
@bot.tree.command(name='purge', description='Elimina los mensajes de un usuario en las ultimas horas.')
@commands.has_permissions(administrator=True)
async def purge_user(interaction: discord.Interaction, user: discord.Member, horas: typing.Literal[7, 24, 48, 72] = 24) -> None:
    """Elimina los mensajes de un usuario en las ultimas horas.

    Args:
        interaction (discord.Interaction): La interaccion que se realiz  este comando.
        user (discord.Member): El usuario cuyos mensajes se van a eliminar.
        horas (int, optional): El numero de horas que se considerar  n recientes. Defaults to 24.

    Returns:
        None
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    time_limit = now - datetime.timedelta(hours=horas)

    def is_recent_and_from_user(message: discord.Message) -> bool:
        """Verifica si un mensaje es reciente y lo hizo el usuario especificado.

        Args:
            message (discord.Message): El mensaje a verificar.

        Returns:
            bool: True si es reciente y lo hizo el usuario especificado, False en caso contrario.
        """
        return message.author == user and message.created_at >= time_limit

    deleted_messages = await interaction.channel.purge(limit=1000, check=is_recent_and_from_user)
    await interaction.response.send_message(
        f'Se han eliminado {len(deleted_messages)} mensajes de {user.display_name} de las ultimas {horas} horas.',
        ephemeral=True
    )

@bot.tree.command(name='saludo', description='Este comando te saluda UwU')
async def saludo(interaction: discord.Interaction):
    """Este comando responde a una saludo personalizado a cada usuario.

    Args:
        interaction (discord.Interaction): La interaccion que se realiz  este comando.
    """
    await interaction.response.send_message(
        f'Hola {interaction.user.mention} Espero este muy bien',
        ephemeral=True
    )

@bot.tree.command(name='test', description='Este comando es un test de la interfaz de usuario de discord.py')
async def test(interaction: discord.Interaction):
    """Este comando es un test de la interfaz de usuario de discord.py

    Este comando envia un modal con un formulario simple que contiene un campo de texto y un boton de submit.
    Cuando se enva el formulario se muestra un mensaje que indica que se ha ejecutado el formulario.

    Args:
        interaction (discord.Interaction): La interaccion que se realiza este comando.
    """
    ui = ui.UIEMBED()
    await interaction.response.send_modal(ui)

@bot.tree.command(name='t', description='Comandos para el uso de tts (Texto a voz)')
async def t(interaction: discord.Interaction, *, mensaje: str):
    await interaction.response.send_message(f'{interaction.user.mention} A dicho: {mensaje}', tts=True)

@bot.tree.command(name='kill', description='Trolea con /kill al mejor estilo de minecraft')
async def kill(interaction: discord.Interaction, user: discord.Member):
    descripciones = [
        f'{user.mention} se ha impactado fuerte contra un cactus mientras luchaba con un zombi.',
        f'{user.mention}  ha explotado mientras escapaba de un femboy.',
        f'Una VTUBER ha acabado con la vida de {user.mention}.',
        f'{user.mention} ha sido asesinado por {interaction.user.mention} con una espada de diamante.',
        f'{user.mention} ha caído en un pozo de lava gracias a {interaction.user.mention}.',
        f'{interaction.user.mention} lanzó a {user.mention} desde una gran altura.',
        f'{user.mention} fue alcanzado por una flecha disparada por {interaction.user.mention}.',
        f'{interaction.user.mention} empujó a {user.mention} a un grupo de creepers.'
    ]
    embed = discord.Embed(title=f'{interaction.user.display_name} le dio Kill a {user.display_name}', description=random.choice(descripciones), color=0xff0000)
    await interaction.response.send_message(f'Troleando a {user.mention}', ephemeral=True)
    await interaction.channel.send(embed=embed, content=f'{user.mention}')

@bot.tree.command(name='killuser', description='Aisla por 60 segundos a un usuario al estilo minecraft')
@commands.has_permissions(ban_members=True)
async def killuser(interaction: discord.Interaction, user: discord.Member):
    try:
        # Aisla al usuario
        timeout_expiry = datetime.timedelta(seconds=60)
        await user.timeout(timeout_expiry, reason="Aislad@ por 60 segundos por uso de /killuser")
        # Response del comando
        await interaction.response.send_message(f'{user.mention} ha sido aislad@ por 60 segundos', ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("No tengo permisos para aislar a este usuario.", ephemeral=True)
    except discord.HTTPException as e:
        await interaction.response.send_message(f"Ocurrió un error al intentar aislar al usuario: {user.mention}, error: {e}", ephemeral=True)


@bot.tree.command(name='create_embed', description='Comando para crear Embed')
@commands.has_permissions(administrator=True)
@app_commands.autocomplete(color=utils.color_autocomplete)
@app_commands.describe(color='Color del Embed', title='Tiulo del Embed', description='Descripción del Embed', description_embed='Descripción del Embed', author='Autor del Embed', channel='Canal donde se enviara el Embed')
async def create_embed(interaction: discord.Interaction, channel: discord.TextChannel, color: str, title: typing.Optional[str] = None, description: typing.Optional[str] = None, description_embed: typing.Optional[str] = None, author: typing.Optional[discord.Member] = None):
    color_value = ColorDiscord[color.upper()].value
    embed = discord.Embed(
        title=title,
        description=description_embed,
        color=color_value
    )

    if author is None and description is None:
        await channel.send(embed=embed)
        await interaction.response.send_message(f"Mensaje enviado al canal {channel.mention}")
    elif author is None:
        await channel.send(f'{description}\n',embed=embed)
        await interaction.response.send_message(f"Mensaje enviado al canal {channel.mention}")
    else:
        await channel.send(f'{description}\n\nAutor: {author}',embed=embed)
        await interaction.response.send_message(f"Mensaje enviado al canal {channel.mention}")

# Conecta el bot usando el token del bot
def check_internet_connection() -> bool:
    """
    Comprueba si hay conexión a Internet.

    Esta función utiliza el módulo ping3 para probarar la conexión a
    `discord.com`. Si la respuesta es `None`, significa que hay conexión.

    Args:
        None

    Returns:
        bool: True si hay conexión a Internet, False en caso contrario.
    """
    target_host: str = 'discord.com'
    response: typing.Optional[ping3.PingResult] = ping3.ping(target_host)
    return response is not None

# Ejemplo de uso
while True:
    if check_internet_connection():
        logging.info("Hay conexión a Internet")
        time.sleep(3)
        # Aquí puedes intentar la conexión del bot
        try:
            logging.info("Estableciendo conexion...")
            bot.run(TOKEN)
            time.sleep(3)
        except (socket.gaierror, aiohttp.client_exceptions.ClientConnectorError, RuntimeError):
            logging.error("Conexion cerrada por error de red.")
    else:
        logging.error("No hay conexión a Internet. Intentando reconectar...")
        # Aquí puedes repetir el proceso de verificación de conexión después de un tiempo determinado
        time.sleep(3)
        continue

# https://discord.com/api/oauth2/authorize?client_id=1108545284264431656&permissions=8&scope=applications.commands%20bot
'''
static void UpdatePresence()
{
    DiscordRichPresence discordPresence;
    memset(&discordPresence, 0, sizeof(discordPresence));
    discordPresence.state = "En Desarrollo";
    discordPresence.details = "Bot en version beta y en desarrollo.";
    discordPresence.startTimestamp = 1507665886;
    discordPresence.endTimestamp = 1507665886;
    discordPresence.largeImageKey = "logo_fondo_cubico";
    discordPresence.largeImageText = "Numbani";
    discordPresence.smallImageKey = "logo_fondo_circular";
    discordPresence.smallImageText = "Rogue - Level 100";
    discordPresence.partyId = "ae488379-351d-4a4f-ad32-2b9b01c91657";
    discordPresence.partySize = 1;
    discordPresence.partyMax = 5;
    discordPresence.joinSecret = "MTI4NzM0OjFpMmhuZToxMjMxMjM= ";
    Discord_UpdatePresence(&discordPresence);
}
'''
