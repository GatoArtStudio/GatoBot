from enum import Enum, auto

class EventType(Enum):

    """
    Todos los eventos de tipo BOT se les enviara un modelo bot_discord
    """
    BOT_STARTED = auto()
    BOT_STATUS = auto()
    BOT_READY = auto()
    BOT_LOGOUT = auto()
    BOT_ERROR = auto()
    BOT_SHUTDOWN = auto()
    BOT_RESTART = auto()
    BOT_RELOAD = auto()
    BOT_RELOAD_CONFIG = auto()
    BOT_RELOAD_GUILD = auto()
    BOT_RELOAD_GUILD_CONFIG = auto()
    BOT_RELOAD_GUILD_MESSENGER = auto()