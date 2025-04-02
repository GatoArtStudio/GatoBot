from sqlalchemy import Integer, Boolean, String, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from models.base import Base


class UserDiscord(Base):
    """
    Modelo User (Tabla en la BD)
    """

    __tablename__ = "user_discord"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    token_type: Mapped[str] = mapped_column(String(255), nullable=False)
    access_token: Mapped[str] = mapped_column(String(255), nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=False)
    token_expires_in: Mapped[int] = mapped_column(BigInteger, nullable=False)
    scope: Mapped[str] = mapped_column(String(255), nullable=False)
    guilds_ids: Mapped[str] = mapped_column(String(255), nullable=False)
    is_administrator: Mapped[bool] = mapped_column(Boolean, default=False)
    is_vip: Mapped[bool] = mapped_column(Boolean, default=False)
    suscribe: Mapped[bool] = mapped_column(Boolean, default=False)
    suscribe_expires_in: Mapped[int] = mapped_column(BigInteger, nullable=False)

    def __repr__(self):
        return (f"<User user_id={self.user_id} "
                f"token_type={self.token_type} "
                f"access_token={self.access_token} "
                f"refresh_token={self.refresh_token} "
                f"token_expires_in={self.token_expires_in} "
                f"scope={self.scope} "
                f"guilds_ids={self.guilds_ids} "
                f"is_administrator={self.is_administrator} "
                f"is_vip={self.is_vip} "
                f"suscribe={self.suscribe} "
                f"suscribe_expires_in={self.suscribe_expires_in}>"
                )