import discord
import logging
import random
import time
from discord import ActivityType
from discord.ext import commands, tasks
from log.logging_config import setup_logging

# Instancia el debug
setup_logging()
logger = logging.getLogger(__name__)

class Presence(commands.Cog):
    '''
    Cambia el estado de actividad del bot
    '''
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.presence = self.getRandomActivity()

    @commands.Cog.listener()
    async def on_ready(self):
        '''
        Cambiamos la actividad del bot
        '''

        # Iniciamos el loop de cambio random de estado
        self.changePresence.start()
        logger.info('Loop para estado random, comenzado')

    @tasks.loop(minutes=1.0)
    async def changePresence(self):
        self.presence = self.getRandomActivity()
        await self.bot.change_presence(activity=self.presence)
    
    def getRandomActivity(self):
        '''
        Obtiene un estado aleatorio
        '''
        states = [
            # Estados Jugando
            discord.Game(
                name="Jugando al ajedrez con la CPU"
            ),
            discord.Game(
                name="Explorando mundos desconocidos"
            ),
            discord.Game(
                name="Configurando servidores mágicos"
            ),

            # Estados Escuchando
            discord.Activity(
                type=ActivityType.listening,
                name="Escuchando tus comandos",
                state="desarrollador: https://gatoartstudio.art/redes/"
            ),
            discord.Activity(
                type=ActivityType.listening,
                name="Interpretando sugerencias",
                state="desarrollador: https://gatoartstudio.art/redes/"
            ),
            discord.Activity(
                type=ActivityType.listening,
                name="Spotify: Canción favorita del año",
                state="desarrollador: https://gatoartstudio.art/redes/"
            ),

            # Estados Viendo
            discord.Activity(
                type=ActivityType.watching,
                name="Observando la actividad del servidor",
                state="desarrollador: https://gatoartstudio.art/redes/"
            ),
            discord.Activity(
                type=ActivityType.watching,
                name="Recolectando estadísticas",
                state="desarrollador: https://gatoartstudio.art/redes/"
            ),
            discord.Activity(
                type=ActivityType.watching,
                name="Mirando el flujo de datos",
                state="desarrollador: https://gatoartstudio.art/redes/"
            ),
            discord.Streaming(
                name="GatoArtStudio",
                details="¡Qué increíble!",
                url="https://gatoartstudio.art/redes/"
            ),

            # Estados Compitiendo
            discord.Activity(
                type=ActivityType.competing,
                name="Compitiendo por el bot más útil",
                state="desarrollador: https://gatoartstudio.art/redes/"
            ),
            discord.Activity(
                type=ActivityType.competing,
                name="En una carrera de programación",
                state="desarrollador: https://gatoartstudio.art/redes/"
            ),
            discord.Activity(
                type=ActivityType.competing,
                name="Contra los límites del tiempo de respuesta",
                state="desarrollador: https://gatoartstudio.art/redes/"
            ),
            discord.Activity(
                type=ActivityType.competing,
                name="Protegiendo el servidor contra tus travesuras",
                state="desarrollador: https://gatoartstudio.art/redes/"
            ),
            discord.Streaming(
                name="GatoArtStudio",
                details="¿Quieres salir en esta actividad publicitaria de forma gratuita?, dale a Ver!!",
                url="https://gatoartstudio.art/redes/"
            ),

            # Estados de Streaming
            discord.Streaming(
                name="anamanacass",
                details="AnamanaCass esta haciendo mamadas!",
                url="https://www.twitch.tv/anamanacass"
            ),
            discord.Streaming(
                name="th3voidlive",
                details="Th3VoiDLive cuidando unos gatitos tikitos!",
                url="https://www.twitch.tv/th3voidlive"
            ),
            discord.Streaming(
                name="eriphantomhive",
                details="EriPhantomhive te dice: hola po!",
                url="https://www.twitch.tv/eriphantomhive"
            ),
            discord.Streaming(
                name="alascr29",
                details="Bueno Bueno Bueno Chicos... Leyenda del streming B)",
                url="https://www.twitch.tv/alascr29"
            )
        ]
        
        # Retornamos un estados aleatorio
        return random.choice(states)


async def setup(bot):
    """
    Agrega el cog al bot
    """
    await bot.add_cog(Presence(bot))