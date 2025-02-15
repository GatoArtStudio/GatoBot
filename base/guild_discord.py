from service import DataBaseDiscord

class GuildDiscord:
    def __init__(self, guild_id: int):
        self.guild_id = guild_id
        self.db = DataBaseDiscord()
        self.config: dict = self._get_guild_config()

    def _get_guild_config(self) -> dict:
        """Obtiene la configuración del servidor desde la base de datos"""
        config = self.db.get_guild_config(self.guild_id)
        if not config:
            self.db.create_guild_config(self.guild_id)
            config = self.db.get_guild_config(self.guild_id)
        return config

    def set_log_channel(self, log_channel_id: int) -> None:
        """Establece el canal de logs en la base de datos"""
        query = 'INSERT INTO guild_config (guild_id, log_channel_id) VALUES (?, ?) ON CONFLICT(guild_id) DO UPDATE SET log_channel_id=excluded.log_channel_id'
        result = self.db.run_query(query, (self.guild_id, log_channel_id))
        if result:
            self.config['log_channel_id'] = log_channel_id
        return result
    
    def set_warning_channel(self, warning_channel_id: int) -> bool:
        """Establece el canal de advertencias en la base de datos"""
        query = 'INSERT INTO guild_config (guild_id, warning_channel_id) VALUES (?, ?) ON CONFLICT(guild_id) DO UPDATE SET warning_channel_id=excluded.warning_channel_id'
        result = self.db.run_query(query, (self.guild_id, warning_channel_id))
        if result:
            self.config['warning_channel_id'] = warning_channel_id
        return result
    
    def set_announcement_channel(self, announcement_channel_id: int) -> None:
        """Establece el canal de anuncios en la base de datos"""
        query = 'INSERT INTO guild_config (guild_id, announcement_channel_id) VALUES (?, ?) ON CONFLICT(guild_id) DO UPDATE SET announcement_channel_id=excluded.announcement_channel_id'
        result = self.db.run_query(query, (self.guild_id, announcement_channel_id))
        if result:
            self.config['announcement_channel_id'] = announcement_channel_id
        return result
    
    def set_sanction_channel(self, sanction_channel_id: int) -> None:
        """Establece el canal de sanciones en la base de datos"""
        query = 'INSERT INTO guild_config (guild_id, sanction_channel_id) VALUES (?, ?) ON CONFLICT(guild_id) DO UPDATE SET sanction_channel_id=excluded.sanction_channel_id'
        result = self.db.run_query(query, (self.guild_id, sanction_channel_id))
        if result:
            self.config['sanction_channel_id'] = sanction_channel_id
        return result

    def get_log_channel(self) -> int:
        """Devuelve el ID del canal de logs"""
        return self.config.get('log_channel_id', 0)

    def get_warning_channel(self) -> int:
        """Devuelve el ID del canal de advertencias"""
        return self.config.get('warning_channel_id', 0)

    def get_announcement_channel(self) -> int:
        """Devuelve el ID del canal de anuncios"""
        return self.config.get('announcement_channel_id', 0)

    def get_sanction_channel(self) -> int:
        """Devuelve el ID del canal de sanciones"""
        return self.config.get('sanction_channel_id', 0)
