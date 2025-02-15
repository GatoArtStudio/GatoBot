from base.data_base import DataBase
from utils.utils_class import class_singleton

@class_singleton
class DataBaseDiscord(DataBase):
    '''
    Base de datos para la configuración de los servidores
    '''
    def __init__(self, db_name = 'data_base_discord.db'):
        super().__init__(db_name)
        self.valid_servers = []
        self.load_valid_servers()
        self.create_tables_guild_config()

    def load_valid_servers(self):
        '''
        Carga el id de los servidores validos o registrados en la base de datos
        '''
        query = 'SELECT guild_id FROM guild_config'
        self.valid_servers = [guild_id[0] for guild_id in self.get_data(query)]

    def create_tables_guild_config(self):
        """Crea las tablas para la configuración de los servidores."""
        self.run_query('''
            CREATE TABLE IF NOT EXISTS guild_config (
                guild_id INTEGER PRIMARY KEY,
                log_channel_id INTEGER,
                warning_channel_id INTEGER,
                announcement_channel_id INTEGER,
                sanction_channel_id INTEGER
            )
        ''')

    def create_guild_config(self, guild_id: int, log_channel_id: int = None, warning_channel_id: int = None,
                            announcement_channel_id: int = None, sanction_channel_id: int = None) -> bool:
        """Crea o actualiza la configuración de un servidor, sin sobrescribir valores existentes."""
    
        # Verificar si el registro ya existe
        existing_config = self.get_guild_config(guild_id)
        
        if existing_config:  # Si ya existe, actualizamos solo los valores proporcionados
            updates = []
            values = []

            if log_channel_id is not None:
                updates.append("log_channel_id = ?")
                values.append(log_channel_id)
            if warning_channel_id is not None:
                updates.append("warning_channel_id = ?")
                values.append(warning_channel_id)
            if announcement_channel_id is not None:
                updates.append("announcement_channel_id = ?")
                values.append(announcement_channel_id)
            if sanction_channel_id is not None:
                updates.append("sanction_channel_id = ?")
                values.append(sanction_channel_id)

            if updates:  # Solo ejecutar UPDATE si hay campos a modificar
                query = f"UPDATE guild_config SET {', '.join(updates)} WHERE guild_id = ?"
                values.append(guild_id)
                return self.run_query(query, tuple(values))
            return True  # No hubo nada que actualizar

        else:  # Si no existe, creamos el registro
            query = '''
                INSERT INTO guild_config (guild_id, log_channel_id, warning_channel_id, announcement_channel_id, sanction_channel_id)
                VALUES (?, ?, ?, ?, ?)
            '''
            return self.run_query(query, (guild_id, log_channel_id or 0, warning_channel_id or 0, announcement_channel_id or 0, sanction_channel_id or 0))
    
    def get_guild_config(self, guild_id: int) -> dict:
        query = '''
            SELECT * FROM guild_config WHERE guild_id = ?
        '''
        result = self.get_data(query, (guild_id,))
        
        if result:
            columns = ["guild_id", "log_channel_id", "warning_channel_id", "announcement_channel_id", "sanction_channel_id"]
            return dict(zip(columns, result[0]))
        
        return {}
