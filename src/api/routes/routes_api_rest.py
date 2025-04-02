from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import datetime
import logging

from core.event import Event, EventType
from core.implements.discord_bot import DiscordBot
from core.logging import Logger
from models.bot_discord import BotDiscord


class Command(BaseModel):
    name: str
    description: str
    usage: Optional[str] = None

class BotStatus(BaseModel):
    status: str
    uptime: Optional[str] = None
    guild_count: Optional[int] = None

class BotApi:
    """
    Clase que encapsula las rutas de la api para manejar el bot de discord
    """

    logger: logging.Logger
    bot: DiscordBot = None
    bot_status_runtime: bool = False
    router: APIRouter
    event_manager: Event

    def __init__(self):
        self.logger = Logger('backend_api_bot').get_logger()
        self.router = APIRouter()
        self.event_manager = Event()

        # Rutas api al router
        self.router.add_api_route('/api/v1/status', self.get_bot_status, response_model=BotStatus, methods=['GET'])
        self.router.add_api_route('/api/v1/commands', self.get_commands, response_model=List[Command], methods=['GET'])

        # Eventos
        self.event_manager.listener(EventType.BOT_STATUS, self.on_bot_status_runtime)
        self.event_manager.listener(EventType.BOT_STARTED, self.on_bot_started)

        self.logger.info("Rutas api cargadas en el backend, listo para recibir solicitudes api.")

    def _format_uptime(self, td: Optional[datetime.timedelta]) -> Optional[str]:
        """
        Formatea un timedelta en un string legible (ej. '1d 2h 3m 45s').
        """
        if td is None:
            return None
        days = td.days
        hours, remainder = divmod(td.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        parts = []
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        parts.append(f"{seconds}s")
        return " ".join(parts)

    async def get_bot_status(self):
        try:
            if self.bot is None:
                return {
                    "status": "Not Ready",
                    "uptime": None,
                    "guild_count": 0
                }

            # Acceder a is_ready como propiedad, no como método
            is_ready = self.bot._is_ready
            uptime = self.bot.uptime
            guilds = self.bot.guilds

            return {
                "status": "online" if is_ready else "offline",
                "uptime": self._format_uptime(uptime) if uptime else None,
                "guild_count": len(guilds) if is_ready else 0
            }
        except Exception as e:
            self.logger.error(f"Error en get_self.bot_status: {str(e)}")
            return {
                "status": "Not Ready",
                "uptime": None,
                "guild_count": 0
            }

    async def get_commands(self):
        try:
            if self.bot is None:
                raise HTTPException(status_code=500, detail='Bot no iniciado')

            commands = []
            for cmd in self.bot.tree.get_commands():

                params = []
                if hasattr(cmd, 'parameters'):
                    for param in cmd.parameters:
                        param_str = f'<{param.name}: {param.type.name}>'
                        params.append(param_str)

                commands.append({
                    "name": cmd.name,
                    "description": cmd.description or "No description available",
                    "usage": f'/{cmd.name} {" ".join(params)}' if params else f'/{cmd.name}'
                })
            return commands
        except Exception as e:
            self.logger.error(str(e))
            raise HTTPException(status_code=500, detail=str(e))

    def on_bot_started(self, bot: DiscordBot):
        self.logger.info("Evento recibido de bot started")
        self.bot = bot

    def on_bot_status_runtime(self, data: BotDiscord):
        self.logger.info(f"Evento recibido de bot status runtime: {data.status_runtime}")
        self.bot_status_runtime = data.status_runtime
