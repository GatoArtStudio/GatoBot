import discord
import logging
import random
from discord import ActivityType
from discord.ext import commands, tasks
from logging_config import setup_logging

# Instancia el debug
setup_logging()
logger = logging.getLogger(__name__)

class Presence(commands.Cog):
    '''
    Cambia el estado de actividad del bot
    '''
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.presence = self.getStatusRandom()

    @commands.Cog.listener()
    async def on_ready(self):
        '''
        Cambiamos la actividad del bot
        '''
        # Cambiamos el estado del bot
        await self.bot.change_presence(activity=discord.Activity(type=self.presence[1], name=self.presence[0]))
        logger.info('Actividad del bot cambiada.')

        # Iniciamos el loop de cambio random de estado
        self.changePresence.start()
        logger.info('Loop para estado random, comenzado')

    @tasks.loop(minutes=1.0)
    async def changePresence(self):
        self.presence = self.getStatusRandom()
        await self.bot.change_presence(activity=discord.Activity(type=self.presence[1], name=self.presence[0]))
    
    def getStatusRandom(self):
        '''
        Obtiene un estado aleatorio
        '''
        states = [
            # Estados Jugando
            ("Jugando al ajedrez con la CPU", ActivityType.playing),
            ("Explorando mundos desconocidos", ActivityType.playing),
            ("Configurando servidores mágicos", ActivityType.playing),

            # Estados Escuchando
            ("Escuchando tus comandos", ActivityType.listening),
            ("Interpretando sugerencias", ActivityType.listening),
            ("Spotify: Canción favorita del año", ActivityType.listening),

            # Estados Viendo
            ("Observando la actividad del servidor", ActivityType.watching),
            ("Recolectando estadísticas", ActivityType.watching),
            ("Mirando el flujo de datos", ActivityType.watching),
            ("¡Qué increíble! Míralo tú mismo en: https://gatoartstudios.github.io/redes", ActivityType.watching),

            # Estados Compitiendo
            ("Compitiendo por el bot más útil", ActivityType.competing),
            ("En una carrera de programación", ActivityType.competing),
            ("Contra los límites del tiempo de respuesta", ActivityType.competing),
            ("Protegiendo el servidor contra tus travesuras", ActivityType.competing),
            ("¿Quieres salir en esta actividad publicitaria de forma gratuita? Escríbele a @GatoArtStudio.", ActivityType.competing),

            # Estados de Streaming
            ("AnamanaCass esta haciendo mamadas! | twitch: anamanacass", ActivityType.streaming),
            ("Th3VoiDLive cuidando unos gatitos tikitos! | twitch: th3voidlive", ActivityType.streaming),
            ("EriPhantomhive te dice: hola po! | twitch: eriphantomhive", ActivityType.streaming),
            ("Bueno Bueno Bueno Chicos... Leyenda del streming B) | twitch: alascr29", ActivityType.streaming)
        ]
        
        # Retornamos un estados aleatorio
        return random.choice(states)


async def setup(bot):
    '''
    Agrega el cog al bot
    '''
    await bot.add_cog(Presence(bot))