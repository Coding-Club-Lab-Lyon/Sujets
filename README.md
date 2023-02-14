# Banque de sujets Coding Club Lyon

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
Pour que les sujets se conforment aux besoin du Coding Club, j'ai ajouté des fonctionnalités au Markdown par défaut

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
```

Ce fichier sert à la génération de la page de couverture du sujet.

> Le dossier subject peut contenir d'autres documents comme des images qui sont insérées dans le fichier Markdown.

Le dossier du sujet doit aussi contenir les ressources données aux participants et une correction (et d'autres dossiers si besoin).
