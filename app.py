import os
import json
from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Cargar configuración desde la variable de entorno `env`
try:
    config = json.loads(os.getenv('env', '{}'))
    mongo_uri = config.get("mongo_uri")
    if not mongo_uri:
        raise ValueError("La clave `mongo_uri` no está configurada en la variable `env`.")
except json.JSONDecodeError as e:
    raise RuntimeError(f"Error al cargar la configuración desde `env`: {e}")

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
