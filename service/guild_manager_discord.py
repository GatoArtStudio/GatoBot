from discord.ext import commands
from base.guild_messenger_discord import GuildMessengerDiscord
from base.guild_discord import GuildDiscord
from base.handler_logs_tools import HandlerLogsTools


class GuildManagerDiscord(GuildDiscord, GuildMessengerDiscord, HandlerLogsTools):

    def __init__(self, guild_id: int, bot: commands.Bot):
        GuildDiscord.__init__(self, guild_id)
        GuildMessengerDiscord.__init__(self, guild_id, bot)
