import logging
import random
import os
import re
import discord
import datetime

from config.config import TMP_PATH
from core.implements.discord_bot import DiscordBot
from view import ui_dc as ui
from helpers import music_utils
from discord import app_commands
from helpers.types_utils import ColorDiscord
from discord.ext import commands, voice_recv
from discord.app_commands.checks import has_permissions

# Configuración de logging
logger: logging.Logger

class OtherCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.path_voice_recordings = TMP_PATH / 'recordings'


    @app_commands.command(name='saludo', description='Este comando te saluda UwU')
    async def saludo(self, interaction: discord.Interaction):
        """Este comando responde a una saludo personalizado a cada usuario.

        Args:
            interaction (discord.Interaction): La interaccion que se realiz  este comando.
        """
        await interaction.response.send_message(
            f'Hola {interaction.user.mention} Espero este muy bien',
            ephemeral=True
        )

    @app_commands.command(name='test', description='Este comando es un test de la interfaz de usuario de discord.py')
    async def test(self, interaction: discord.Interaction):
        """Este comando es un test de la interfaz de usuario de discord.py

        Este comando envia un modal con un formulario simple que contiene un campo de texto y un boton de submit.
        Cuando se enva el formulario se muestra un mensaje que indica que se ha ejecutado el formulario.

        Args:
            interaction (discord.Interaction): La interaccion que se realiza este comando.
        """
        modal = ui.UIEMBED()
        await interaction.response.send_modal(modal)

    @app_commands.command(name='t', description='Comandos para el uso de tts (Texto a voz)')
    async def t(self, interaction: discord.Interaction, *, mensaje: str):
        await interaction.response.send_message(f'{interaction.user.mention} A dicho: {mensaje}', tts=True)

    @app_commands.command(name='kill', description='Trolea con /kill al mejor estilo de minecraft')
    async def kill(self, interaction: discord.Interaction, user: discord.Member):
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

    @app_commands.command(name='killuser', description='Aisla por 60 segundos a un usuario al estilo minecraft')
    @has_permissions(ban_members=True)
    async def killuser(self, interaction: discord.Interaction, user: discord.Member):
        # Compruba si el usuario tiene permisos de administracion
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("No tienes permisos para usar este comando.", ephemeral=True)
            return
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

    @app_commands.command(name='play', description='Escucha musica')
    async def play(self, interaction: discord.Interaction, query: str):
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


    @app_commands.command(name='menu_music', description='Muestra el menu de musica')
    async def menu_music(self, interaction: discord.Interaction):
        await interaction.response.send_message("Menu de musica", view=ui.MenuMusica())

    @app_commands.command(name='voice_join', description='Ingresa a un canal de voz')
    async def voice_join(self, interaction: discord.Interaction, channel: discord.VoiceChannel):
        await channel.connect()
        await channel.send(f'Conectado al canal de voz {channel.mention}')
        await interaction.response.send_message(f'Conectado al canal de voz {channel.mention}', ephemeral=True)


    @app_commands.command(name='voice_stop', description='Sale de un canal de voz')
    @has_permissions(administrator=True)
    async  def voice_stop(self, interaction: discord.Interaction):
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.disconnect()
            await interaction.response.send_message(f'Desconectado del canal de voz', ephemeral=True)
        else:
            await interaction.response.send_message(f'No estoy conectado al canal de voz', ephemeral=True)


    @app_commands.command(name='voice_rec', description='Inicia la grabación en canal de voz')
    @has_permissions(administrator=True)
    async def voice_rec(self, interaction: discord.Interaction, channel: discord.VoiceChannel):
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
                self.path_voice_recordings.mkdir(exist_ok=True, parents=True)

                # Escribimos los datos en caliente en el archivo
                name_file = f'{user}_{fchtime}.pcm'
                with open(f'{self.path_voice_recordings}/{name_file}', 'ab') as f:
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


async def setup(bot: DiscordBot):
    """
    Agrega el cog al bot
    """

    global logger
    logger = bot.logger

    await bot.add_cog(OtherCommands(bot))