import logging

import discord
import datetime
from discord.ext import commands
from sqlalchemy import event
from sqlalchemy.orm import Session

from core.implements.discord_bot import DiscordBot
from core.logging import Logger
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from config.config import WORKING_MODE_DEV, SERVER_DEV_ID
from database.connection import Database
from models.guild_discord import GuildDiscord

# Instancia el debug
logger: logging.Logger

class Messages(commands.Cog):
    '''
    Maneja los mensajes
    '''

    guild_config: dict[int, GuildDiscord] = {}
    session_database: Session

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.TIMEOUT_SECONDS = 60
        self.model = None
        self.session_database = Database().get_session()
        self.load_guilds()
        event.listen(GuildDiscord, 'after_update', self.load_guilds) # Cuando se actualiza la configuracion de un servidor, se actualiza el diccionario
        event.listen(GuildDiscord, 'after_insert', self.load_guilds)
        event.listen(GuildDiscord, 'after_delete', self.load_guilds)
        logger.warning('Entrenando modelos de Machine Learning...')
        self.train_model_spam()

    def load_guilds(self, *args, **kwargs):

        logger.info('Cargando configuraciones de los servidores...')
        logger.info(f'Recividos argumentos: {args} y {kwargs}')
        try:
            guilds = self.session_database.query(GuildDiscord).all()

            for guild in guilds:
                self.guild_config[guild.guild_id] = guild
        except Exception as e:
            logger.error(f'Error al cargar configuraciones de los servidores: {e}')

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

        if message.guild:
            if WORKING_MODE_DEV and message.guild.id == int(SERVER_DEV_ID):
                await self.handle_is_spam(message=message)
                return


        # Verifica que el autor del mensaje no sea el bot / administrador / o mencionar a @everyone
        if await self.handle_everyone_mention(message=message):
            return
        
        # Verifica si hay spam de una cuenta comprometida
        # Debido a un problema con el modelo LM, el bot detecta el numero 50 como spam
        if message.guild.id in self.guild_config:
            if self.guild_config[message.guild.id].active_antispam:
                await self.handle_is_spam(message=message)
            else:
                logger.warning(f'Antispam desactivado en el servidor: {message.guild.name}')

    async def handle_is_spam(self, message: discord.Message):
        '''
        Verifica si el autor del mensaje esta haciendo spam
        '''
        print(f'Procesando mensaje por el sistema de antispam con IA: {message.content}')
        # No hacemos nada si el autor del mensaje es el bot
        if message.author.bot:
            return
        
        # verificamos si el mensaje tiene contenido de texto
        if message.content == '':
            return
        
        prediction = self.model.predict([message.content])
        if prediction[0] == 'spam':
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
            await message.delete()
            return True
        
        # Retornamos si ninguna de las siguientes condiciones se comple
        return False

    def train_model_spam(self):
        '''
        Entrenamiento del modelo
        '''

        messages = [
                "steam gift 50$ - [steamcommunity.com/gift-card/pay/50](https://)@everyone",
                "Haz clic aquí para reclamar tu premio",
                "Invierte en criptomonedas y hazte rico",
                "Únete a nuestro grupo y obtén recompensas",
                "Hola, ¿cómo estás?",
                "Nos vemos mañana en la reunión",
                "Recuerda enviar el reporte antes del viernes",
                "¡Oferta especial solo por hoy!, escribeme al dm",
                "¡Oferta especial solo por hoy!",
                "Compra seguidores para tu cuenta, escribeme al dm",
                "Compra seguidores para tu cuenta",
                "Llámame cuando puedas",
                "@everyone steam gift 50$ - [steamcommunity.com/gift-card/pay/50](https://)",
                "50$ gift https://steamuconmmunity.com/s/10329209416",
                "50$ steam gift - https://",
                "https://tenor.com/view/",
                "https://x.com/",
                "https://www.instagram.com/",
                "https://www.tiktok.com/",
                "https://www.youtube.com/",
                "https://www.twitch.tv/",
                "https://www.facebook.com/",
            ]
        labels = [
                "spam", "no_spam", "no_spam", "no_spam", "no_spam",
                "no_spam", "no_spam", "spam", "no_spam", "spam", "no_spam", "no_spam", "spam", "spam", "spam", 
                "no_spam", "no_spam", "no_spam", "no_spam", "no_spam", 'no_spam', "no_spam"
            ]
        
        # Convertimos los mensajes a una array 2d
        # messages = np.array(messages).reshape(-1, 1)
        
        
        # Entrenamos el modelo con TF-IDF y Naive Bayes
        self.model = make_pipeline(TfidfVectorizer(), MultinomialNB())
        self.model.fit(messages, labels)


async def setup(bot: DiscordBot):
    """
    Agrega el cog al bot
    """

    global logger
    logger = bot.logger

    await bot.add_cog(Messages(bot))