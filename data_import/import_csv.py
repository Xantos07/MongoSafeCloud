import pandas as pd
from pymongo import MongoClient
import os
from dotenv import load_dotenv

print("✅ Start PYTHON !")

def addition(a, b):
    return a + b

def connect_to_mongo():
    load_dotenv()
    MONGO_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME")
    MONGO_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
    connection_string = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@mongodb:27017/?authSource=admin&authMechanism=SCRAM-SHA-256&retryWrites=true"
    client = MongoClient(connection_string)
    return client

def import_data_to_mongo():
    client = connect_to_mongo()
    db = client["health_db"]
    collection = db["health_collection"]
    csv_file = "/app/data/dataset.csv"
    df = pd.read_csv(csv_file)
    data = df.to_dict(orient="records")
    collection.insert_many(data)
    print("✅ Importation terminée avec succès !")

if __name__ == "__main__":
    import_data_to_mongo()


