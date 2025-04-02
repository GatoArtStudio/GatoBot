from __future__ import annotations

from abc import ABC, abstractmethod

import sqlalchemy
from sqlalchemy.orm import Session

from core.interfaces.i_database_crud import IDatabaseCRUD
from core.logging import Logger
from models.base import Base


class BaseCRUD(ABC, IDatabaseCRUD):
    """
    Implementacion base para operaciones CRUD en la base de datos.
    """

    model: Base  # Modelo de la base de datos (se define en las clases hijas
    logger: Logger

    def create(self, session: Session, obj: Base) -> Base | None:
        """
        Crear un nuevo registro en la BD
        :param session: Sesión de la base de datos
        :param obj: Un objeto de tipo Guild
        """
        if not isinstance(obj, Base) or obj is None:
            return None

        if self.logger:
            self.logger.info(f"Creando un nuevo registro: {obj}")

        try:
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj
        except sqlalchemy.exc.IntegrityError as e:
            session.rollback()
            if self.logger:
                self.logger.error(f"Error al crear el registro: {e}")
            return None
        except sqlalchemy.exc.PendingRollbackError as e:
            session.rollback()
            if self.logger:
                self.logger.error(f"Error al crear el registro: {e}")
            return None

    def read(self, session: Session) -> list:
        """
        Obtener todos los registro de guilds
        :param session: Sesión de la base de datos
        """
        return session.query(self.model).all()

    @abstractmethod
    def update(self, session: Session, obj: Base, **kwargs) -> Base | None:
        """
        Actualizar un registro existente
        :param session: Sesión de la base de datos
        :param obj: Objeto a actualizar
        :param kwargs: Datos actualizados
                """
        if not isinstance(obj, Base) or obj is None:
            if self.logger:
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
            if self.logger:
                self.logger.error(f"Error al actualizar el registro: {e}")
            return None

    def delete(self, session: Session, obj: Base) -> bool:
        """
        Eliminar un registro
        :param session: Sesión de la base de datos
        :param obj: Objeto a eliminar
        """
        if not isinstance(obj, Base) or obj is None:
            return False

        session.delete(obj)
        session.commit()
        return True