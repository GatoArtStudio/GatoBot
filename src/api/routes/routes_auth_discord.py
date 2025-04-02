import logging

from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse

from config.config import DISCORD_URL_AUTHORIZE
from core.logging import Logger
from helpers.discord_auth_api import DiscordAuthAPI


class RoutesAuthDiscord:

    logger: logging.Logger
    router: APIRouter
    discord_auth_api: DiscordAuthAPI

    def __init__(self):
        self.logger = Logger('routes_auth_discord').get_logger()
        self.router = APIRouter()
        self.discord_auth_api = DiscordAuthAPI()

        # Rutas api al router
        self.router.add_api_route('/discord/login', self.handle_route_login, methods=['GET'])
        self.router.add_api_route('/discord/logout', self.handle_route_logout, methods=['GET'])
        self.router.add_api_route('/discord/oauth2/authorize/callback', self.handle_route_callback, methods=['GET'])


    async  def handle_route_login(self, request: Request):
        return RedirectResponse(url=DISCORD_URL_AUTHORIZE)

    async def handle_route_logout(self, request: Request):
        pass

    async def handle_route_callback(self, request: Request):
        # Obtener el código de autorización
        code = request.query_params.get("code")
        error = request.query_params.get("error")

        # Verificar si hay un error
        if error:
            return {"error": error}

        # Intercambiar el código de autorización por un token de acceso
        r = self.discord_auth_api.discord_exchange_code(code)

        access_token = r['access_token']
        refresh_token = r['refresh_token']

        # Devolver el token de acceso
        return {"access_token": access_token, "refresh_token": refresh_token}