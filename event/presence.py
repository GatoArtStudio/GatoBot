import discord
import logging
from discord.ext import commands
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
        self.presence = discord.Activity(
            # name = 'tu video en 4🥵',
            name = '🛠️ Bot en mantenimiento 🛠️',
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

    @commands.Cog.listener()
    async def on_ready(self):
        '''
        Cambiamos la actividad del bot
        '''
        await self.bot.change_presence(activity=self.presence)
        logger.info('Actividad del bot cambiada.')

async def setup(bot):
    '''
    Agrega el cog al bot
    '''
    await bot.add_cog(Presence(bot))