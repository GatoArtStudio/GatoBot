import discord
import typing
from discord.ext import commands
from discord import app_commands
import aiohttp

class Minecraft(commands.Cog):
    """Comandos para monitorear servidores de Minecraft"""

    def __init__(self, bot):
        self.bot = bot
        self.api_url = "https://api.mcsrvstat.us/3/"
        self.api_url_bedrock = "https://api.mcsrvstat.us/bedrock/3/"

    async def obtener_datos(self, ip: str, bedrock: bool = False):
        """Realiza una petición al endpoint del servidor de Minecraft"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.api_url if bedrock == False else self.api_url_bedrock}{ip}') as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return None

    mc = app_commands.Group(name='mc', description='comandos para utilidades de minecraft.')

    @mc.command(name="serverinfo", description='Obtiene informacion de una ip de un servidor de Minecraft.')
    async def serverinfo(self, interaction: discord.Interaction, ip: typing.Optional[str] = None, ip_bedrock: typing.Optional[str] = None):
        """📜 Muestra información del servidor Minecraft"""
        datos = await self.obtener_datos(f"{ip if ip_bedrock is None else ip_bedrock}", False if ip_bedrock is None else True)
        ip = datos.get("ip", "Desconocido")
        if not datos or ip is None and ip_bedrock is None or '127.0.0.1' in ip:
            await interaction.response.send_message(f"⚠️ No se pudo obtener la información del servidor{", debes colocar una ip o ip valida." if ip is None and ip_bedrock is None else "."}", ephemeral=True)
            return

        puerto = datos.get("port", "Desconocido")
        motd = datos.get("motd", {}).get("clean", ["No disponible"])[0]
        jugadores_online = datos.get("players", {}).get("online", "0")
        jugadores_max = datos.get("players", {}).get("max", "0")
        version = datos.get("version", "Desconocida")
        online = datos.get("online", False)
        software = datos.get("software", "Desconocida")



        embed = discord.Embed(title="🌍 Información del Servidor Minecraft", color=discord.Color.green())
        embed.add_field(name="IP", value=f"`{ip}:{puerto}`", inline=True)
        embed.add_field(name="Versión", value=f"{version}", inline=True)
        embed.add_field(name="MOTD", value=f"{motd}", inline=False)
        embed.add_field(name="Jugadores", value=f"👥 {jugadores_online}/{jugadores_max}", inline=False)
        embed.add_field(name="Estado", value=f"{"Online" if online == True else "Offline"}", inline=True)
        (lambda: embed.add_field(name="Software", value=f"{software}", inline=True) if software != 'Desconocida' else None)()

        await interaction.response.send_message(embed=embed)

    @mc.command(name="jugadores", description='Obtiene la cantidad de jugadores conectados en el servidor.')
    async def jugadores(self, interaction: discord.Interaction, ip: typing.Optional[str] = None, ip_bedrock: typing.Optional[str] = None):
        """👥 Lista los jugadores conectados en el servidor"""
        datos = await self.obtener_datos(f"{ip if ip_bedrock is None else ip_bedrock}", False if ip_bedrock is None else True)
        ip = datos.get("ip", "Desconocido")
        if not datos or ip is None and ip_bedrock is None or '127.0.0.1' in ip:
            await interaction.response.send_message(f"⚠️ No se pudo obtener la información del servidor{", debes colocar una ip o ip valida." if ip is None and ip_bedrock is None else "."}", ephemeral=True)
            return

        jugadores_online = datos.get("players", {}).get("online", 0)
        maximo_jugadores = datos.get("players", {}).get("max", 0)

        if jugadores_online == 0:
            await interaction.response.send_message("🚫 No hay jugadores conectados en este momento.", ephemeral=True)
        else:
            await interaction.response.send_message(f"👥 **Jugadores conectados ({jugadores_online}/{maximo_jugadores}):**")

    @mc.command(name="pingserver", description='Hace un ping al servidor para saber si esta online.')
    async def pingserver(self, interaction: discord.Interaction, ip: typing.Optional[str] = None, ip_bedrock: typing.Optional[str] = None):
        """🏓 Muestra el ping del servidor Minecraft"""
        datos = await self.obtener_datos(f"{ip if ip_bedrock is None else ip_bedrock}", False if ip_bedrock is None else True)
        ip = datos.get("ip", "Desconocido")
        if not datos or ip is None and ip_bedrock is None or '127.0.0.1' in ip:
            await interaction.response.send_message(f"⚠️ No se pudo obtener la información del servidor{", debes colocar una ip o ip valida." if ip is None and ip_bedrock is None else "."}", ephemeral=True)
            return

        ping = datos.get("debug", {}).get("ping", "Desconocido")
        await interaction.response.send_message(f"🏓 **Ping del servidor:** {ping} ms")

async def setup(bot):
    await bot.add_cog(Minecraft(bot))
