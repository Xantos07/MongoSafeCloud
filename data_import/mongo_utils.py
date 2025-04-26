import os
from pymongo import MongoClient
from dotenv import load_dotenv

def connect_to_mongo():
    load_dotenv()
    username = os.getenv("MONGO_INITDB_ROOT_USERNAME")
    password = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
    host = os.getenv("MONGO_HOST", "mongodb")
    uri = f"mongodb://{username}:{password}@{host}:27017/?authSource=admin"
    return MongoClient(uri)
