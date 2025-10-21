# 🍲 Woody Vert Restaurant (Full Stack)

Bienvenue dans le dépôt du projet final Woody Vert Restaurant. Ce projet est une application web complète (full-stack) composée d'un backend **Flask (Python)** et d'un frontend **React (JavaScript)**.

## 🚀 Démarrage du Projet

Pour exécuter l'application localement, vous devez configurer et démarrer à la fois le backend (API) et le frontend (Interface Utilisateur).

### 📋 Prérequis

Vous devez avoir :

1.  **Python 3.10+** et **pip**.
2.  **Node.js** (recommandé 18+) et **npm** ou **yarn**.
3.  Un environnement de développement configuré (terminal, éditeur de code).

-----

## 💻 1. Configuration et Démarrage du Backend (API)

Le backend est une API RESTful construite avec Flask, Flask-RESTful et SQLAlchemy.

### 🛠️ Installation du Backend

1.  **Naviguez vers le dossier `server` :**
    ```bash
    cd server
    ```
2.  **Créez un environnement virtuel Python :**
    ```bash
    python -m venv venv
    source venv/bin/activate # Sous Linux/macOS
    .\venv\Scripts\activate   # Sous Windows
    ```
3.  **Installez les dépendances Python :**
    ```bash
    pip install -r requirements.txt
    # Assurez-vous d'avoir un requirements.txt complet ou installez les dépendances
    ```

### ⚙️ Configuration Backend

1.  **Créez un fichier `.env`** à la racine du dossier `server` et ajoutez votre clé secrète :
    ```dotenv
    # .env (dans /server)
    SECRET_KEY="VOTRE_CLÉ_SECRÈTE_FLASK_TRES_LONGUE"
    ```

### 🗃️ Base de Données (SQLite)

Le projet utilise SQLite pour la base de données de développement (`sqlite:///food_app.db`).

1.  **Initialisation/Création des tables :**
    ```bash
    flask db init          # Si c'est la première fois
    flask db migrate -m "Initial setup" # Créer le script de migration
    flask db upgrade       # Appliquer la migration pour créer les tables
    ```
2.  **Remplissage de la base (Seed) :**
    *Si vous avez un fichier `seed.py` :*
    ```bash
    python seed.py
    ```

### 🚀 Démarrage du Serveur API

Lancez le serveur Flask. L'API sera accessible à l'adresse par défaut : `http://127.0.0.1:5000`.

```bash
flask run
```

-----

## 🌐 2. Configuration et Démarrage du Frontend (React)

Le frontend est une application React qui communique avec l'API Flask sur le port 5000.

### 🛠️ Installation du Frontend

1.  **Naviguez vers le dossier `client` (ou là où se trouve votre code React) :**
    *(Ajustez le chemin si votre dossier frontend s'appelle différemment, par exemple, `frontend` ou `client`.)*
    ```bash
    cd ../client 
    ```
2.  **Installez les dépendances Node.js :**
    ```bash
    npm install
    # OU
    yarn install
    ```

### ⚙️ Configuration Frontend

Le frontend doit savoir où trouver le backend. Par défaut, React développe sur le port 3000, et votre API est sur le port 5000.

1.  **Créez un fichier `.env.local`** à la racine du dossier `client` pour définir l'URL de l'API :
    ```dotenv
    # .env.local (dans /client)
    # Assurez-vous que ce port correspond à celui où Flask est lancé (5000 par défaut)
    REACT_APP_API_BASE_URL=http://127.0.0.1:5000
    ```
2.  *(**Note :** Si vous utilisez un proxy dans le `package.json` de React, cette étape peut ne pas être nécessaire.)*

### 🚀 Démarrage de l'Application Frontend

Lancez l'application React. Elle sera accessible à l'adresse par défaut : `http://localhost:3000`.

```bash
npm start
# OU
yarn start
```

## 🎉 L'Application est Prête \!

Vous devriez maintenant avoir :

  * Le **Backend Flask** en cours d'exécution sur **Port 5000** (fournissant les données).
  * Le **Frontend React** en cours d'exécution sur **Port 3000** (l'interface utilisateur).

-----

## 🗺️ Structure de l'API Backend

| Endpoint | Méthode | Description |
| :--- | :--- | :--- |
| `/food_users` | `GET` / `POST` | Gère la liste et l'inscription des utilisateurs. |
| `/restaurants` | `GET` / `POST` | Gère la liste et la création de restaurants. |
| `/reviews` | `GET` / `POST` | Gère les critiques (`?restaurant_id=X` disponible). |
| `/login` | **`POST`** | Connexion de l'utilisateur. |
| `/logout` | **`DELETE`** | Déconnexion de l'utilisateur. |
| `/check_session` | **`GET`** | Vérifie l'état de la connexion. |