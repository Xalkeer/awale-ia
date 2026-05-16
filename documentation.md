# Architecture du projet Awale (projet-ia)

Dans ce document, vous retrouverez toutes les informations nécessaire pour comprendre et utiliser ce projet liant les algorithmes MinMax
et MCTS au jeu d'Awale 

## Architecture  

- `awale.py`        : Gère toute la logique du jeu (état de la grille, règles, captures, etc)
- `player.py`       : implémentations basiques du joueur humain et du stupid bot
- `minMax.py`       : bot MinMax, renvoie un coup à jouer
- `mcts.py`         : bot MCTS, renvoie un coup à jouer 
- `game.py`         : orchestrateur de partie 
- `gui.py`          : afficahge du plateau et des éléments graphiques (Tkinter)
- `main.py`         : permet de lancer l'ui
- `simulate.py`     : Permet de lancer plusieurs parties sans interface graphique et de collecter des statistques

## Démarrage du projet

Pour cela, vous avez 2 options : 

- Lancer `main.py` pour démarrer l'interface graphique et jouer contre une IA ou un autre joueur humain.
- Lancer `simulate.py` pour exécuter plusieurs parties en ligne de commande et collecter des statistiques
