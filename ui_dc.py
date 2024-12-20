import discord
from discord.utils import MISSING
import typing
import music_utils

class UIEMBED(discord.ui.Modal, title='Crea Embed'):
    title_input = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label='Titulo - Embed',
        required=False,
        placeholder='Coloca el titulo del Embed'
    )
    color = discord.ui.Select(
        placeholder='Select',
        options=[discord.SelectOption(label='color', value='color')]
    )
    async def on_submit(self, interaction: discord.Integration):
        await interaction.response.send_message(f'Ejecutado, {self.title_input.value}')

class MenuMusica(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(PlayButtonMusic())
        self.add_item(PauseButtonMusic())
        self.add_item(SkipButtonMusic())
        self.add_item(StopButtonMusic())
        self.add_item(QueueButtonMusic())
        self.add_item(ResumeButtonMusic())
        self.add_item(RemoveButtonMusic())

class PlayButtonMusic(discord.ui.Button):
    def __init__(self):
        super().__init__(label='Play', style=discord.ButtonStyle.green, custom_id='play_button_music')

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        try:
            voice_channel = interaction.user.voice.channel
        except:
            await interaction.followup.send("No estas en un canal de voz", ephemeral=True)
            return
        if music_utils.is_paused:
            music_utils.vc.resume()
            await interaction.followup.send("> La reproducción ha sido reanudada.")
            return
        else:
            if len(music_utils.music_queue) > 0:
                await music_utils.play_music(interaction)
            else:
                await interaction.followup.send("No hay canciones en la cola", ephemeral=True)


class PauseButtonMusic(discord.ui.Button):
    def __init__(self):
        super().__init__(label='Pause', style=discord.ButtonStyle.green, custom_id='pause_button_music')

    async def callback(self, interaction: discord.Interaction):
        # Diferir la respuesta para que no expire
        await interaction.response.defer(ephemeral=True)
        if music_utils.is_playing:
            music_utils.is_playing = False
            music_utils.is_paused = True
            music_utils.vc.pause()
            followup_message = 'Musica pausada'
        else:
            music_utils.is_paused = False
            music_utils.is_playing = True
            music_utils.vc.resume()
            followup_message = 'Musica reanudada'

        # Enviar la respuesta de seguimiento
        await interaction.followup.send(followup_message, ephemeral=True)


class SkipButtonMusic(discord.ui.Button):
    def __init__(self):
        super().__init__(label='Skip', style=discord.ButtonStyle.green, custom_id='skip_button_music')

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if music_utils.vc != None and music_utils.vc:
            music_utils.vc.stop()
            # Reproducir la siguiente cancion
            await music_utils.play_music(interaction)
        await interaction.followup.send('Siguiente cancion', ephemeral=True)

class StopButtonMusic(discord.ui.Button):
    def __init__(self):
        super().__init__(label='Stop', style=discord.ButtonStyle.green, custom_id='stop_button_music')

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        music_utils.is_playing = False
        music_utils.is_paused = False
        await music_utils.vc.disconnect()

class QueueButtonMusic(discord.ui.Button):
    def __init__(self):
        super().__init__(label='Queue', style=discord.ButtonStyle.green, custom_id='queue_button_music')

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        retval = ''
        for i in range(0, len(music_utils.music_queue)):
            retval += f"#{i+1} -" + music_utils.music_queue[i][0]['title'] + "\n"

        if retval != '':
            await interaction.followup.send(f"```List:\n{retval}```")
        else:
            await interaction.followup.send("```No hay musica en la cola```")

class ResumeButtonMusic(discord.ui.Button):
    def __init__(self):
        super().__init__(label='Resume', style=discord.ButtonStyle.green, custom_id='resume_button_music')

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if music_utils.is_paused:
            music_utils.is_paused = False
            music_utils.is_playing = True
            music_utils.vc.resume()
            await interaction.followup.send('Musica reanudada', ephemeral=True)

class RemoveButtonMusic(discord.ui.Button):
    def __init__(self):
        super().__init__(label='Remove', style=discord.ButtonStyle.green, custom_id='remove_button_music')

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if len(music_utils.music_queue) == 0:
            await interaction.followup.send('No hay canciones en la cola', ephemeral=True)
            return
        music_utils.music_queue.pop()
        await interaction.followup.send('Ultima cancion eliminada', ephemeral=True)