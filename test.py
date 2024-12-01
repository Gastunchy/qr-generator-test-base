from pymongo import MongoClient

MONGO_URI = "mongodb+srv://chiquito:96p3o1l9WBNDAwnn@basenueva.hxpdn.mongodb.net/?retryWrites=true&w=majority&appName=BaseNueva"

try:
    client = MongoClient(MONGO_URI)
    db_names = client.list_database_names()
    print("Databases:", db_names)
except Exception as e:
    print("Error connecting to MongoDB:", str(e))
