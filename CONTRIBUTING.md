# 🤝 Contribuyendo a GatoBot

¡Gracias por tu interés en contribuir a GatoBot! Este documento proporciona las pautas y mejores prácticas para contribuir al proyecto.

## 📋 Tabla de Contenidos

1. [Código de Conducta](#código-de-conducta)
2. [¿Cómo puedo contribuir?](#cómo-puedo-contribuir)
3. [Reportando Bugs](#reportando-bugs)
4. [Sugiriendo Mejoras](#sugiriendo-mejoras)
5. [Pull Requests](#pull-requests)
6. [Estilo de Código](#estilo-de-código)

## 📜 Código de Conducta

Este proyecto y todos sus participantes están bajo el [Código de Conducta de Contribuyentes](CODE_OF_CONDUCT.md). Al participar, se espera que mantengas este código. Por favor, reporta cualquier comportamiento inaceptable a [contact@gatoartstudio.art](mailto:contact@gatoartstudio.art).

## 🤔 ¿Cómo puedo contribuir?

### 🐛 Reportando Bugs

1. **Verifica que el bug no haya sido reportado**
   * Revisa la sección de [Issues](https://github.com/GatoArtStudios/GatoBot/issues) en GitHub

2. **Crea un nuevo issue**
   * Usa el template de bug report
   * Incluye un título claro y descriptivo
   * Describe los pasos para reproducir el problema
   * Describe el comportamiento esperado
   * Describe el comportamiento actual
   * Incluye capturas de pantalla si es posible

### 💡 Sugiriendo Mejoras

1. **Verifica que la mejora no haya sido sugerida**
   * Revisa la sección de [Issues](https://github.com/GatoArtStudios/GatoBot/issues)

2. **Crea un nuevo issue**
   * Usa el template de feature request
   * Proporciona un título claro
   * Explica en detalle la mejora propuesta
   * Describe los beneficios de la mejora

## 🔄 Pull Requests

1. **Fork el repositorio**

2. **Crea una nueva rama**
   ```bash
   git checkout -b feature/nombre-de-tu-feature
   ```

3. **Haz tus cambios**
   * Sigue las guías de estilo de código
   * Añade o actualiza tests si es necesario
   * Actualiza la documentación si es necesario

4. **Commit tus cambios**
   ```bash
   git commit -m "feat: descripción corta de tus cambios"
   ```
   * Usa [Conventional Commits](https://www.conventionalcommits.org/)
   * Tipos comunes: feat, fix, docs, style, refactor, test, chore

5. **Push a tu fork**
   ```bash
   git push origin feature/nombre-de-tu-feature
   ```

6. **Crea el Pull Request**
   * Usa el template de pull request
   * Describe los cambios realizados
   * Vincula issues relacionados

## 💻 Estilo de Código

### Python
* Sigue [PEP 8](https://www.python.org/dev/peps/pep-0008/)
* Usa type hints cuando sea posible
* Documenta las funciones con docstrings
* Mantén las líneas a un máximo de 100 caracteres

### JavaScript/TypeScript
* Usa ESLint y Prettier
* Sigue las guías de Airbnb
* Usa TypeScript cuando sea posible

### Commits
* Usa [Conventional Commits](https://www.conventionalcommits.org/)
* Mantén los commits pequeños y enfocados
* Escribe mensajes descriptivos

## ⚙️ Setup del Ambiente de Desarrollo

1. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configura pre-commit hooks**
   ```bash
   pre-commit install
   ```

3. **Ejecuta los tests**
   ```bash
   pytest
   ```

## 📝 Notas Adicionales

* Mantén las discusiones respetuosas y profesionales
* Sé paciente con las revisiones de código
* Pregunta si tienes dudas

¡Gracias por contribuir a GatoBot! 🎉
