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
docker-compose build --no-cache
```

Lancement du build:
```bash
docker-compose up -d
```

---

Schéma de la B=base de donnée : 

![Schéma de la base de données](images/schema_db.png)

Schéma Docker  : 

![Schéma de la base de données](images/schema_docker.png)

## 📢 Présentation finale

- **Le contexte de la mission**
- **La démarche technique**
- **Les choix technologiques et leur justification**

---

Donnée de test sur : 
https://www.kaggle.com/datasets/prasad22/healthcare-dataset/data?select=healthcare_dataset.csv
