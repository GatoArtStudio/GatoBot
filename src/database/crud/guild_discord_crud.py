import sqlalchemy
from sqlalchemy.orm import Session

from core.interfaces.i_database_crud import IDatabaseCRUD
from models.guild_discord import GuildDiscord
from core.logging import Logger


class GuildCRUD(IDatabaseCRUD):
    """
    Implementación de CRUD para el modelo User.
    """

    model: GuildDiscord = GuildDiscord
    logger: Logger = Logger("GuildCRUD").get_logger()

    def read(self, session: Session) -> list:
        """
        Obtener todos los registro de guilds
        :param session: Sesión de la base de datos
        """
        return session.query(self.model).all()

    def get_by_id(self, session: Session, guild_id: int) -> GuildDiscord:
        """
        Obtener un registro por ID
        :param session: Sesión de la base de datos
        :param guild_id: ID del registro - guild_id
        """
        return session.query(self.model).filter(self.model.guild_id == guild_id).first()

    def create(self, session: Session, obj: GuildDiscord) -> GuildDiscord | None:
        """
        Crear un nuevo registro en la BD
        :param session: Sesión de la base de datos
        :param obj: Un objeto de tipo Guild
        """
        self.logger.info(f"Creando un nuevo registro: {obj}")

        try:
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj
        except sqlalchemy.exc.IntegrityError as e:
            session.rollback()
            self.logger.error(f"Error al crear el registro: {e}")
            return None
        except sqlalchemy.exc.PendingRollbackError as e:
            session.rollback()
            self.logger.error(f"Error al crear el registro: {e}")
            return None

    def update(self, session: Session, obj: GuildDiscord, **kwargs):
        """
        Actualizar un registro existente
        :param session: Sesión de la base de datos
        :param obj: Objeto a actualizar
        :param kwargs: Datos actualizados
        """
        if not isinstance(obj, GuildDiscord) or obj is None:
            self.logger.error("Objeto no válido")
            return None

        for key, value in kwargs.items():
            setattr(obj, key, value)

        try:
            session.commit()
            session.refresh(obj)
            return obj
        except Exception as e:
            session.rollback()
            self.logger.error(f"Error al actualizar el registro: {e}")
            return None