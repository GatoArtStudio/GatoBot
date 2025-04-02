from typing import Any

import requests

from config.config import DISCORD_CLIENT_ID, DISCORD_CLIENT_SECRET, DISCORD_REDIRECT_URI


class DiscordAuthAPI:

    discord_api_endpoint = 'https://discord.com/api/v10'

    def discord_refresh_token(self, refresh_token: str) -> Any:
        """
        Refresca el token de acceso utilizando el token de actualización
        """
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        r = requests.post('%s/oauth2/token' % self.discord_api_endpoint, data=data, headers=headers, auth=(DISCORD_CLIENT_ID, DISCORD_CLIENT_SECRET))
        return r.json()

    def discord_exchange_code(self, code: str) -> Any:
        """
        Intercambia el código de autorización por un token de acceso
        """
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': DISCORD_REDIRECT_URI
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        r = requests.post('%s/oauth2/token' % self.discord_api_endpoint, data=data, headers=headers, auth=(DISCORD_CLIENT_ID, DISCORD_CLIENT_SECRET))
        return r.json()

    def discord_revoke_access_token(self, access_token: str) -> Any:
        """
        Revoca el token de acceso
        """
        data = {
            'token': access_token,
            'token_type_hint': 'access_token'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        r = requests.post('%s/oauth2/token/revoke' % self.discord_api_endpoint, data=data, headers=headers,auth=(DISCORD_CLIENT_ID, DISCORD_CLIENT_SECRET))
        return r.json()