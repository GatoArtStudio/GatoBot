if [[ -d .git ]] && [[ "1" == "1" ]]; then 
    echo "[GatoBot] Reseteando cambios locales..." && \
    git reset --hard HEAD && \
    echo "[GatoBot] Actualizando desde git..." && \
    git pull
fi

if [[ ! -z "" ]]; then 
    pip install -U --prefix .local
fi

if [[ -f /home/container/${REQUIREMENTS_FILE} ]]; then 
    pip install -U --prefix .local -r ${REQUIREMENTS_FILE}
fi

/usr/local/bin/python /home/container/src/main.py