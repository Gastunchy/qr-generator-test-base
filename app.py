from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Función para obtener el cliente de MongoDB
def get_mongo_client():
    # Carga el URI de MongoDB directamente desde el archivo .env
    mongo_uri = os.getenv('MONGO_URI')
    if not mongo_uri:
        raise ValueError("MONGO_URI no está configurado en las variables de entorno")
    return MongoClient(mongo_uri)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health_check():
    try:
        client = get_mongo_client()
        databases = client.list_database_names()
        db_summary = {db: len(client.get_database(db).list_collection_names()) for db in databases}
        return render_template('health.html', status="healthy", db_summary=db_summary)
    except Exception as e:
        return render_template('health.html', status="unhealthy", error=str(e))

@app.route('/dbinfo', methods=['GET'])
def db_info():
    try:
        client = get_mongo_client()
        databases = client.list_database_names()
        db_data = {}
        for db_name in databases:
            db = client.get_database(db_name)
            collections = db.list_collection_names()
            db_data[db_name] = {}
            for collection in collections:
                # Incluye documentos con `_id` excluido para evitar problemas de serialización
                db_data[db_name][collection] = list(db[collection].find({}, {"_id": 0}))
        return render_template('dbinfo.html', db_data=db_data)
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)