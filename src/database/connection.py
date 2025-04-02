from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
# Hay que importar los modelos antes de usar Base.metadata.create_all(bind=self.engine), al importar los modelos, ya se crean las tablas
from models.guild_discord import GuildDiscord
from models.ip import Ip
from models.user_discord import UserDiscord
from models.link_temp import LinkTemp
from models.base import Base
from helpers.utils_class import class_singleton

from config.config import BIN_PATH, MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE


@class_singleton
class Database:

    database_path: str = BIN_PATH / "database.db"
    database_url: str = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    engine: create_engine
    session: Session

    def __init__(self) -> None:
        self.engine = create_engine(self.database_url, echo=True)
        session_local = sessionmaker(bind=self.engine)
        self.session = session_local()

    def create_tables(self) -> None:
        """
        Crea las tablas en la base de datos
        """
        # Base.metadata.drop_all(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    def get_session(self) -> Session:
        """
        Devuelve la sesion de la base de datos
        """
        return self.session