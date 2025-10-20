#🍽️ Woody Vert (Food Review API)

Ce projet est une API RESTful construite avec Flask pour gérer les utilisateurs, les restaurants, les menus, les plats et les revues associées. Il utilise SQLAlchemy pour la gestion de la base de données (SQLite en développement) et Flask-Bcrypt pour le hachage sécurisé des mots de passe.

🚀 Démarrage

Suivez ces étapes pour configurer et lancer l'API en mode développement.

1. Prérequis

Assurez-vous d'avoir Python 3.9+ installé.

2. Configuration de l'environnement

2.1. Cloner le dépôt et se placer dans le répertoire du serveur

git clone <URL_DU_DEPOT>
cd belony-projet-final-flask/server


2.2. Créer et activer l'environnement virtuel

Il est fortement recommandé d'utiliser un environnement virtuel pour isoler les dépendances.

# Création de l'environnement
python3 -m venv venv

# Activation de l'environnement (Linux/macOS)
source venv/bin/activate

# Activation de l'environnement (Windows - PowerShell)
# .\venv\Scripts\Activate


2.3. Installer les dépendances

Installez tous les packages nécessaires listés dans requirements.txt (ou installez-les directement si le fichier est manquant) :

pip install Flask Flask-SQLAlchemy Flask-RESTful Flask-Bcrypt python-dotenv Flask-Migrate Flask-CORS requests


3. Configuration des Variables d'Environnement

Le projet utilise le package python-dotenv pour charger les variables de configuration depuis un fichier .env.

Créez un fichier nommé .env à la racine du dossier server et ajoutez-y votre clé secrète :

# Fichier .env
SECRET_KEY=remplacez_ceci_par_une_cle_secrete_longue_et_aleatoire


4. Lancer l'API

Le script run.py se charge de créer la base de données SQLite (app.db) si elle n'existe pas, et de démarrer le serveur de développement.

python run.py


Vous devriez voir le message de confirmation indiquant que l'API est démarrée :

Base de données et tables créées (app.db).
...
 * Running on [http://127.0.0.1:5000](http://127.0.0.1:5000)


