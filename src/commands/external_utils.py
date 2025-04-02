import logging
import typing
import discord
from discord import app_commands
from discord.ext import commands

from core.implements.discord_bot import DiscordBot
from src.config.config import USER_DEV_ID
from src.helpers.colors import ColorDiscord

# Instancia el debug
logger: logging.Logger

class EmbedModal(discord.ui.Modal):
    def __init__(self, view):
        super().__init__(title="Crear Embed")
        self.view = view
        
        # Agregar campos al modal
        self.add_item(discord.ui.TextInput(
            label="Título del Embed",
            placeholder="Ingresa el título...",
            required=True,
            max_length=256,
            custom_id="title"
        ))
        
        self.add_item(discord.ui.TextInput(
            label="Descripción",
            placeholder="Ingresa la descripción...",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=4000,
            custom_id="description"
        ))
        
        self.add_item(discord.ui.TextInput(
            label="Color (hex)",
            placeholder="#ff0000",
            required=False,
            max_length=7,
            default="#1f75ff",
            custom_id="color"
        ))
        
        self.add_item(discord.ui.TextInput(
            label="Texto del Footer",
            placeholder="Texto opcional al pie del embed...",
            required=False,
            max_length=2048,
            custom_id="footer"
        ))

    async def on_submit(self, interaction: discord.Interaction):
        try:
            # Obtener valores de los campos
            title = self.children[0].value
            description = self.children[1].value
            color_value = self.children[2].value or "#1f75ff"
            footer = self.children[3].value

            # Convertir color hex a int
            try:
                color_int = int(color_value.lstrip('#'), 16)
            except ValueError:
                color_int = ColorDiscord.AQUA.value
            
            # Crear el embed
            embed = discord.Embed(
                title=title,
                description=description,
                color=color_int
            )
            
            if footer:
                embed.set_footer(text=footer)
                
            # Guardar el embed en la vista padre
            self.view.embeds.append(embed)
            await interaction.response.send_message("¡Embed creado con éxito!", ephemeral=True)
            
            # Actualizar la vista con el nuevo embed
            await self.view.update_message(interaction)
            
        except Exception as e:
            logger.error(f"Error al crear embed: {str(e)}")
            await interaction.response.send_message(f"Error al crear el embed: {str(e)}", ephemeral=True)

class FieldModal(discord.ui.Modal):
    def __init__(self, view, embed_index):
        super().__init__(title="Agregar Field al Embed")
        self.view = view
        self.embed_index = embed_index
        
        self.add_item(discord.ui.TextInput(
            label="Nombre del Field",
            placeholder="Título del campo...",
            required=True,
            max_length=256,
            custom_id="name"
        ))
        
        self.add_item(discord.ui.TextInput(
            label="Valor",
            placeholder="Contenido del campo...",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=1024,
            custom_id="value"
        ))
        
        self.add_item(discord.ui.TextInput(
            label="Inline",
            placeholder="true o false",
            required=False,
            max_length=5,
            default="true",
            custom_id="inline"
        ))

    async def on_submit(self, interaction: discord.Interaction):
        try:
            name = self.children[0].value
            value = self.children[1].value
            inline = self.children[2].value.lower() == "true"
            
            if self.embed_index >= len(self.view.embeds):
                await interaction.response.send_message("❌ Error: El embed ya no existe", ephemeral=True)
                return
                
            embed = self.view.embeds[self.embed_index]
            embed.add_field(name=name, value=value, inline=inline)
            
            await interaction.response.send_message(f"✅ Field agregado al embed #{self.embed_index + 1}!", ephemeral=True)
            await self.view.update_message(interaction)
            
        except Exception as e:
            logger.error(f"Error al agregar field: {str(e)}")
            await interaction.response.send_message(f"❌ Error al agregar field: {str(e)}", ephemeral=True)

class EmbedView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.embeds = []
        self.target_channel = None
    
    @discord.ui.button(label="📝 Nuevo Embed", style=discord.ButtonStyle.green, row=0)
    async def add_embed(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = EmbedModal(self)
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="➕ Agregar Field", style=discord.ButtonStyle.blurple, row=0)
    async def add_field(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.embeds:
            await interaction.response.send_message("❌ Primero crea un embed!", ephemeral=True)
            return
            
        # Si hay múltiples embeds, preguntamos a cuál agregar el field
        if len(self.embeds) > 1:
            options = [
                discord.SelectOption(
                    label=f"Embed #{i+1}",
                    description=f"Título: {embed.title[:50]}..." if embed.title else "Sin título",
                    value=str(i)
                ) for i, embed in enumerate(self.embeds)
            ]
            
            select = discord.ui.Select(
                placeholder="Selecciona el embed para agregar el field",
                options=options,
                custom_id="embed_select"
            )
            
            async def select_callback(interaction: discord.Interaction):
                embed_index = int(select.values[0])
                modal = FieldModal(self, embed_index)
                await interaction.response.send_modal(modal)
            
            select.callback = select_callback
            
            temp_view = discord.ui.View(timeout=30)
            temp_view.add_item(select)
            await interaction.response.send_message("Selecciona el embed:", view=temp_view, ephemeral=True)
        else:
            # Si solo hay un embed, lo agregamos directamente a ese
            modal = FieldModal(self, 0)
            await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="🗑️ Eliminar Último", style=discord.ButtonStyle.red, row=0)
    async def remove_embed(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.embeds:
            self.embeds.pop()
            await interaction.response.send_message("✅ ¡Último embed eliminado!", ephemeral=True)
            await self.update_message(interaction)
        else:
            await interaction.response.send_message("❌ No hay embeds para eliminar", ephemeral=True)
    
    @discord.ui.button(label="📨 Enviar Embeds", style=discord.ButtonStyle.green, row=1)
    async def send_embeds(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.target_channel:
            await interaction.response.send_message("❌ ¡Primero selecciona un canal!", ephemeral=True)
            return
            
        if not self.embeds:
            await interaction.response.send_message("❌ ¡No hay embeds para enviar!", ephemeral=True)
            return
            
        try:
            for embed in self.embeds:
                await self.target_channel.send(embed=embed)
            await interaction.response.send_message(f"✅ ¡Embeds enviados a {self.target_channel.mention}!", ephemeral=True)
            self.embeds = []
            await self.update_message(interaction)
        except Exception as e:
            logger.error(f"Error al enviar embeds: {str(e)}")
            await interaction.response.send_message("❌ Error al enviar los embeds", ephemeral=True)
    
    async def update_message(self, interaction: discord.Interaction):
        content = "**📝 Editor de Embeds**\n"
        if self.target_channel:
            content += f"📍 Canal: {self.target_channel.mention}\n"
        
        if self.embeds:
            content += f"📚 Embeds creados: {len(self.embeds)}\n\n"
            for i, embed in enumerate(self.embeds):
                content += f"**Embed #{i+1}**:\n"
                content += f"• Título: {embed.title or 'Sin título'}\n"
                content += f"• Fields: {len(embed.fields)}\n"
        else:
            content += "📚 No hay embeds creados"
        
        try:
            await interaction.message.edit(content=content, view=self)
        except:
            await interaction.channel.send(content=content, view=self)

class ExternalUtils(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def is_developer(self, interaction: discord.Interaction):
        """Verifica si el usuario es el desarrollador del bot."""
        return interaction.user.id == int(USER_DEV_ID)

    @app_commands.command(name='update_announcement', description='Informa en todos los canales que esta, sobre la actualizacion del bot')
    async def update_announcement(self, interaction: discord.Interaction, message: str, title: typing.Optional[str] = 'Actualización'):
        await interaction.response.defer(ephemeral=True)

        if not self.is_developer(interaction):
            await interaction.followup.send("No tienes permisos para usar este comando, solo el desarrollador.", ephemeral=True)
            return

        for guild in self.bot.guilds:
            system_channel = guild.system_channel
            if system_channel is not None:
                try:
                    message_formtated = message.replace('\\n', '\n')
                    embed = discord.Embed(
                        title=title,
                        description=message_formtated,
                        color=ColorDiscord.AQUA.value
                    )
                    await system_channel.send(embed=embed)
                except discord.errors.Forbidden:
                    logger.warning(f'No tengo permiso para enviar el mensaje en el canal {system_channel.mention} del servidor {guild.name}')
                    await interaction.followup.send(f'No tengo permiso para enviar el mensaje en el canal {system_channel.mention} del servidor {guild.name}', ephemeral=True)
                except discord.errors.HTTPException:
                    logger.warning(f'No puedo enviar el mensaje en el canal {system_channel.mention} del servidor {guild.name}')
                    await interaction.followup.send(f'No puedo enviar el mensaje en el canal {system_channel.mention} del servidor {guild.name}', ephemeral=True)

        await interaction.followup.send(f'Anuncio enviado en todos los servidores', ephemeral=True)

    @app_commands.command(name='create_embed', description='Abre el editor de embeds')
    @app_commands.describe(channel='Canal donde se enviarán los embeds')
    async def create_embed(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """Crea embeds de forma interactiva y los envía al canal especificado."""
        if not self.is_developer(interaction):
            await interaction.response.send_message("No tienes permisos para usar este comando.", ephemeral=True)
            return

        view = EmbedView()
        view.target_channel = channel
        
        await interaction.response.send_message(
            "**📝 Editor de Embeds**\n"
            f"📍 Canal: {channel.mention}\n"
            "📚 No hay embeds creados",
            view=view,
            ephemeral=True
        )

    @app_commands.command(name='set_role', description='Darle rol a un usuario')
    @app_commands.describe(user='Usuario a darle el rol', role='Rol a darle al usuario')
    async def set_role(self, interaction: discord.Interaction, user: discord.Member, role: discord.Role):
        if not self.is_developer(interaction):
            await interaction.response.send_message("No tienes permisos para usar este comando.", ephemeral=True)
            return

        await user.add_roles(role)
        await interaction.response.send_message(f'El rol {role.mention} se le ha dado al usuario {user.mention}', ephemeral=True)

    @app_commands.command(name='remove_role', description='Quitarle rol a un usuario')
    @app_commands.describe(user='Usuario a quitarle el rol', role='Rol a quitarle al usuario')
    async def remove_role(self, interaction: discord.Interaction, user: discord.Member, role: discord.Role):
        if not self.is_developer(interaction):
            await interaction.response.send_message("No tienes permisos para usar este comando.", ephemeral=True)
            return

        await user.remove_roles(role)
        await interaction.response.send_message(f'El rol {role.mention} se le ha quitado al usuario {user.mention}', ephemeral=True)

    @app_commands.command(name='get_roles', description='Obtener los roles de un servidor')
    async def get_roles(self, interaction: discord.Interaction):
        if not self.is_developer(interaction):
            await interaction.response.send_message("No tienes permisos para usar este comando.", ephemeral=True)
            return

        roles = [role.mention for role in interaction.guild.roles]
        await interaction.response.send_message(f'Roles del servidor {interaction.guild.name}: {", ".join(roles)}', ephemeral=True)


async def setup(bot: DiscordBot):
    """
    Agrega el cog al bot
    """

    global logger
    logger = bot.logger

    await bot.add_cog(ExternalUtils(bot))