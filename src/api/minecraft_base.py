import aiohttp
import hashlib

class MinecraftBase:
    def __init__(self):
        self.api_url = "https://api.mcsrvstat.us/3/"
        self.api_url_bedrock = "https://api.mcsrvstat.us/bedrock/3/"
        self.api_url_mojang_uuid = "https://api.mojang.com/users/profiles/minecraft/{username}?at=1513527763"

    async def obtener_datos(self, ip: str, bedrock: bool = False):
        """Realiza una petición al endpoint del servidor de Minecraft"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.api_url if not bedrock else self.api_url_bedrock}{ip}') as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return None

    async def obtener_uuid(self, username: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.api_url_mojang_uuid.replace("{username}", username)}') as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return None

    def generate_uuid_offline(self, username):
        """Genera un uuid offline a partir de un username"""
        string = "OfflinePlayer:" + username
        hash = hashlib.md5(string.encode("utf-8")).digest()
        byte_array = [byte for byte in hash]
        byte_array[6] = hash[6] & 0x0F | 0x30  # set the version to 3 -> Name based md5 hash
        byte_array[8] = hash[8] & 0x3F | 0x80  # IETF variant

        hash_modified = bytes(byte_array)
        offline_player_uuid = hash_modified.hex()
        offline_player_uuid_formated = self.format_uuid(hash_modified.hex())

        return offline_player_uuid, offline_player_uuid_formated

    def format_uuid(self, string):
        """Agrega los guiones al uuid"""
        string_striped = (
            string[:8]
            + "-"
            + string[8:12]
            + "-"
            + string[12:16]
            + "-"
            + string[16:20]
            + "-"
            + string[20:]
        )
        return string_striped