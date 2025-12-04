# Tutoriel d'Intégration pour Développeurs - GSB Frais

## 1. Objectif

Ce document a pour but de guider les nouveaux développeurs dans l'installation, la configuration et le lancement du projet GSB Frais en environnement de développement local.

## 2. Prérequis

Avant de commencer, assurez-vous d'avoir les outils suivants installés sur votre machine :
- **Python** (version 3.8 ou supérieure recommandée)
- **Git** pour le contrôle de version

## 3. Procédure d'Installation

Suivez ces étapes pour mettre en place votre environnement de développement.

### a. Cloner le Dépôt

Ouvrez un terminal et clonez le projet depuis le dépôt Git :
```bash
git clone https://github.com/assadakh/gsb_frais
cd gsb_frais
```

### b. Créer un Environnement Virtuel

Il est recommandé d'utiliser un environnement virtuel Python pour isoler les dépendances du projet.

```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows
venv\Scripts\activate
# Sur macOS/Linux
source venv/bin/activate
```

### c. Installer les Dépendances

Le projet utilise des dépendances Python et JavaScript.

```bash
# Installer les paquets Python
pip install -r requirements.txt

```
**Note :** La dépendance `mysqlclient` est listée dans `requirements.txt` pour une éventuelle utilisation avec une base de données MySQL. Cependant, la configuration de développement par défaut utilise SQLite, vous n'avez donc pas besoin d'un serveur MySQL pour commencer.

### d. Configurer la Base de Données

La base de données utilisée pour le développement est SQLite.

```bash
# Créer les tables de la base de données
python manage.py migrate
```

### e. Peupler la Base de Données

Un script est fourni pour remplir la base de données avec un jeu de données initial.

```bash
# Exécuter le script de peuplement
python populate_db.py
```

## 4. Lancement de l'Application

Une fois l'installation terminée, vous pouvez lancer le serveur de développement Django.

```bash
python manage.py runserver
```

L'application sera alors accessible à l'adresse suivante : [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## 5. Exécution des Tests

Pour vous assurer que tout fonctionne correctement, vous pouvez lancer la suite de tests automatisés.

```bash
python manage.py test
```

## 6. Structure du Projet

- `gsb_frais/`: Répertoire principal du projet, contient les fichiers de configuration (`settings.py`, `urls.py`).
- `frais/`: Application Django principale du projet. C'est ici que se trouvent les modèles, les vues, les templates et les URLs spécifiques à l'application.
- `db.sqlite3`: Fichier de la base de données SQLite utilisé en développement.
- `populate_db.py`: Script pour insérer les données de base nécessaires au fonctionnement de l'application.
- `requirements.txt`: Liste des dépendances Python.
- `package.json`: Liste des dépendances JavaScript.
- `manage.py`: Utilitaire en ligne de commande de Django.
