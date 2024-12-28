from collections import deque, Counter
import datetime
import discord
from types_utils import ColorDiscord
import utils


logging = None

TIMEOUT_SECONDS = 60
SPAM_MESSAGE_COUNT = 4

async def handle_everyone_mention(message: discord.Message):
    if message.author.bot:
        return True
    if message.author.guild_permissions.administrator:
        return True
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
    return True
    if message.author.id not in data_msg:
        data_msg[message.author.id] = deque(maxlen=SPAM_MESSAGE_COUNT + 1)

    if message.content:
        # Agregamos contenido del mensaje textual
        data_msg[message.author.id].append(message.content)
    elif message.attachments:
        # Agregamos nombres de los archivos adjuntos (attachments)
        for adjunt in message.attachments:
            data_msg[message.author.id].append(adjunt.filename)
    else:
        return  # Si no hay contenido ni attachments, no hacemos nada y salimos

    # Comprobar si hay al menos SPAM_MESSAGE_COUNT mensajes para analizar
    if len(data_msg[message.author.id]) >= SPAM_MESSAGE_COUNT:
        # Obtener los mensajes recientes desde `data_msg`
        messages = list(data_msg[message.author.id])

        # Indicador de spam basado en si los mensajes son demasiado similares
        if is_spam(messages):
            # Mensajes son spam y se elimina el mensaje del usuario
            await utils.msg_del(message, logging, ColorDiscord.RED)
        else:
            # Mensajes no son spam, pero damos advertencia
            await utils.msg_advertence(message, logging, ColorDiscord.YELLOW)


def is_spam(messages):
    """
    Verifica si los mensajes son spam. Consideramos spam si los mensajes tienen contenido repetitivo o casi idéntico.
    """
    # Convertir todos los mensajes a "tokens" para la comparación
    clean_messages = [msg.strip().lower() for msg in messages]

    # Usamos un contador para ver si hay demasiados duplicados
    freq = Counter(clean_messages)
    most_common_count = freq.most_common(1)[0][1]  # Número de repeticiones del mensaje más común

    # Lógica para considerar spam:
    # - Si el mensaje más frecuente representa más del 80% de los mensajes totales
    # - Si existe poca diversidad en los mensajes
    if most_common_count / len(clean_messages) > 0.8 or len(freq) <= 2:
        return True  # Consideramos que es spam

    return False  # No es spam
