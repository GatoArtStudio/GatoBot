import sqlite3
import threading
from core.logging import Logger

# Instancia el debug
logger = Logger().get_logger()

class DataBase:
    def __init__(self, db_name = 'data_base.db'):
        self.db_name = db_name
        self._lock = threading.Lock()
        self._connect()

    def _connect(self) -> None:
        """Establece la conexión con la base de datos."""
        try:
            self.connection = sqlite3.connect(self.db_name, check_same_thread=False)
            self.cursor = self.connection.cursor()
            logger.info("Conexión a la base de datos establecida.")
        except sqlite3.Error as e:
            logger.error(f"Error al conectar con la base de datos: {e}")
            raise

    def run_query(self, query, params=()) -> bool:
        """Ejecuta una consulta SQL y guarda los cambios."""
        try:
            with self._lock:  # 🔒 Bloqueo para acceso seguro
                self.cursor.execute(query, params)
                self.connection.commit()
                logger.info(f"Consulta ejecutada: {query}")
                return True
        except sqlite3.Error as e:
            logger.error(f"Error en la consulta: {e}")
            return False

    def get_data(self, query, params=()) -> list:
        """Ejecuta una consulta de lectura y devuelve los resultados."""
        try:
            with self._lock:
                self.cursor.execute(query, params)
                return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Error al obtener datos: {e}")
            return []

    def close_connection(self) -> None:
        """Cierra la conexión a la base de datos de forma segura."""
        if self.connection:
            self.connection.close()
            logger.info("Conexión a la base de datos cerrada.")