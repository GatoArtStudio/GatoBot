from sqlalchemy import Integer, String, Boolean, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from models.base import Base


class LinkTemp(Base):
    __tablename__ = "link_temp"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    link: Mapped[str] = mapped_column(String(255), nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    expires: Mapped[int] = mapped_column(BigInteger, nullable=False)

    def __repr__(self):
        return f"LinkTemp(id={self.id}, link={self.link}, filename={self.filename}, active={self.active}, expires={self.expires})"