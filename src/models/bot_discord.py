from sqlalchemy import String, BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base

class BotDiscord(Base):

    __tablename__ = "bot_discord"

    id_bot_discord: Mapped[int] = mapped_column(BigInteger ,primary_key=True)
    status_runtime: Mapped[bool] = mapped_column(Boolean, default=False)
    token: Mapped[str] = mapped_column(String(255), nullable=False)
    client_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    client_secret: Mapped[str] = mapped_column(String(255), nullable=False)