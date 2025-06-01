# Projet de Système d’Inventaire pour un RPG - Partie 2
Un projet de gestion d’inventaire pour un jeu de rôle (RPG), développé en Python et MySQL.

## Contributeur

- MEHDI EL MARDAH [000589290]
- HASSAN AMRI [000595737]
- David Poplawski[000587317]
- Dat Bui The [000546997]

## Installation

### Prérequis
- Python 3.x
- MySQL 8+
- `mysql-connector-python`

### Cloner le projet
```bash
git clone 
cd inventaire-rpg

###

Lancement du projet : 

1. Dans le fichier DataBase.py : 

Modifier dans la fonction connectToDatabase(self), la variable « user » et « password » par vos données.


2. Ouvrir un terminal et utiliser la commande : python3 loadFiles.py.
3. Ouvrir un second terminal et utiliser la commande :  mysql -u « votre pseudo » -p. Entrer le mot de passe.  Entrer le chemin vers le fichier schéma.sql en commençant par source.  
4. Lancer sur le premier terminal la commande : python3 MainGui.py

