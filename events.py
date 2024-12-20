from collections import deque
import datetime
import discord
from types_utils import ColorDiscord
import utils


logging = None

TIMEOUT_SECONDS = 60
SPAM_MESSAGE_COUNT = 2

async def handle_everyone_mention(message: discord.Message):
    if message.author.bot:
        return
    if message.author.guild_permissions.administrator:
        return
    if not message.author.guild_permissions.mention_everyone and '@everyone' in message.content:
        await utils.msg_del(message, logging, ColorDiscord.RED)
        return True
    return False

async def handle_spam_links(message):
    if '[store.steampowered.com' in message.content:
        await message.delete()
        try:
            timeout_expiry = datetime.timedelta(seconds=TIMEOUT_SECONDS)
            await message.author.timeout(timeout_expiry, reason="Aislad@ por 60 segundos, por enviar link engañoso de steam")
            logging.warning(f'El usuario: {message.author.display_name}, ID: {message.author.id} Esta haciendo spam, mensaje: {message.content}')
        except (discord.Forbidden, discord.HTTPException) as e:
            logging.error(f"No tengo permisos para aislar a este usuario o ocurrió un error: {e}")

async def handle_message_logging(message, data_msg):
    if message.author.id not in data_msg:
        data_msg[message.author.id] = deque(maxlen=SPAM_MESSAGE_COUNT + 1)
    if message.content:
        data_msg[message.author.id].append(message.content)
    elif message.attachments:
        for adjunt in message.attachments:
            data_msg[message.author.id].append(adjunt.filename)
    else:
        return

    if len(data_msg[message.author.id]) >= SPAM_MESSAGE_COUNT:
        if all(msg == data_msg[message.author.id][0] for msg in data_msg[message.author.id]):
            await utils.msg_del(message, logging, ColorDiscord.RED)
        else:
            await utils.msg_advertence(message, logging, ColorDiscord.YELLOW)