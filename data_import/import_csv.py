#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import pandas as pd
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

# Pour forcer le flush immédiat des print() dans Docker
sys.stdout.reconfigure(line_buffering=True)

def connect_to_mongo():
    load_dotenv()
    username = os.getenv("MONGO_INITDB_ROOT_USERNAME")
    password = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
    uri = f"mongodb://{username}:{password}@mongodb:27017/?authSource=admin"
    return MongoClient(uri)

def load_data():
    """
    Lit dataset.csv et en extrait :
      - patients_df   : colonnes Name, Age, Gender, Blood Type + _id
      - hospitals_df  : colonnes Hospital + _id
      - doctors_df    : colonnes Doctor + _id
      - admissions_df : toutes les lignes (pour boucler dessus)
    """
    df = pd.read_csv("/app/data/dataset.csv")

    # Patients uniques
    patients_df = (
        df[["Name", "Age", "Gender", "Blood Type"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    patients_df["_id"] = patients_df.index.astype(str)

    # Hôpitaux uniques
    hospitals_df = (
        df[["Hospital"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    hospitals_df["_id"] = hospitals_df.index.astype(str)

    # Docteurs uniques
    doctors_df = (
        df[["Doctor"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    doctors_df["_id"] = doctors_df.index.astype(str)

    # On gardera df complet pour créer les admissions
    admissions_df = df

    return patients_df, hospitals_df, doctors_df, admissions_df

def build_mappings(patients_df, hospitals_df, doctors_df):
    """Crée des dicts name→_id pour lookup rapide."""
    patient_map  = dict(zip(patients_df["Name"],    patients_df["_id"]))
    hospital_map = dict(zip(hospitals_df["Hospital"], hospitals_df["_id"]))
    doctor_map   = dict(zip(doctors_df["Doctor"],   doctors_df["_id"]))
    return patient_map, hospital_map, doctor_map

def prepare_admissions(admissions_df, patient_map, hospital_map, doctor_map):
    """Construit la liste de documents Admission à insérer."""
    admissions = []
    for i, row in admissions_df.iterrows():
        pid = patient_map.get(row["Name"])
        hid = hospital_map.get(row["Hospital"])
        did = doctor_map.get(row["Doctor"])

        # Vérification des références
        if pid is None:
            print(f"⚠️  Patient '{row['Name']}' non trouvé (ligne {i})")
            continue
        if hid is None:
            print(f"⚠️  Hôpital '{row['Hospital']}' non trouvé (ligne {i})")
            continue
        if did is None:
            print(f"⚠️  Médecin '{row['Doctor']}' non trouvé (ligne {i})")
            continue

        # Conversion de la date si nécessaire
        try:
            doa = datetime.strptime(row["Date of Admission"], "%Y-%m-%d")
        except Exception:
            doa = row["Date of Admission"]

        admissions.append({
            "patientId":        pid,
            "hospitalId":       hid,
            "doctorId":         did,
            "medicalCondition": row["Medical Condition"],
            "dateOfAdmission":  doa,
            "insuranceProvider": row["Insurance Provider"],
            "billingAmount":     float(row["Billing Amount"]),
        })
    return admissions

def insert_into_mongo(patients, hospitals, doctors, admissions):
    client = connect_to_mongo()
    db     = client["health_db"]

    # Ré-initialisation des collections
    db.patients.delete_many({})
    db.hospitals.delete_many({})
    db.doctors.delete_many({})
    db.admissions.delete_many({})

    # Insertions
    print(f"✅ Insertion {len(patients)} patients…")
    db.patients.insert_many(patients)

    print(f"✅ Insertion {len(hospitals)} hôpitaux…")
    db.hospitals.insert_many(hospitals)

    print(f"✅ Insertion {len(doctors)} médecins…")
    db.doctors.insert_many(doctors)

    print(f"✅ Insertion {len(admissions)} admissions…")
    if admissions:
        db.admissions.insert_many(admissions)
    print("✅ Import terminé !")

def main():
    print("▶️  Démarrage de l'import normalisé…")

    # 1. Lecture et extraction des DataFrames
    patients_df, hospitals_df, doctors_df, admissions_df = load_data()

    # 2. Mapping name → _id
    patient_map, hospital_map, doctor_map = build_mappings(
        patients_df, hospitals_df, doctors_df
    )

    # 3. Préparation des admissions
    admissions = prepare_admissions(
        admissions_df, patient_map, hospital_map, doctor_map
    )

    # 4. Conversion des DataFrames en liste de dicts
    patients  = patients_df.to_dict(orient="records")
    hospitals = hospitals_df.to_dict(orient="records")
    doctors   = doctors_df.to_dict(orient="records")

    # 5. Insertion en base
    insert_into_mongo(patients, hospitals, doctors, admissions)

if __name__ == "__main__":
    main()
