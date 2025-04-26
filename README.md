# Migration des Données Médicales vers MongoDB & Déploiement sur AWS | OpenClassrooms Projet 5

## 📌 Contexte
Dans le cadre d’une mission, nous devons migrer un dataset de patients vers **MongoDB** afin d’améliorer la scalabilité et la gestion des données. De plus, nous devons explorer des solutions pour un déploiement efficace sur **AWS**.

## 🎯 Objectifs
1. **Migration des données vers MongoDB via Docker**
   - Automatiser l’importation du dataset en utilisant un script de migration.
   - Conteneuriser MongoDB et les scripts de migration avec Docker.
   - Assurer la version et la sauvegarde du projet sur GitHub.
   - Documenter en détail le processus et inclure un schéma de la base de données.
   - Mettre en place un système d’authentification et de gestion des rôles utilisateurs.

2. **Déploiement sur AWS**
   - Explorer différentes solutions pour héberger MongoDB sur AWS.
   - Comparer les services AWS pertinents : Amazon **S3, RDS pour MongoDB, DocumentDB, ECS**.
   - Justifier les choix technologiques en fonction des besoins du client.

---

## 📂 Structure du projet

Local :
```text
MongoSafeCloud/
├── data/
│   └── dataset.csv
├── data_import/
│   ├── Dockerfile
│   ├── import_csv.py
│   └── requirements.txt
├── .env
├── .gitignore
├── compose.yaml
├── Dockerfile
└── README.md
```
Build sous docker :
```text
MongoSafeCloud/
/app
├── requirements.txt         
├── import_csv.py            
├── data/                    
│   └── dataset.csv
└── .env                    
```

---

## 🚀 Installation et Exécution

### 1️⃣ Prérequis
- **Docker & Docker Compose** installés


### 2️⃣ Installation
Cloner le dépôt :
```bash
git clone https://github.com/Xantos07/MongoSafeCloud.git
cd MongoSafeCloud
```

Initialisation pour un build:
```bash
docker-compose build 
```

Lancement du build:
```bash
docker-compose up -d
```

---

Schéma de la base de donnée : 

![Schéma de la base de données](images/schema_db.png)

Schéma Docker  : 

![Schéma de la base de données](images/schema_docker.png)


---

## 🛠️ Technologies & Justification

| Technologie          | Raison du choix                                                                        |
|----------------------|----------------------------------------------------------------------------------------|
| **Docker / Compose** | Isolation des services et portabilité ; déploiement rapide et reproductible.           |
| **MongoDB**          | Base NoSQL scalable, schéma flexible pour des données médicales.                       |
| **mongo-express**    | Interface web légère pour administrer la base sans installer de client externe.        |
| **Python 3 + pandas**| Traitement et nettoyage du CSV, scripting simple pour l’import automatique.            |
| **Git**              | Versioning, revue de code et collaboration facilitées.                                 |

---

## Environnement 

### Variables d’environnement à configurer

 - Pour la base de données MongoDB

```text
MONGO_INITDB_ROOT_USERNAME=VotreUserRoot
MONGO_INITDB_ROOT_PASSWORD=VotreMdpRoot
```

- Pour l’accès à mongo-express

```text
ME_CONFIG_BASICAUTH_USERNAME=VotreUSER
ME_CONFIG_BASICAUTH_PASSWORD=VotreMDP
```

⚠️ Attention :
mongo-express ne supporte qu’une seule connexion utilisateur à la fois (pas de multi-utilisateur).

## 🔒 Authentification & Gestion des Rôles

Pour garantir la sécurité de la base de données, trois rôles principaux sont mis en place :

| Rôle         | Description                                                         |
|--------------|---------------------------------------------------------------------|
| **admin**    | Accès complet à toutes les fonctionnalités et données               |
| **readWrite**| Lire, écrire, créer/supprimer des collections et des indexes        |
| **read**     | Accès en lecture seule                                              |

Les mots de passe et identifiants sont sécurisés conformément à la documentation MongoDB :  
=> [Gestion des utilisateurs MongoDB](https://www.mongodb.com/docs/manual/reference/method/db.createUser/)

### Création et gestion des utilisateurs

1. **Se connecter au conteneur MongoDB**

Se connecter au container en question : 


```bash
docker exec -it mongodb bash
```

2. **Se connecter en tant qu’administrateur**

(Les identifiants sont dans le fichier .env)

```bash
mongosh -u $MONGO_INITDB_ROOT_USERNAME -p $MONGO_INITDB_ROOT_PASSWORD --authenticationDatabase admin
```

3. **Créer un nouvelle utilisateur**

```bash
use health_db
```
```bash
db.createUser({
user: "userReadWrite",
pwd: "votreMDP",
roles: [ { role: "readWrite", db: "health_db" } ]
})
```
```bash
db.createUser({
user: "userRead",
pwd: "votreMDP",
roles: [ { role: "read", db: "health_db" } ]
})
```


4. **Connexion avec un utilisateur spécifique**


```bash
mongosh "mongodb://userReadWrite:votreMDP@localhost:27017/health_db"
```

ou

```bash
mongosh "mongodb://userRead:votreMDP@localhost:27017/health_db"
```

**Remarques :**

Les utilisateurs sont créés dans la base admin mais affectés à la base cible (health_db).

mongo-express ne permet la connexion qu’avec un seul utilisateur à la fois. 


## 📢 Présentation finale

- **Le contexte de la mission**
- **La démarche technique**
- **Les choix technologiques et leur justification**

Jeu de données d’exemple :
https://www.kaggle.com/datasets/prasad22/healthcare-dataset/data?select=healthcare_dataset.csv


