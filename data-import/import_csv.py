import pandas as pd
from pymongo import MongoClient
import os
from dotenv import load_dotenv

print("✅ Start PYTHON !")

load_dotenv()

MONGO_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")

print(f"MONGO_USERNAME: {MONGO_USERNAME}")
print(f"MONGO_PASSWORD: {MONGO_PASSWORD}")

connection_string = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@mongodb:27017/?authSource=admin&authMechanism=SCRAM-SHA-256&retryWrites=true"
#connection_string = f"mongodb://root:secret@mongodb:27017/?authSource=admin&authMechanism=SCRAM-SHA-256&retryWrites=true"

client = MongoClient(connection_string)

db = client["health_db"]
collection = db["health_collection"]

csv_file = "/app/data/dataset.csv"

df = pd.read_csv(csv_file)

data = df.to_dict(orient="records")

# Insérer les données dans la collection MongoDB
collection.insert_many(data)

print("✅ Importation terminée avec succès !")
