#!/bin/sh
echo "[GatoBot] Iniciando GatoBot..."
echo "[GatoBot] Instalando dependencias..."
pip install -r requirements.txt
echo "[GatoBot] Ejecutando GatoBot..."
exec python3 src/main.py
