import os
import subprocess
from config import TOKEN_CLOUDFLARE, WORKING_MODE
from log.logging_config import Logger

# Instancia el debug
logger = Logger().get_logger()

def start_cloudflare_tunnel():
    """
    Inicia el túnel de Cloudflare usando el binario portable.
    """

    if WORKING_MODE != 'production':
        logger.info("El bot no está en modo producción, el túnel de Cloudflare no se iniciará.")
        return

    if not os.path.isfile('./cloudflared-linux-amd64'):
        logger.error("El binario portable de Cloudflare no fue encontrado.")
        return
    
    try:
        # Reemplaza 'cloudflared' con la ruta a tu binario portable de Cloudflare
        # y ajusta los parámetros según tus necesidades.

        subprocess.Popen(['./cloudflared-linux-amd64', 'tunnel', '--no-autoupdate', 'run', '--token', TOKEN_CLOUDFLARE])
        logger.info("Túnel de Cloudflare iniciado.")
    except Exception as e:
        logger.error(f"Error al iniciar el túnel de Cloudflare: {e}")