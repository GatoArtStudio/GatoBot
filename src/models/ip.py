from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import mapped_column, Mapped

from models.base import Base


class Ip(Base):
    """
    Modelo Ip
    """

    __tablename__ = "ip"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ip: Mapped[str] = mapped_column(String(20), nullable=False)
    port: Mapped[int] = mapped_column(Integer, nullable=False, default=25565)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    # TODO: Agregar rol como proxy, web, etc
    rol: Mapped[str] = mapped_column(String(20), nullable=False)

    def __repr__(self):
        return f"Ip(id={self.id}, ip={self.ip}, port={self.port}, enabled={self.enabled}, rol={self.rol})"