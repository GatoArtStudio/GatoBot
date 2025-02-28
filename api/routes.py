from fastapi import APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from base.bot import bot
import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class Command(BaseModel):
    name: str
    description: str
    usage: Optional[str] = None

class BotStatus(BaseModel):
    status: str
    uptime: Optional[str] = None
    guild_count: Optional[int] = None

def format_uptime(td: Optional[datetime.timedelta]) -> Optional[str]:
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

@router.get("/api/status", response_model=BotStatus)
async def get_bot_status():
    try:
        # Acceder a is_ready como propiedad, no como método
        is_ready = getattr(bot, '_is_ready', False)
        uptime = getattr(bot, 'uptime', None)
        guilds = getattr(bot, 'guilds', [])
        
        return {
            "status": "online" if is_ready else "offline",
            "uptime": format_uptime(uptime) if uptime else None,
            "guild_count": len(guilds) if is_ready else 0
        }
    except Exception as e:
        logger.error(f"Error en get_bot_status: {str(e)}")
        return {
            "status": "error",
            "uptime": None,
            "guild_count": 0
        }

@router.get("/api/commands", response_model=List[Command])
async def get_commands():
    try:
        commands = []
        for cmd in bot.commands:
            commands.append({
                "name": cmd.name,
                "description": cmd.description or "No description available",
                "usage": cmd.usage
            })
        return commands
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
