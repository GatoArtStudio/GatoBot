# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.1] - 2025-04-01

### 🚀 Cambios Importantes
- Implementación de la API REST para sistema de autenticación
- Mejoras en el frontend para mejorar la experiencia del usuario
- Mejoras en el backend para mejorar la seguridad y rendimiento
- Reestructuración del proyecto para mejorar la organización
- Nuevo sistema de eventos para mejorar la comunicación entre componentes
- Sistema de comandos para iniciar servicios por separado

### ✨ Añadido

- **Frontend**
  - Se implemento para iniciar sesión con Discord

- **Backend**
  - Se agrego los endpoints de autenticación con discord
  - Se agrego el sistema de comandos para iniciar servicios por separado
  - Se agrego el sistema de eventos para mejorar la comunicación entre componentes

- **DevOps**
  - Ahora el main es el script de arranque, donde se despliegan los servicios
  - Se agrego el script de build para construir el frontend
  - Dockerfile mejorado para optimizar la construcción

### 🔧 Modificado
- `main.py -> src/main.py`: Refactorizado para mejor manejo de servicios
- `estructura`: EL proyecto fue movido al directorio src
- `requirements.txt`: Actualizadas dependencias
- `.gitignore`: Actualizado para nuevos archivos
- `Paths`: Actualizados para mejor manejo de rutas
- `.env`: Se Agregan variables de entorno

### 🗑️ Eliminado
- Sistema antiguo de archivos estáticos
- Endpoints HTTP simples
- Formato de directorios para binarios necesarios
- Los Tests fueron eliminados

### 🏗️ Estructura del Proyecto
```
GatoBot/
└── src
   ├── api/            # API REST con FastAPI
   ├── assets/         # Recursos estáticos
   ├── commands/       # Comandos del bot
   ├── config/         # Configuraciones
   ├── core/           # Núcleo del bot
   ├── database/       # Base de datos
   ├── events/         # Eventos del bot
   ├── frontend/       # Interfaz web (Astro + React)
   ├── helpers/        # Utilidades y helpers
   ├── models/         # Modelos de datos
   ├── services/       # Servicios
   ├── views/          # Vistas de discord
   └── main.py         # Punto de entrada
```

### 🔍 Detalles Técnicos
- MySQL-connector-python: 9.2.0
- SQLAlchemy: 2.0.38
- pytest: 8.3.4
- psutil: 7.0.0
- pydantic: 2.10.6
- pyMySQL: 1.1.1
- pathlib: 1.0.1

### 📝 Notas
- El proyecto sigue en desarrollo, y se espera mejorar en el futuro.
- Asegúrate de tener las nuevas variables de entorno correctas
- Ahora el fronted se despliega y construye solo con el script de arranque
- Ahora se pueden agregar mas servicios si es necesario solo haciendo uso del patron comando
- Proximamente se agregara un receivers para mejorar la comunicación entre componentes
- Por ahora se necesita colocar los binarios necesarios de forma manual dentro de `.local`

## [2.0.0] - 2025-02-28

### 🚀 Cambios Importantes
- Migración completa del frontend a Astro Framework
- Nueva API REST implementada con FastAPI
- Sistema mejorado de instalación de Node.js para Docker
- Integración con Cloudflare Tunnel

### ✨ Añadido
- **Frontend**
  - Nuevo framework Astro para mejor rendimiento
  - Componentes React para UI interactiva
  - Tailwind CSS para estilos modernos
  - TypeScript para mejor tipado
  - Nuevo diseño responsive y moderno

- **Backend**
  - API REST con FastAPI
  - Sistema de rutas modular
  - Mejor manejo de errores y logging
  - Endpoints optimizados

- **DevOps**
  - Sistema robusto de instalación de Node.js
  - Mejor manejo de permisos en Docker
  - Scripts de automatización
  - Sistema de build mejorado

### 🔧 Modificado
- `main.py`: Refactorizado para mejor manejo de servicios
- `base/bot.py`: Simplificado y mejorado
- `requirements.txt`: Actualizadas dependencias
- `.gitignore`: Actualizado para nuevos archivos

### 🗑️ Eliminado
- Sistema antiguo de archivos estáticos
- Endpoints HTTP simples
- Manejo manual de Node.js

### 🏗️ Estructura del Proyecto
```
GatoBot/
├── api/                # Nueva API REST
├── frontend/          # Frontend con Astro
│   ├── src/
│   │   ├── components/
│   │   ├── layouts/
│   │   └── pages/
├── scripts/           # Scripts de automatización
└── www/              # Archivos estáticos
```

### 🔍 Detalles Técnicos
- Node.js v22.14.0
- Python 3.11+
- Astro 4.x
- FastAPI 0.115+
- Tailwind CSS 3.x

### 📝 Notas
- Este es un cambio importante (breaking change)
- Se requiere reconstruir el frontend al desplegar
- Asegúrate de tener las variables de entorno correctas
