import os
import json
from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient
#from dotenv import load_dotenv
from google.cloud import secretmanager

def load_secret(secret_version_name: str) -> str:
    """
    Carga el valor de un secreto desde Google Secret Manager.
    
    :param secret_version_name: Nombre completo del secreto.
    :return: El valor del secreto como una cadena decodificada.
    :raises RuntimeError: Si no se puede acceder al secreto.
    """
    try:
        client = secretmanager.SecretManagerServiceClient()
        response = client.access_secret_version(request={"name": secret_version_name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        raise RuntimeError(f"Error al acceder al secreto: {e}")


def parse_config(env: str) -> dict:
    """
    Parsea un JSON de configuración desde una cadena.
    
    :param env: Cadena JSON a parsear.
    :return: Diccionario con la configuración.
    :raises ValueError: Si la configuración no contiene claves esperadas.
    :raises json.JSONDecodeError: Si la cadena no es un JSON válido.
    """
    config = json.loads(env)
    if "mongo_uri" not in config:
        raise ValueError("La clave `mongo_uri` no está configurada en el secreto.")
    return config


# Nombre del secreto en Google Secret Manager
SECRET_VERSION_NAME = "projects/970772571927/secrets/test-base-secret/versions/latest"

# Cargar el secreto y la configuración
try:
    env = load_secret(SECRET_VERSION_NAME)
    config = parse_config(env)
    mongo_uri = config["mongo_uri"]
    print("Configuración cargada exitosamente.")
except Exception as e:
    raise RuntimeError(f"Error al inicializar la aplicación: {e}")

# Configurar la aplicación Flask
app = Flask(__name__)


# Función para obtener el cliente de MongoDB
def get_mongo_client():
    try:
        return MongoClient(mongo_uri)
    except Exception as e:
        raise RuntimeError(f"Error al conectar con MongoDB: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health_check():
    """Revisar el estado de la conexión a MongoDB y listar bases de datos."""
    try:
        client = get_mongo_client()
        databases = client.list_database_names()
        db_summary = {
            db: len(client.get_database(db).list_collection_names()) for db in databases
        }
        return render_template('health.html', status="healthy", db_summary=db_summary)
    except Exception as e:
        return render_template('health.html', status="unhealthy", error=str(e))

@app.route('/dbinfo', methods=['GET'])
def db_info():
    """Obtener información detallada de las bases de datos y sus colecciones."""
    try:
        client = get_mongo_client()
        databases = client.list_database_names()
        db_data = {
            db_name: {
                collection: list(client[db_name][collection].find({}, {"_id": 0}))
                for collection in client[db_name].list_collection_names()
            }
            for db_name in databases
        }
        return render_template('dbinfo.html', db_data=db_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def page_not_found(e):
    """Manejar errores 404 con una página personalizada."""
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)))
