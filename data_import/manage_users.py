import os
from pymongo import MongoClient
import bcrypt
from dotenv import load_dotenv
from mongo_utils import connect_to_mongo

# Chargement des variables d'environnement
load_dotenv()

def register(username, password, role="user"):
    client = connect_to_mongo()
    db = client["health_db"]
    users = db["users"]
    if users.find_one({"username": username}):
        print("Utilisateur déjà existant")
        return False
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users.insert_one({"username": username, "password": hashed_pw, "role": role})
    print("Utilisateur enregistré avec succès (rôle : {}).".format(role))
    return True

def login(username, password):
    client = connect_to_mongo()
    db = client["health_db"]
    users = db["users"]
    user = users.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        print(f"Connexion réussie. Rôle : {user.get('role', 'user')}")
        return user
    print("Nom d'utilisateur ou mot de passe invalide")
    return None

def admin_menu(admin_user):
    print("\n=== Menu Admin ===")
    print("1. Créer un nouvel utilisateur (admin ou user)")
    print("2. Quitter")
    choix = input("Votre choix : ").strip()
    if choix == "1":
        username = input("Nom d'utilisateur : ")
        password = input("Mot de passe : ")
        role = input("Rôle (admin/user) [user] : ") or "user"
        register(username, password, role)
    else:
        print("Déconnexion admin.")

def user_menu(user):
    print("\n=== Menu User ===")
    print("Pas de privilèges spéciaux")
    print("Déconnexion")

if __name__ == "__main__":
    print("Connectez-vous (seul un admin peut créer d'autres admins) :")
    username = input("Nom d'utilisateur : ")
    password = input("Mot de passe : ")
    user = login(username, password)
    if user:
        if user["role"] == "admin":
            admin_menu(user)
        else:
            user_menu(user)