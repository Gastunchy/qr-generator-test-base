from flask import Flask, jsonify
from pymongo import MongoClient
from google.cloud import secretmanager
import os

app = Flask(__name__)

def get_secret(secret_name):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/970772571927/secrets/test-base-secret/versions/latest"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode('UTF-8')

@app.route('/health', methods=['GET'])
def health_check():
    try:
        mongo_uri = get_secret('MONGO_URI')
        client = MongoClient(mongo_uri)
        db = client.get_database()
        db.command('ping')
        return jsonify(status='healthy'), 200
    except Exception as e:
        return jsonify(status='unhealthy', error=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)