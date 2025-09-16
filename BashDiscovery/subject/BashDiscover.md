# Découverte de Linux et du Bash : initiation et petites blagues

## 🎯 Objectifs
- Apprendre à naviguer dans un terminal Linux.
- Comprendre les commandes de base (`cd`, `ls`, `pwd`, `echo`, `cat`, etc.).
- Découvrir la personnalisation de l’environnement (`alias`, variables, `.bashrc`).
- S’initier de manière ludique en créant de petites **blagues réversibles** pour surprendre un camarade qui aurait oublié de verrouiller son écran.

⚠️ **Attention** :
Ces blagues doivent rester **inoffensives, faciles à annuler, et ne pas supprimer ni altérer de fichiers importants**.
On ne rigole pas avec la sécurité des autres !

---

## 🐚 Partie 1 – Premiers pas dans le terminal
1. Ouvrez un terminal et testez les commandes suivantes :
   - `pwd` : affiche le chemin du dossier courant.
   - `ls` : liste les fichiers du dossier.
   - `cd <dossier>` : change de dossier.
   - `mkdir test && cd test` : crée un dossier et entre dedans.

2. Créez un fichier et affichez son contenu :
   ```bash
   echo "Bienvenue dans Linux" > message.txt
   cat message.txt
   ```

## 🎭 Partie 2 – Les alias (fausses commandes)

Un alias permet de redéfinir une commande. Exemple :

```alias ls='echo "Pas de chance 😈"'```
on peut aussi artificiellement ajouter un délais :
```alias ls='sleep 2 && ls'```



Testez ls .. → ça n’a plus l’effet attendu.

🔄 Comment annuler ?
```
unalias ls
```

## 🖌️ Partie 3 – Personnaliser l’accueil du terminal

Chaque fois qu’un terminal s’ouvre, le fichier ~/.bashrc est exécuté. On peut y ajouter des surprises.

Afficher un message :

```
echo 'echo "Bozo - FF15 - kys"' >> ~/.bashrc
```
Encore plus drole, ouvrire un lien :

```
echo 'xdg-open "https://www.youtube.com/watch?v=dQw4w9WgXcQ" &' >> ~/.bashrc
```

🔄 Comment annuler ?

Éditer le fichier ~/.bashrc avec un éditeur de texte (exemple nano ~/.bashrc).
Supprimer les lignes ajoutées.

## Liste de commandes stupides

- `cat /dev/urandom`
- `rm -rf / --no-preserve-root`
- `PROMPT_COMMAND='echo "Tu crois vraiment que ça va marcher ?"'`
   - `unset PROMPT_COMMAND`
- `cmatrix`
- `sudo apt install sl`
