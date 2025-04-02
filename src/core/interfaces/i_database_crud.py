from __future__ import annotations

from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from core.logging import Logger
from models.base import Base


class IDatabaseCRUD(ABC):
    """
    Interfaz base para operaciones CRUD en la base de datos.
    """

    model: Base  # Modelo de la base de datos (se define en las clases hijas
    logger: Logger

    @abstractmethod
    def create(self, session: Session, obj: Base) -> Base | None:
        """
        Crear un nuevo registro en la BD
        :param session: Sesión de la base de datos
        :param obj: Un objeto de tipo Guild
        """
        pass

    @abstractmethod
    def read(self, session: Session) -> list:
        """
        Obtener todos los registro de guilds
        :param session: Sesión de la base de datos
        """
        pass

    @abstractmethod
    def update(self, session: Session, obj: Base, **kwargs):
        """Actualizar un registro existente."""
        pass

    @abstractmethod
    def delete(self, session: Session, obj: Base) -> bool:
        """
        Eliminar un registro
        :param session: Sesión de la base de datos
        :param obj: Objeto a eliminar
        """
        pass