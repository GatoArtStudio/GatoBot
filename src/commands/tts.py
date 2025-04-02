import logging

import discord
import os
import asyncio
from pathlib import Path
from gtts import gTTS
from discord.ext import commands, tasks
from discord import app_commands

from config.config import TMP_PATH
from core.implements.discord_bot import DiscordBot
from core.logging import Logger

# Instancia el debug
logger: logging.Logger

class MembersUtils(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.dir_tmp = TMP_PATH / 'tts'
        self.dir_tmp.mkdir(parents=True, exist_ok=True) # Crea el directorio si no existe
        self.tts_queue = [] # Cola de mensajes por enviar
        self.is_playing = False # Bandera para saber si esta reproduciendo un mensaje
        
    @commands.Cog.listener()
    async def on_ready(self):
        self.check_empty_channel.start()
    
    def add_to_queue(self, interaction: discord.Interaction, message: str):
        self.tts_queue.append((interaction, message))
        if not self.is_playing:
            self.bot.loop.create_task(self.play_next_in_queue())
        else:
            self.bot.loop.create_task(self.notify_queue(interaction))

    async def notify_queue(self, interaction: discord.Interaction):
        await interaction.followup.send("Tu mensaje ha sido agregado a la cola", ephemeral=True)

    def get_from_queue(self):
        interaction: discord.Interaction = None
        message: str = None
        interaction, message = self.tts_queue.pop(0)
        
        return interaction, message

    @app_commands.command(name='tts', description='Permite que los demas usuarios escuchen lo que escribas')
    async def tts(self, interaction: discord.Interaction, message: str):
        """
        Permite que los demas usuarios escuchen lo que escribas
        """
        
        # Deferir la respuesta
        await interaction.response.defer(ephemeral=True)

        try:

            # Verifica que el usuario este en un canal de voz
            voice_channel = interaction.user.voice.channel if interaction.user.voice else False
            if not voice_channel:
                await interaction.followup.send("Debes estar en un canal de voz para usar este comando", ephemeral=True)
                return

            # Verificar permisos del usuario en el canal de voz
            permissions = voice_channel.permissions_for(interaction.user)
            if not permissions.send_tts_messages:
                await interaction.followup.send("No tienes permisos para usar TTS en este canal de voz.", ephemeral=True)
                return
            
            # Agrega el mensaje a la cola
            self.add_to_queue(interaction, f'{interaction.user.name}, {message}')

        except Exception as e:
            logger.error(f"Error al enviar el mensaje: {e}")
            await interaction.followup.send(f"Error al enviar el mensaje.", ephemeral=True)

    async def play_next_in_queue(self):
        if not self.tts_queue:
            self.is_playing = False
            return
        
        self.is_playing = True
        interaction, message = self.get_from_queue()

        try:
            # Generar el archivo de audio
            tts = gTTS(message, lang='es')
            tts.save(f"{self.dir_tmp}/{interaction.user.id}_tts.mp3")

            # Conectarse al canal de voz si no esta conectado
            voice_client = interaction.guild.voice_client
            if voice_client is None or voice_client.channel != interaction.user.voice.channel:
                if voice_client is not None:
                    await voice_client.disconnect()
                voice_client = await interaction.user.voice.channel.connect()

                # Esperamos un monento para que se conecte
                await asyncio.sleep(1)

            # Reproducir el archivo de audio
            voice_client.play(discord.FFmpegPCMAudio(f"{self.dir_tmp}/{interaction.user.id}_tts.mp3"), after=lambda e: self.bot.loop.create_task(self.on_audio_complete()))

            # Esperar a que termine de reproducir
            while voice_client.is_playing():
                await asyncio.sleep(1)

            # Eliminar el archivo de audio
            os.remove(f"{self.dir_tmp}/{interaction.user.id}_tts.mp3")

            # Enviar un mensaje de confirmacion
            await interaction.followup.send("Mensaje enviado", ephemeral=True)

        except Exception as e:
            logger.error(f"Error al enviar el mensaje: {e}")
            await interaction.followup.send(f"Error al enviar el mensaje.", ephemeral=True)
            self.is_playing = False

    async def on_audio_complete(self):
        # self.is_playing = False
        await self.play_next_in_queue()

    @tasks.loop(seconds=30)
    async def check_empty_channel(self):
        # Interamos todos los servidores
        for guild in self.bot.guilds:
            # Obtenemos el voice client del cada servidor iterado
            voice_client: discord.VoiceClient = guild.voice_client
            # Verificamos si el voice client esta conectado y si el canal de voz tiene un solo miembro
            if voice_client and len(voice_client.channel.members) == 1:
                # Desconectamos al bot del canal
                await voice_client.disconnect()


async def setup(bot: DiscordBot):
    """
    Agrega el cog al bot
    """

    global logger
    logger = bot.logger

    await bot.add_cog(MembersUtils(bot))