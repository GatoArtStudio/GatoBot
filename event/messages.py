import discord
import datetime
from discord.ext import commands
from log.logging_config import Logger
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from config import WORKING_MODE, SERVER_DEV_ID

# Instancia el debug
logger = Logger().get_logger()

class Messages(commands.Cog):
    '''
    Maneja los mensajes
    '''
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.TIMEOUT_SECONDS = 60
        self.model = None
        logger.warning('Entrenando modelos de Machine Learning...')
        self.train_model_spam()

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
            if WORKING_MODE == 'dev' and message.guild.id == int(SERVER_DEV_ID):
                await self.handle_is_spam(message=message)
                return


        # Verifica que el autor del mensaje no sea el bot / administrador / o mencionar a @everyone
        if await self.handle_everyone_mention(message=message):
            return
        
        # Verifica si hay spam de una cuenta comprometida
        await self.handle_is_spam(message=message)

    async def handle_is_spam(self, message: discord.Message):
        '''
        Verifica si el autor del mensaje esta haciendo spam
        '''
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
                "50$ steam gift - https://"
            ]
        labels = [
                "spam", "no_spam", "no_spam", "no_spam", "no_spam",
                "no_spam", "no_spam", "spam", "no_spam", "spam", "no_spam", "no_spam", "spam", "spam", "spam"
            ]
        
        # Convertimos los mensajes a una array 2d
        # messages = np.array(messages).reshape(-1, 1)
        
        
        # Entrenamos el modelo con TF-IDF y Naive Bayes
        self.model = make_pipeline(TfidfVectorizer(), MultinomialNB())
        self.model.fit(messages, labels)


async def setup(bot):
    '''
    Agrega el cog al bot
    '''
    await bot.add_cog(Messages(bot))