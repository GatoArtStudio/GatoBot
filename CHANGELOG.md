# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
