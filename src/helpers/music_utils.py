from typing import Optional

import discord
from discord.ext import commands
from yt_dlp import YoutubeDL
import asyncio

from config.config import BIN_PATH

is_playing = False
is_paused = False
bot: Optional[commands.Bot] = None

music_queue = []
YDL_OPTIONS = {'format': 'bestaudio/best'}
FFMPEG_OPTIONS = {'options': '-vn',
                  'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
                  }
check_path_ffmpeg = BIN_PATH / 'ffmpeg'
check_path_ffmpeg.mkdir(parents=True, exist_ok=True)
ffmpeg_path: str = str(BIN_PATH / 'ffmpeg' / 'bin' / 'ffmpeg')

vc = None
ytdl = YoutubeDL(YDL_OPTIONS)


def search_yt(item):
    if item.startswith("https://"):
        # Si es un enlace de YouTube, extraemos la información directamente
        title = ytdl.extract_info(item, download=False)["title"]
        return {'source': item, 'title': title}
    else:
        # Utilizamos yt_dlp para buscar y obtener el enlace
        query = f"ytsearch:{item}"  # Formato de búsqueda para yt_dlp
        search_result = ytdl.extract_info(query, download=False)["entries"]
        if len(search_result) == 0:
            return None  # No se encontraron resultados
        video = search_result[0]  # Obtenemos el primer resultado
        return {'source': video['url'], 'title': video['title']}

async def play_next():
    global vc, is_playing
    if len(music_queue) > 0:
        is_playing = True

        #get the first url
        m_url = music_queue[0][0]['source']

        #remove the first element as you are currently playing it
        music_queue.pop(0)
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(m_url, download=False))
        song = data['url']
        vc.play(discord.FFmpegPCMAudio(song, executable= ffmpeg_path, **FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(play_next(), vc.loop))
    else:
        is_playing = False

async def play_music(ctx: discord.Interaction):
    global vc, is_playing
    if len(music_queue) > 0:
        is_playing = True

        m_url = music_queue[0][0]['source']
        #try to connect to voice channel if you are not already connected
        if vc is None or not vc.is_connected():
            try:
                vc = await music_queue[0][1].connect()

                #in case we fail to connect
                if vc == None:
                    await ctx.followup.send("```No se pudo conectar al canal de voz```")
                    return
            except discord.errors.ClientException:
                await ctx.followup.send("```Ya estoy en un canal de voz```")
        else:
            await vc.move_to(music_queue[0][1])
        #remove the first element as you are currently playing it
        music_queue.pop(0)
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(m_url, download=False))
        song = data['url']
        vc.play(discord.FFmpegPCMAudio(song, executable= ffmpeg_path, **FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(play_next(), vc.loop))

    else:
        is_playing = False