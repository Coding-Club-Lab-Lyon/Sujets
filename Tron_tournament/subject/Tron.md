# Tron Battle – Sujet de Projet

## 🎮 Contexte

Le **Tron Battle** est une variante multijoueur inspirée du film *Tron* et de son célèbre jeu de moto-lumière.  
Chaque joueur contrôle une moto qui avance en continu sur une grille. À chaque "tick" du serveur :

- La moto avance d’une case dans la direction actuelle.
- Le joueur peut choisir de tourner à gauche, aller tout droit ou tourner à droite.
- Chaque moto laisse une **traînée** derrière elle (occupant les cases traversées).
- Si une moto une traînée (y compris la sienne), elle meurt.
- La partie continue jusqu’à ce qu’il ne reste qu’un survivant (ou aucun).

L’objectif est donc de développer un **algorithme** capable de survivre et, si possible, de gagner contre les autres bots.

---

## 🖥️ Communication avec le serveur

Le serveur Tron (en C++/Qt) gère la simulation et communique avec les clients via un protocole binaire.  
Pour simplifier l’utilisation de ce protocole, un **wrapper Python** est fourni : `tron_wrapper.py`.

Il vous permet de vous connecter facilement au serveur, de recevoir l’état du jeu et d’envoyer vos commandes.

---

## 📦 Le wrapper `TronClient`

Le fichier `tron_wrapper.py` contient la classe **`TronClient`**.  
Elle encapsule toute la logique réseau et expose une API simple pour écrire des votre algorithme.

### Méthodes principales

- `play_loop(callback)` : boucle principale qui appelle `callback(client, grid, me)` à chaque tick.
- `rotate_left()` : tourne à gauche.
- `rotate_right()` : tourne à droite.
- `stay_straight()` : continue tout droit.
- `get_grid()` : retourne la grille de jeu sous forme de liste 2D.
- `get_players()` : retourne la liste des joueurs avec leur état.
- `get_me()` : retourne les infos sur **votre moto** (`id`, `x`, `y`, `dir`, `alive`).
- `is_alive()` : indique si votre moto est encore en vie.

---

### Lancer le serveur

Pour lancer le serveur afin de tester votre bot il suffit de lancer la commande suivante

```./tron_battle -s 40 40 -d y -f game.conf
```

Bien entendu vous pouvez modifier les paramètres si ça vous amuse mais notez bien que le servuer sera lancé
dans ces condition lors du tournois.

Bonne chance a tous 