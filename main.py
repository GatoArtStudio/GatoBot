import sys
import socket
import aiohttp
import asyncio
from base.bot import bot
from config import RETRY_DELAY
from log import Logger

# Configuración de logging
logger = Logger().get_logger()

async def check_internet_connection() -> bool:
    target_host = 'https://discord.com'
    async with aiohttp.ClientSession() as session:
        try:
            async with session.head(target_host) as res:
                return res.status == 200
        except aiohttp.ClientError as e:
            logger.error(e)
            return False

async def handle_bot_connection():
    try:
        logger.info("Estableciendo conexion...")
        async with bot:
            await bot.start_bot()
    except KeyboardInterrupt:
        logger.info("Saliendo...")
        await bot.close()
        sys.exit(0)
    except (socket.gaierror, aiohttp.client_exceptions.ClientConnectorError, RuntimeError):
        logger.error("Conexion cerrada por error de red.")
        if await check_internet_connection():
            sys.exit(1)
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        sys.exit(2)

async def wait_and_retry_connection():
    logger.error("Intentando reconectar...")
    await asyncio.sleep(RETRY_DELAY)

async def main():
    while True:
        res = await check_internet_connection()
        if res:
            logger.info("Hay conexion a internet")
            await asyncio.sleep(RETRY_DELAY)
            await handle_bot_connection()
        else:
            await wait_and_retry_connection()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    logger.warning("Deteniendo Bot...")
    sys.exit(0)