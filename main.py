import sys

import discord
from discord.ext import commands, voice_recv
from discord import app_commands
import socket
import aiohttp
from aiohttp import client_exceptions
import time
import ping3
from config import TOKEN
import typing
import logging
import view.ui_dc as ui
from utils import utils_tools
import datetime
import random
from utils.types_utils import ColorDiscord
import threading
from utils import music_utils
from log.logging_config import setup_logging
import os
import re
import asyncio
from service.server_proxy import ServerProxy
from service.server_http import ServerHTTP

# Configuración de logging
setup_logging()
logger = logging.getLogger(__name__)

# Clases

intents = discord.Intents.default()
intents.message_content = True  # Habilitar la intención de recibir contenido de mensajes
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix='/', intents=intents)


# sincronizar

@bot.event
async def setup_hook():
    bot.add_view(ui.MenuMusica())

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
    logger.info(f'Conectado como {bot.user.name} ({bot.user.id})')

    # ----------------------------------------------- Variables en otros modulos -----------------------------------------------
    music_utils.bot = bot

    
    # ----------------------------------------------- Sincronizar comandos -----------------------------------------------

    try:
        # Sincroniza los nuevos comandos
        logger.info('Sincronizando comandos...')
        synced = await bot.tree.sync()
        logger.info(f'Sincronizado {len(synced)} comando (s)')
    except Exception as e:
        logger.error(f'Tipo de error {e}')

RETRY_DELAY = 3  # Tiempo de espera entre intentos

# Comando personalizado

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
    modal = ui.UIEMBED()
    await interaction.response.send_modal(modal)

@bot.tree.command(name='t', description='Comandos para el uso de tts (Texto a voz)')
async def t(interaction: discord.Interaction, *, mensaje: str):
    await interaction.response.send_message(f'{interaction.user.mention} A dicho: {mensaje}', tts=True)

@bot.tree.command(name='kill', description='Trolea con /kill al mejor estilo de minecraft')
async def kill(interaction: discord.Interaction, user: discord.Member):
    descripciones = [
        (f'{user.mention} le exploto un globo a los niños y ahora le pegan.', 'https://raw.githubusercontent.com/GatoArtStudios/GatoBot/Gatun/img/Jushiro%20Ukitake%20and%20Sogyo%20no%20Kotowari.gif'),
        (f'la cara de {user.mention} hullendo de {interaction.user.mention} al ver semejante sable.', 'https://raw.githubusercontent.com/GatoArtStudios/GatoBot/Gatun/img/giphy5.gif'),
        (f'{user.mention} se agarro la ñonga a kempachi y ahora unohana lo persigue.', 'https://raw.githubusercontent.com/GatoArtStudios/GatoBot/Gatun/img/giphy5.gif'),
        (f'{user.mention} soy demaciada diva como para que me trates mal perr*s', 'https://raw.githubusercontent.com/GatoArtStudios/GatoBot/Gatun/img/giphy9.gif'),
        (f'{user.mention} dice, ey {interaction.user.mention} como es que tienes ese agujero tan blanco, no seas mamon, enseña esa estrategia bro.', 'https://raw.githubusercontent.com/GatoArtStudios/GatoBot/Gatun/img/giphy11.gif'),
        (f'{user.mention} Esta plenamente enamorado de {interaction.user.mention}, pero es un amor prohibido, ya que {interaction.user.mention} a decidido cazarce con un femboy.', 'https://raw.githubusercontent.com/GatoArtStudios/GatoBot/Gatun/img/giphy13.gif'),
        (f'{user.mention} fue contagiado de l**b por {interaction.user.mention}, ahora somos libre como el viento UwU.', 'https://raw.githubusercontent.com/GatoArtStudios/GatoBot/Gatun/img/giphy8.gif'),
        (f'{user.mention}  ha explotado mientras escapaba de un femboy.', 'https://raw.githubusercontent.com/GatoArtStudios/GatoBot/Gatun/img/iwo6UYIcHBFjlSoEMM.gif'),
        (f'Una VTUBER ha acabado con la vida de {user.mention}.', 'https://raw.githubusercontent.com/GatoArtStudios/GatoBot/Gatun/img/giphy.gif'),
        (f'{user.mention} ha sido asesinado por {interaction.user.mention} con una espada de diamante.', 'https://raw.githubusercontent.com/GatoArtStudios/GatoBot/Gatun/img/giphy2.gif'),
        (f'{user.mention} ha caído en un pozo de lava gracias a {interaction.user.mention}.', 'https://raw.githubusercontent.com/GatoArtStudios/GatoBot/Gatun/img/200.gif'),
        (f'{interaction.user.mention} lanzó a {user.mention} desde una gran altura.', 'https://raw.githubusercontent.com/GatoArtStudios/GatoBot/Gatun/img/B1FAKSmfWqRA4.gif'),
        (f'{user.mention} fue alcanzado por una flecha disparada por {interaction.user.mention}.', 'https://raw.githubusercontent.com/GatoArtStudios/GatoBot/Gatun/img/giphy4.gif'),
        (f'{interaction.user.mention} empujó a {user.mention} a un grupo de creepers.', 'https://raw.githubusercontent.com/GatoArtStudios/GatoBot/Gatun/img/giphy3.gif')
    ]
    descript, url = random.choice(descripciones)
    embed = discord.Embed(title=None, description=descript, color=ColorDiscord.GREEN.value)
    embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)
    embed.set_footer(text=f'Por {interaction.user.display_name}', icon_url=interaction.user.display_avatar.url)
    embed.set_image(url=url)
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
@app_commands.autocomplete(color=utils_tools.color_autocomplete)
@app_commands.describe(color='Color del Embed', title='Tiulo del Embed', description='Descripción del Embed', description_embed='Descripción del Embed', author='Autor del Embed', channel='Canal donde se enviara el Embed')
async def create_embed(interaction: discord.Interaction, channel: discord.TextChannel, color: str, title: typing.Optional[str] = None, description: typing.Optional[str] = None, description_embed: typing.Optional[str] = None, author: typing.Optional[discord.Member] = None):
    color_value = ColorDiscord[color.upper()].value
    description_embed = description_embed.replace('\\n', '\n')
    embed = discord.Embed(
        title=title,
        description=description_embed,
        color=color_value
    )

    if author is None and description is None:
        await channel.send(embed=embed)
        await interaction.response.send_message(f"Mensaje enviado al canal {channel.mention}")
    elif author is None:
        await channel.send(content=description,embed=embed)
        await interaction.response.send_message(f"Mensaje enviado al canal {channel.mention}")
    else:
        if description is None:
            embed.set_author(name=author.display_name, icon_url=author.display_avatar.url)
            await channel.send(embed=embed)
            await interaction.response.send_message(f"Mensaje enviado al canal {channel.mention}")
        else:
            await channel.send(f'{description}\n\nAutor: {author}',embed=embed)
            await interaction.response.send_message(f"Mensaje enviado al canal {channel.mention}")


@bot.tree.command(name='play', description='Escucha musica')
async def play(interaction: discord.Interaction, query: str):
    args = query.split(' ')
    query = " ".join(args)
    try:
        voice_channel = interaction.user.voice.channel
    except:
        await interaction.response.send_message("No estas en un canal de voz", ephemeral=True)
        return
    if music_utils.is_paused:
        music_utils.vc.resume()
        await interaction.followup.send("> La reproducción ha sido reanudada.")
        return
    else:
        await interaction.response.defer(ephemeral=True) # Espera la respuesta del comando
        song = music_utils.search_yt(query)
        print(f'Resultado de la busqueda: {song}')
        if type(song) == bool and not song:
            await interaction.response.send_message("No se pudo descargar la cancion", ephemeral=True)
            return
        # Verificamos si ya se está reproduciendo algo
        if music_utils.is_playing:
            position_in_queue = len(music_utils.music_queue) + 2
            await interaction.followup.send(f"**#{position_in_queue} - '{song['title']}'** agregado a la cola")
        else:
            await interaction.followup.send(f"**'{song['title']}'** agregado a la cola")

        # Añadimos la canción a la cola
        music_utils.music_queue.append([song, voice_channel])

        # Si no hay canciones reproduciéndose, comenzamos la reproducción
        if not music_utils.is_playing:
            await music_utils.play_music(interaction)
            music_ui = ui.MenuMusica()
            await interaction.followup.send(f"**'{song['title']}'** comenzando a reproducirse" ,view=music_ui)


@bot.tree.command(name='menu_music', description='Muestra el menu de musica')
async def menu_music(interaction: discord.Interaction):
    await interaction.response.send_message("Menu de musica", view=ui.MenuMusica())

@bot.tree.command(name='voice_join', description='Ingresa a un canal de voz')
async def voice_join(interaction: discord.Interaction, channel: discord.VoiceChannel):
    await channel.connect()
    await channel.send(f'Conectado al canal de voz {channel.mention}')
    await interaction.response.send_message(f'Conectado al canal de voz {channel.mention}', ephemeral=True)


@bot.tree.command(name='voice_stop', description='Sale de un canal de voz')
async  def voice_stop(interaction: discord.Interaction):
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message(f'Desconectado del canal de voz', ephemeral=True)
    else:
        await interaction.response.send_message(f'No estoy conectado al canal de voz', ephemeral=True)


@bot.tree.command(name='voice_rec', description='Inicia la grabación en canal de voz')
async def voice_rec(interaction: discord.Interaction, channel: discord.VoiceChannel):
    try:
        # Obtenemos la fecha y hora actual la cual se usara para el nombre del archivo
        fchtime = datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S")

        # Definimos la funcion de callback que se encargara de gestionar los datos de entrada de voz
        def callback(user, data: voice_recv.VoiceData):
            logger.info(f'User: {user} Data: {data}')

            # Limpiamos el nombre del usuario de caracteres especiales
            user = re.sub(r'[^a-zA-Z0-9_\-\. ]', '', user.name)

            # Guarda el audio en un archivo dentro de el directorio recordings
            # Si no existe el directorio para guardar las grabaciones, lo crea
            if not os.path.exists('recordings'):
                os.makedirs('recordings')

            # Escribimos los datos en caliente en el archivo
            name_file = f'{user}_{fchtime}.pcm'
            with open(f'recordings/{name_file}', 'ab') as f:
                f.write(data.pcm)

        await interaction.response.send_message(f'Conectado al canal de voz {channel.mention}', ephemeral=True)
        vc = await channel.connect(cls=voice_recv.VoiceRecvClient)
        vc.listen(voice_recv.BasicSink(callback))

    except Exception as e:
        logger.error(f'Error al iniciar la grabación: {e}')
        if not interaction.response.is_done():
            await interaction.response.send_message(
                f'Error al intentar grabar: {e}',
                ephemeral=True
            )
        else:
            await interaction.followup.send(f'Error al intentar grabar: {e}')

# inicia servidor http
def start_server_http():
    '''
    Inicia el servidor http
    '''
    shttp = ServerHTTP()
    shttp.start_server()

# Conecta el bot usando el token del bot
async def check_internet_connection() -> bool:
    """
    Comprueba si hay conexión a Internet.

    Esta función utiliza el módulo ping3 para probarar la conexión a
    `discord.com`. Si la respuesta es `None`, significa que hay conexión.

    Args:
        None

    Returns:
        bool: True si hay conexión a Internet, False en caso contrario.
    """
    target_host: str = 'https://discord.com'
    async with aiohttp.ClientSession() as session:
        try:
            async with session.head(target_host) as res:
                return res.status == 200
        except aiohttp.ClientError as e:
            logger.error(e)
            return False

async def handle_bot_connection():
    """Establece conexión con el bot y maneja posibles errores."""
    try:
        logger.info("Estableciendo conexion...")
        async with bot:
            # cargamos los cogs
            for filename in os.listdir('./event'):
                if filename.endswith('.py'):
                    await bot.load_extension(f'event.{filename[:-3]}')
            
            for filename in os.listdir('./commands'):
                if filename.endswith('.py'):
                    await bot.load_extension(f'commands.{filename[:-3]}')
            
            # Iniciamos servidor http
            servidor_http_thread = threading.Thread(target=start_server_http)
            servidor_http_thread.start()
            
            # Iniciamos el bot
            await bot.start(TOKEN)

    except KeyboardInterrupt:
        logger.info("Saliendo...")
        sys.exit(0)

    except (socket.gaierror, aiohttp.client_exceptions.ClientConnectorError, RuntimeError):
        logger.error("Conexion cerrada por error de red.")
        if await check_internet_connection():
            sys.exit(1)
    
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        sys.exit(2)  # Error genérico para otros problemas no cubiertos previamente

async def wait_and_retry_connection():
    """Espera un tiempo y luego vuelve a intentar la conexión."""
    logger.error("Intentando reconectar...")
    await asyncio.sleep(RETRY_DELAY)

# Ejecución principal del proceso
async def main():
    while True:
        res = await check_internet_connection()
        if res:
            logger.info("Hay conexion a internet")
            await asyncio.sleep(RETRY_DELAY)
            await handle_bot_connection()
        else:
            await wait_and_retry_connection()

asyncio.run(main())

# Link para agregar el bot al servidor
# https://discord.com/oauth2/authorize?client_id=1108545284264431656
# Link para agregar el bot al servidor
