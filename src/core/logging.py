import logging
import os

import colorlog

from config.config import HOME_PATH, TMP_PATH


def setup_logging(service_name: str):
    """
    Maneja el debug
    """
    service_name = service_name.replace(' ', '_').replace('-', '_').replace('.', '_')

    logger = logging.getLogger(service_name)

    # Comentar esta validación para evitar que el logger se reinicialice mal
    # if logger.hasHandlers():
    #     return logger

    # Directorio de logs
    log_dir = TMP_PATH / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file_path = log_dir / f'{service_name}.log'

    # Archivo de log GENERAL para capturar todos los logs
    general_log_path = log_dir / 'application.log'

    # Formato de logs en consola con colores
    log_format = '%(asctime)s - [%(log_color)s%(levelname)s%(reset)s] - [%(name)s] - %(message)s'
    log_colors = {
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }

    # Handler de consola con colores
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(
        colorlog.ColoredFormatter(log_format, datefmt='%Y-%m-%d %H:%M:%S', log_colors=log_colors))

    # Handler de archivo para logs del servicio
    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s - [%(levelname)s] - [%(name)s] - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))

    # Handler de archivo para capturar **todos los logs** (incluyendo discord.py, FastAPI, etc.)
    general_file_handler = logging.FileHandler(general_log_path, encoding='utf-8')
    general_file_handler.setLevel(logging.DEBUG)
    general_file_handler.setFormatter(
        logging.Formatter('%(asctime)s - [%(levelname)s] - [%(name)s] - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))

    # Configura el logger del servicio
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Configura el **logger raíz** para capturar todos los logs
    root_logger = logging.getLogger()
    if not root_logger.hasHandlers():
        root_logger.setLevel(logging.DEBUG)
        root_logger.addHandler(console_handler)
        root_logger.addHandler(general_file_handler)  # Captura todo en application.log

    logger.propagate = False  # Evita duplicaciones en la consola

    return logger


# @class_singleton
class Logger:
    """
        Retorna un logger específico para cada servicio.
        ```python
        logger = Logger("mi_servicio").get_logger()
        logger.info("Este es un mensaje de información")
        ```
    """
    def __init__(self, service_name: str = 'services'):
        self.logger = setup_logging(service_name)

    def get_logger(self) -> logging.Logger:
        """
        Retorna el logger
        ```python
        Retorna el logger ya configurado.
        ```
        """
        return self.logger