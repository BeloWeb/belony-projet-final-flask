

# 🍲 Woody Vert Restaurant API (Backend)

Bienvenue dans le dépôt backend de l'application Woody Vert Restaurant, construit avec Flask. Cette API RESTful gère les utilisateurs, les restaurants, les critiques (reviews), les menus, les plats, les favoris et l'authentification (y compris Google OAuth).

## 🚀 Démarrage

Suivez ces étapes pour configurer et exécuter l'application localement.

### 📋 Prérequis

Vous devez avoir **Python 3.10+** et **pip** installés.

### 🛠️ Installation

1.  **Clonez le dépôt :**

    ```bash
    git clone https://github.com/BeloWeb/belony-projet-final-flask.git
    cd server
    ```

2.  **Créez un environnement virtuel** (fortement recommandé) :

    ```bash
    python -m venv venv
    source venv/bin/activate  # Sous Linux/macOS
    source venv/script/activate   # Sous Windows
    ```

3.  **Installez les dépendances :**

    ```bash
    pip install -r requirements.txt
    # Si vous n'avez pas de requirements.txt, installez les paquets vus dans app.py :
    # pip install Flask Flask-SQLAlchemy Flask-Migrate Flask-RESTful Flask-CORS Flask-Bcrypt python-dotenv Authlib Flask-Login requests
    ```

### ⚙️ Configuration de l'Environnement

Créez un fichier **`.env`** à la racine du dossier `server` pour stocker les clés secrètes :

```dotenv
# .env
SECRET_KEY="VOTRE_CLÉ_SECRÈTE_FLASK"

```

### 🗃️ Base de Données (SQLite)

Le projet utilise **SQLite** pour la base de données de développement (`sqlite:///food_app.db`).

1.  **Initialisation de la base de données :**
    ```bash
    flask db init
    ```
2.  **Création des tables à partir des modèles :**
    ```bash
    flask db migrate -m "Initial database setup"
    flask db upgrade
    ```
3.  *Optionnel : Exécutez le script `seed.py` pour ajouter des données de test si vous en avez un.*

### 🚀 Démarrage du Serveur

Lancez le serveur Flask :

```bash
flask run
```

L'API sera accessible à l'adresse par défaut : `http://127.0.0.1:5000`

-----

## 🗺️ Structure de l'API

L'API est construite avec **Flask-RESTful** et offre les endpoints suivants pour gérer les ressources du restaurant :

| Endpoint | Méthode | Description |
| :--- | :--- | :--- |
| `/food_users` | `GET` | Récupère la liste de tous les utilisateurs. |
| `/food_users` | `POST` | Crée un nouvel utilisateur (inscription). |
| `/food_users/<int:id>` | `GET` | Récupère un utilisateur spécifique. |
| `/food_users/<int:id>` | `PATCH` | Met à jour le profil ou le mot de passe de l'utilisateur. |
| `/food_users/<int:id>` | `DELETE` | Supprime un utilisateur. |
| `/restaurants` | `GET` | Liste tous les restaurants (vue résumée). |
| `/restaurants` | `POST` | Crée un nouveau restaurant. |
| `/restaurants/<int:id>` | `GET` | Récupère les détails d'un restaurant, y compris les revues et les favoris. |
| `/reviews` | `GET` | Liste toutes les revues ou filtre par `?restaurant_id=X`. |
| `/reviews` | `POST` | Crée une nouvelle revue. |
| `/reviews/<int:id>` | `PATCH/DELETE` | Met à jour ou supprime une revue spécifique. |
| `/dishes` | `GET`/`POST` | Gère la liste et la création de plats. |
| `/favorites` | `POST` | Ajoute un restaurant aux favoris (`{restaurant_id: X}`). |
| `/favorites/<int:id>` | `DELETE` | Supprime le restaurant `<int:id>` des favoris de l'utilisateur. |
| `/menus` | `GET` | Récupère tous les menus ou filtre par `?restaurant_id=X`. |

-----

## 🔒 Authentification et Sécurité

Le système utilise l'authentification par **Session/Cookie**.

| Endpoint | Description |
| :--- | :--- |
| `/login` | **`POST`** : Connecte un utilisateur (Session). Retourne l'objet utilisateur. |
| `/logout` | **`DELETE`** : Déconnecte l'utilisateur (supprime la session). |
| `/check_session` | **`GET`** : Vérifie la session de l'utilisateur et retourne les données de l'utilisateur connecté. |
| `/login/google` | **`POST`** : Gère l'authentification avec un jeton Google (nécessite une configuration OAuth côté client). |
| `/current_user` | **`GET`** : Retourne l'utilisateur actuellement connecté par l'ID de session. |


## 🧑‍💻 Modèles de Données

Le backend s'appuie sur la structure de modèles SQLAlchemy suivante :

  * **`FoodUser`** (Utilisateurs)
  * **`Restaurant`**
  * **`Menu`**
  * **`Dish`** (Plat)
  * **`Review`** (Critique)
  * **`Favorite`** (Relation entre `FoodUser` et `Restaurant`)
  * **`MenuDish`** (Table d'association entre `Menu` et `Dish`)

-----
