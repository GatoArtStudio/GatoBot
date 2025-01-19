import logging
import colorlog


def setup_logging():
    '''
    Maneja el debug
    '''

    # Define el formato de los logs
    log_format = (
        '%(asctime)s - %(log_color)s%(levelname)s%(reset)s - %(message)s'
    )

    # Configura el color para cada nivel
    log_colors = {
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }


    # Configura el handler de consola con colores
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(colorlog.ColoredFormatter(
        log_format, datefmt='%Y-%m-%d %H:%M:%S', log_colors=log_colors
    ))

    # Configura el handler de archivo sin colores
    file_handler = logging.FileHandler('app_discord.log', encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
    ))

    # Configura el logger raíz
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[console_handler, file_handler]
    )