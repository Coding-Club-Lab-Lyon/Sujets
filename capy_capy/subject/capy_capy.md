## I. Introduction

Il était une fois, dans une forêt tropicale d'Amérique du Sud, un capybara nommé Capy. Capy était un animal curieux et aimait explorer les mystères de l'informatique. Un jour, il découvrit un ordinateur portable caché dans un tronc d'arbre et décida de l'utiliser pour apprendre le langage Python. Capy se lança dans un projet ambitieux : convertir des images en ASCII !

## II. Consignes
Avant de commencer cette introduction, voici les consignes techniques et les outils que vous allez utiliser :
1.  Langage de programmation : Python

2.  Bibliothèques nécessaires :
    1.	argparse : pour gérer les arguments passés lors du lancement du programme
    2.	opencv2 (OpenCV) : pour lire et manipuler les images

3.  Installation des bibliothèques :
		Vous pouvez installer les bibliothèques nécessaires en utilisant pip :
```sh
pip install opencv-python
```

4.	Environnement de développement :
		Utilisez un éditeur de code ou un environnement de développement intégré (IDE) de votre choix pour écrire et exécuter le code Python.

5.	Structure du projet :
		Créez un fichier ["main.py"] où vous écrirez le code pour la conversion d'image en ASCII.

Suivez ces consignes et vous serez prêt à commencer le projet de conversion d'images en ASCII avec l'histoire du capybara Capy.

## III. Argparse

Avant de commencer, Capy devait apprendre à utiliser "argparse", une bibliothèque Python pour gérer les arguments passés lors du lancement d'un programme. Pour ce faire, il créa un fichier ["main.py"] et importa "argparse" :

```py
import argparse

def main():
    parser = argparse.ArgumentParser(description="Convertir une image en ASCII")
    parser.add_argument("path=", required=True, type=str, help="Chemin vers l'image à convertir")
    args = parser.parse_args()

    print("Image à convertir :", args.image)

if __name__ == "__main__":
    main()
```

Avec ce code, Capy pouvait exécuter le programme en passant le chemin de l'image en argument :

```sh
python convert.py chemin/vers/image.jpg
```

