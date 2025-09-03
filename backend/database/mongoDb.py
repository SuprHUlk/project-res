from pymongo import AsyncMongoClient

mongo_client = None

def get_mongo_client():
    if mongo_client is None:
        raise Exception("Mongo client not ready")
    
    return mongo_client

def set_mongo_client():
    global mongo_client
    try:
        client = AsyncMongoClient("mongodb+srv://admin:admin@cluster0.mhdcgcd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
        mongo_client = client['test']
        print("MongoDB client set successfully")
    except Exception as e:
        print(f"Could not set mongo client: {e}");