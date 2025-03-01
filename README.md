# 🐱 GatoBot

<div align="center">
  <img src="frontend/public/logo.svg" alt="GatoBot Logo" width="200"/>
  
  [![Discord](https://img.shields.io/badge/Discord-Add%20Bot-7289DA?style=for-the-badge&logo=discord&logoColor=white)](https://gatobot.gatoartstudio.art)
  [![Website](https://img.shields.io/badge/Website-Visit-2ea44f?style=for-the-badge&logo=firefox&logoColor=white)](https://gatobot.gatoartstudio.art)
</div>

## 📋 Descripción

GatoBot es un bot de Discord versátil y amigable, diseñado para mejorar la experiencia de tu servidor. Con una interfaz web moderna y funciones potentes, GatoBot combina utilidad y facilidad de uso.

## ✨ Características

### 🛡️ Moderación
- Gestión de usuarios (kick, ban, timeout)
- Sistema de advertencias
- Filtrado de contenido
- Logs de acciones

### 🎵 Música
- Reproducción de música de alta calidad
- Soporte para múltiples plataformas
- Control de cola y reproducción
- Comandos intuitivos

### 🎮 Diversión
- Comandos interactivos
- Mini-juegos
- Reacciones personalizadas

### ⚙️ Utilidades
- Sistema avanzado de embeds
- Anuncios personalizables
- Información del servidor
- Estadísticas

## 🚀 Uso

### Comandos Principales

```
/help - Muestra la lista de comandos
/play - Reproduce música
/create_embed - Crea embeds personalizados
/update_announcement - Envía anuncios globales (solo desarrollador)
```

### Ejemplos

1. **Reproducir Música**
   ```
   /play <URL o nombre de la canción>
   ```

2. **Crear Embed**
   ```
   /create_embed #canal
   ```

3. **Moderación**
   ```
   /timeout @usuario <duración> <razón>
   /warn @usuario <razón>
   ```

## 🛠️ Tecnologías

- **Backend**: Python, Discord.py
- **Frontend**: Astro, React, TailwindCSS
- **Base de Datos**: SQLite
- **API**: FastAPI
- **Contenedorización**: Docker

## 📥 Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/GatoArtStudio/GatoBot.git
   cd GatoBot
   ```

2. **Configurar variables de entorno**
   ```bash
   cp .env.example .env
   # Editar .env con tus tokens y configuraciones
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   cd frontend && npm install
   ```

4. **Iniciar el bot**
   ```bash
   # Usando Docker
   docker-compose up -d

   # Sin Docker
   python main.py
   ```

## 🌐 Arquitectura

```
GatoBot/
├── api/            # API REST con FastAPI
├── base/           # Núcleo del bot
├── commands/       # Comandos del bot
├── frontend/       # Interfaz web (Astro + React)
└── utils/          # Utilidades y helpers
```

## 🤝 Contribuir

Las contribuciones son bienvenidas! Por favor, lee nuestro [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👥 Créditos

Desarrollado con ❤️ por [GatoArtStudios](https://github.com/GatoArtStudios)

## 📞 Soporte

- [Servidor de Discord](https://discord.gg/tuservidor)
- [Sitio Web](https://gatobot.gatoartstudio.art)
- [Correo](mailto:contact@gatoartstudio.art)
