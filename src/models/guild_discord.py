from typing import Optional

from sqlalchemy import Integer, Boolean, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class GuildDiscord(Base):
    """
    Modelo Guild (Tabla en la BD)
    """
    __tablename__ = "guild_discord"

    # primary_key=True, therefore will be NOT NULL
    guild_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    log_channel_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    warning_channel_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    announcement_channel_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    # Optional[], therefore will be NULL
    sanction_channel_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    # not Optional[], therefore will be NOT NULL
    active_antispam: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self):
        return (f"<Guild guild_id={self.guild_id} "
                f"log_channel_id={self.log_channel_id} "
                f"warning_channel_id={self.warning_channel_id} "
                f"announcement_channel_id={self.announcement_channel_id} "
                f"sanction_channel_id={self.sanction_channel_id} "
                f"active_antispam={self.active_antispam}>"
                )