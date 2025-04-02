from enum import Enum

from core.enums.e_types_services import ETypesServices


class EDiscordBot(Enum):
    # Geneal
    TYPE_SERVICE = ETypesServices.DISCORD_BOT.value
    LOGGING = "LOGGING"
    REDY = "READY"
    START_TIME = "START_TIME"

    # Models

    # Methods
    @staticmethod
    def get_key_state(id_service: int = 0) -> str:
        """
        Get key state
        example:
            DISCORD_BOT_234234

        :param id_service:
        """
        return f'{EDiscordBot.TYPE_SERVICE.value}_{id_service}'

print(EDiscordBot.get_key_state())