import discord
import datetime
import utils
from discord.ext import commands
from types_utils import ColorDiscord
import logging
from logging_config import setup_logging

# Instancia el debug
setup_logging()
logger = logging.getLogger(__name__)

class Messages(commands.Cog):
    '''
    Maneja los mensajes
    '''
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.TIMEOUT_SECONDS = 60

    @commands.Cog.listener()
    async def on_ready(self):
        '''
        Modulo cargado
        '''
        logger.info('Modulo que maneja los mensajes cargado.')

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        '''
        Evento de mensaje, se activa cuando se recibe un mensaje en un canal de texto.

        Verifica si el mensaje no es de un bot y si el autor no tiene permisos de administrador.
        Verifica si el mensaje contiene @everyone y si el autor no tiene permiso para mencionar a @everyone, elimina el mensaje de spam.
        Agrega el mensaje o nombre de adjunto a data_msg.
        Si ya tiene 2 mensajes registrados, verifica si el ultimo mensaje es igual al semi-ultimo mensaje o al tercer-avo mensaje ultimo y elimina el mensaje de spam o manda advertencia.


        Args:
            message (discord.Message): El mensaje que se ha recibido.
        '''

        # Verifica que el autor del mensaje no sea el bot
        if await self.handle_everyone_mention(message=message):
            return
        
        await self.handle_spam_links(message=message)
    
    async def handle_everyone_mention(self, message: discord.Message):
        '''
        Verifica si el autor del mensaje comble las siguientes condiciones
        '''
        # Verificamos si el autor del mensaje es el bot
        if message.author.bot:
            return True
        
        # Verificamos si el autor del mensaje tiene permisos de administracion, si es asi, queda excluido de las reglas de bloqueo
        if message.author.guild_permissions.administrator:
            return True
        
        # Verificamos si el usuario que envia el mensaje, intenta mensionar a todos los usuarios del servidor y si tiene permiso para el mismo
        if not message.author.guild_permissions.mention_everyone and '@everyone' in message.content:
            # Eliminamos el mensaje no autorizado
            await utils.msg_del(message, logging, ColorDiscord.RED)
            return True
        
        # Retornamos si ninguna de las siguientes condiciones se comple
        return False

    async def handle_spam_links(self, message: discord.Message):
        '''
        Verifica si hay spam de una cuenta comprometida
        '''

        # Verificamos si el mensaje incluye este contenido que es usual en cuantas comprometidas
        if '[steamcommunity.com/' in message.content:
            # Eliminamos el mensaje de la cuenta comprometida
            await message.delete()

            try:
                # Establecemos un timestap para el timeout
                timeout_expiry = datetime.timedelta(
                    seconds=self.TIMEOUT_SECONDS
                )

                # Aplicamos el respectivo TimeOut al usuario comprometido
                await message.author.timeout(
                    timeout_expiry,
                    reason="Aislado por 60 segundos, por enviar link engañoso de steam"
                )

                # Mostramos en el debug un warn sobre la cuenta comprometida
                logger.warning(
                    f'El usuario: {message.author.display_name}, ID: {message.author.id} Esta haciendo spam, mensaje: {message.content}'
                )

            # Si hay un error durante la sancion al usuario
            except (discord.Forbidden, discord.HTTPException) as e:

                # Notificamos que hubo un error a la consola
                logger.error(f"No tengo permisos para aislar a este usuario o ocurrió un error: {e}")

async def setup(bot):
    '''
    Agrega el cog al bot
    '''
    await bot.add_cog(Messages(bot))