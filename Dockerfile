# Imagen base de Python
FROM python:3.11

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar solo requirements.txt para cachear la instalación de dependencias
COPY requirements.txt /app/requirements.txt

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto que el bot usará
EXPOSE 25978
EXPOSE 26206