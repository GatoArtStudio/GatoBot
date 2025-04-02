from __future__ import annotations

from sqlalchemy.orm import Session, Mapped

from database.connection import Database
from models.guild_discord import GuildDiscord as GuildM


class GuildDiscord:

    session_database: Session
    guild: GuildM | None

    def __init__(self, guild_id: int):
        self.guild_id = guild_id
        self.session_database = Database().get_session()
        self.guild = self.session_database.query(GuildM).filter_by(guild_id = guild_id).first()

        if self.guild is None:
            self.guild = GuildM(guild_id = guild_id)
            self.session_database.add(self.guild)
            self.session_database.commit()

    def set_log_channel(self, log_channel_id: int) -> bool:
        """Establece el canal de logs en la base de datos"""
        self.guild.log_channel_id = log_channel_id
        self.session_database.commit()
        return True
    
    def set_warning_channel(self, warning_channel_id: int) -> bool:
        """Establece el canal de advertencias en la base de datos"""
        self.guild.warning_channel_id = warning_channel_id
        self.session_database.commit()
        return True
    
    def set_announcement_channel(self, announcement_channel_id: int) -> bool:
        """Establece el canal de anuncios en la base de datos"""
        self.guild.announcement_channel_id = announcement_channel_id
        self.session_database.commit()
        return True
    
    def set_sanction_channel(self, sanction_channel_id: int) -> bool:
        """Establece el canal de sanciones en la base de datos"""
        self.guild.sanction_channel_id = sanction_channel_id
        self.session_database.commit()
        return True

    def get_log_channel(self) -> Mapped[int | None]:
        """Devuelve el ID del canal de logs"""
        return self.guild.log_channel_id

    def get_warning_channel(self) -> Mapped[int | None]:
        """Devuelve el ID del canal de advertencias"""
        return self.guild.warning_channel_id

    def get_announcement_channel(self) -> Mapped[int | None]:
        """Devuelve el ID del canal de anuncios"""
        return self.guild.announcement_channel_id

    def get_sanction_channel(self) -> Mapped[int | None]:
        """Devuelve el ID del canal de sanciones"""
        return self.guild.sanction_channel_id