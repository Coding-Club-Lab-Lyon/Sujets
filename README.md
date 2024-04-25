# Banque de sujets Coding Club Lyon

## Process de création de sujets

### 1. Rédaction du sujet

Les sujets sont rédigés en Markdown, puis convertir en PDF par une GitHub Action.<br>
Le sujet est à placer à la racine du repo dans un dossier nommé `nom_du_sujet`.<br>
Chaque sujet doit contenir trois sous-dossiers :
- `subject` : Contient le sujet en Markdown, les ressources nécessaires et le fichier `data.txt`
- `Participants` : Contient les ressources à donner aux participants
- `Cobra` : Contient la correction du sujet

voici l'arborescence type d'un sujet :
```
.
├── nom_du_sujet
│   ├── subject
│   │   ├── data.txt
│   │   └── sujet.md
│   ├── Participants
│   │   └── ...
│   └── Cobra
│       └── ...
```   

Pour plus d'instructions sur la rédaction des sujets, voir la section [Rédaction de sujets](#rédaction-de-sujets)

### 2. Création d'une Pull Request

Une fois le sujet rédigé, il faut créer une Pull Request pour que le sujet soit ajouté à la banque de sujets.<br>
La Pull Request est à créer sur une branche nommée `feat/nom_du_sujet`.<br>
**Attention**: Aucun fork ne sera accepté, il faut créer une branche sur ce repo.<br>
Une fois la branche créée avec le sujet, il faut créer une Pull Request vers la branche `main` du repo.<br>
La Pull Request doit contenir les informations suivantes :
- Le nom du sujet
- Langage utilisé
- Auteur du sujet (Utiliser la partie `assignees` de la Pull Request)

Il est **interdit** de merge sa propre Pull Request.

### 2. Cycle de vie de la Pull Request

La Pull Request n'est pas décorative, elle doit être revue par un autre membre du Coding Club.<br>
Pour accompagner la Pull Request, il existe 4 labels :
- `Work in progress` : La Pull Request est en cours de rédaction
- `To Test` : La Pull Request est prête à être testée, elle sera review par un autre membre du Coding Club
- `To Reword` : La Pull Request a été testée et des modifications sont nécessaires
- `To Merge` : La Pull Request est prête à être mergée, le merge sera fait par un autre membre du Coding Club

### 3. Review de la Pull Request

La review de la Pull Request est faite par un responsable du Coding Club.<br>
Elle contient deux étapes :
- Vérification fonctionnelle du sujet
  - Le sujet marche
  - Les ressources sont bien placées
- Vérification syntaxique du sujet
  - Le sujet est bien rédigé
  - Le code est propre

Si la Pull Request n'est pas conforme, le reviewer doit ajouter le label `To Reword` et expliquer les modifications à apporter.<br>
Les modifications demandé seront décrites via la fonctionnalité `Review changes` de GitHub.

Si la Pull Request est conforme, le reviewer doit ajouter le label `To Merge` et laisser un commentaire pour indiquer que la Pull Request est prête à être mergée.

### 4. Merge de la Pull Request

Le merge de la Pull Request est fait par un responsable du Coding Club.<br>

Une fois le sujet mergé, la Pull Request est fermée et le sujet est ajouté à la banque de sujets.

## Rédaction de sujets

La nouvelle façon de rédiger les sujets du Coding Club est basée sur le [Markdown](https://www.markdownguide.org/cheat-sheet/)

Si vous n'êtes pas très a l'aise avec cette syntaxe ça s'apprend très vite ;)

### Règles
Pour que les sujets soit cohérents je vous demanderais de respecter les [bonnes pratiques générales](https://www.markdownguide.org/basic-syntax/)

Également, pour garder de la cohérence dans les sujets :

- **Il n'est pas nécessaire de créer une page de couverture**, elle sera générée automatiquement lors de la conversion.
- Utilisez des h2 (##) pour les titres des différentes parties du sujet puis des h3, h4, h5 hiérarchiquement selon l'importance de l'information.
- Utilisez le plus possible les éléments du Markdown (listes, tableaux...)
- Utilisez les blocs de code pour insérer du code dans le sujet (le code sera surligné automatiquement selon la syntaxe)

### Ajouts
Pour que les sujets se conforment aux besoins du Coding Club, j'ai ajouté des fonctionnalités au Markdown par défaut

- **Icônes :**
Vous pouvez insérer n'importe quelle icône [FontAwesome 6 Pro](https://fontawesome.com/search) en tappant `!icon:<id>`

Exemple : `!icon:triangle-exclamation` affiche un panneau "Attention" 

![](/.github/codingclub/assets/warning.png)

- **Boîtes d'info :**
Sur les sujets EPITECH, on voit souvent ces petites boîtes avec une information et un bonhomme moche.
On peut faire la même chose sur les sujets du Coding Club en faisant.
```
> Information ou conseil
```

Ces boîtes peuvent être déclinées en plusieurs couleurs avec "info", "success", "warning", "danger".

```
>:danger Une boîte rouge !
```

Vous pouvez aussi ajouter une petite icône avec votre boîte d'info :

```
>:warning !icon:triangle-exclamation **Attention:** Pensez à sauvegarder votre code !
```

![](/.github/codingclub/assets/info.png)

- **Sauts de page :**
Si vous avez besoin de forcer un saut de page vous pouvez utiliser !pagebreak.


- **Formules Mathématiques :**
Si vous avez besoin d'insérer des formules mathématiques, écrivez les entre des `$` en langage [LaTeX](https://latexeditor.lagrida.com/)

Exemple : `$\int_{a}^{b} f(x)dx = F(b) - F(a)$`

![](/.github/codingclub/assets/formula.png)

## Instancier un nouveau sujet
Si vous créez un sujet pour le Coding Club il vous suffit d'ajouter un dossier à la racine de ce repo.

Veuillez respecter cette architecture sinon il ne sera pas converti automatiquement :

```
.
├── nom_du_sujet
│   ├── subject
│   │   ├── data.txt
│   │   └── sujet.md
│   └── ...
```

Le sujet doit être un fichier \*.md dans le dossier "subject", il doit être accompagné d'un fichier "data.txt" structuré comme ceci :

```
NOM DU SUJET
1.0.0
Campus 
// stable // 
```

Ce fichier sert à la génération de la page de couverture du sujet.

> Le dossier subject peut contenir d'autres documents comme des images qui sont insérées dans le fichier Markdown.

Le dossier du sujet doit aussi contenir les ressources données aux participants et une correction (et d'autres dossiers si besoin).
