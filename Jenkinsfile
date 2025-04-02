pipeline {
    agent any

    stages {

        stage('Clonando repositorio de git') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/GatoArtStudio/GatoBot.git'
            }
        }

        stage('Verificando variables de entorno') {
            steps {
                script {
                    sh """
                    # Verificar si el archivo .env existe
                    if [ -f .env ]; then
                        echo "El archivo .env existe"
                    else
                        echo "El archivo .env no existe"
                        exit 1
                    fi
                    """
                }
            }
        }
        
        stage('Detener docker') {
            steps {
                script {
                    sh """
                    # Verificar si el contenedor está en ejecución
                    if docker ps -f "name=${CONTAINER_NAME}" | grep -q "${CONTAINER_NAME}"; then
                        echo "El contenedor ${CONTAINER_NAME} está en ejecución"
                        # Bajar el contenedor
                        docker-compose down
                    else
                        # Omitir si no está en ejecución
                        echo "El contenedor ${CONTAINER_NAME} no está en ejecución, omitiendo."
                    fi
                    """
                }
            }
        }
        
        stage('Iniciando docker del gatobot') {
            steps {
                sh 'docker-compose up -d'
            }
        }
    }
}
