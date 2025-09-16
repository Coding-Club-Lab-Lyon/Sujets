
# Tron Battle - Serveur + GUI (Qt)

Serveur TCP + interface Qt tout-en-un pour un jeu type Tron/Snake.

## Flags CLI
- `-d y|n` : debug on/off
- `-s X Y` : taille de la map (deux entiers après `-s`), ex: `-s 64 48`
- `-f path/to/config.conf` : fichier de configuration

**Exemple** :
```
./tron_battle -d y -s 64 48 -f game.conf
```

## Fichier `.conf` (exemple)
```
tickrate : 1
start speed : 0.025
end speed : 0.25
auto kill : on
lenght : 125
maps : 1
```

- `tickrate` : ticks par seconde.
- `start speed` / `end speed` : cellules/seconde, interpole sur 5 minutes par paliers de 3s.
- `auto kill` : on/off — si off, on ignore collision avec sa propre traînée.
- `lenght` : tous les `lenght` ticks, la traînée s’allonge de 1 (on ne pop pas la queue).
- `maps` : envoi d’un snapshot complet de la carte tous les `maps` ticks (pas de delta pour V1).

## Build (Qt5 ou Qt6)
Prerequis : Qt (Widgets, Network), CMake >= 3.16, un compilateur C++17.
```
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build . -j
```

## Lancement
1. Démarrer l'app avec vos flags
2. Les clients se connectent (max 8)
3. Le lobby affiche les joueurs connectés. Cliquer **Start** pour lancer la partie.
4. La partie se joue côté serveur, wrap aux bords, traînées; quand il reste 1 joueur, le gagnant s'affiche (nom transmis au handshake).

## Protocole (binaire, little-endian)

### Messages
- `MSG_HELLO (0x0001)` C->S : nom du joueur (UTF-8, 32 octets max) + option id souhaité (0=auto)  
- `MSG_WELCOME (0x0002)` S->C : id assigné + paramètres de partie
- `MSG_INPUT (0x0003)` C->S : tournant (-1 gauche, 0 tout droit, +1 droite)
- `MSG_STATE (0x0004)` S->C : état complet (tick, carte W*H octets, états joueurs)
- `MSG_BYE (0x0006)` S->C : fin (mort/gagnant/fermeture)

### Framing
Chaque paquet commence par `MsgHeader { type, len, ver, reserved }` (8 octets), suivi du payload.
Toutes les valeurs en little-endian, structs packées.

Voir `src/Protocol.h` pour les structures.
