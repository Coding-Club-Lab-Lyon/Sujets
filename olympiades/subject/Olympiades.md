Bienvenue aux Olympiades du Coding Club !

Aujourd'hui, nous vous proposons une compétition qui mettra à l'épreuve vos compétences en résolution de problèmes et en programmation. Vous serez confrontés à cinq exercices différents, et chaque exercice vous fournira une réponse spécifique à entrer dans l'ordinateur central pour obtenir un indice précieux.

<center>![](https://new.asterix.com/wp-content/uploads/2018/04/alb12-1-400x274.jpg)</center>

L'objectif est d'être le plus rapide à trouver tous les indices et à les combiner pour résoudre l'énigme finale. Vous devrez faire preuve de rapidité, de logique et de compétences en programmation pour réussir.

Préparez-vous à relever le défi et à montrer vos talents de codeur ! Que le meilleur gagne !

<center>![](https://new.asterix.com/wp-content/uploads/2018/04/alb12-2-400x442.jpg) </center>


!pagebreak


## I : Pollution

Dans une situation d'embouteillage, il est essentiel de prendre en compte les émissions de CO2 des véhicules présents sur la route.

Les différentes marques de voitures ont des niveaux d'émission variables, ce qui peut avoir un impact significatif sur la qualité de l'air et l'environnement.

Afin de mieux évaluer l'impact environnemental d'un embouteillage, il est nécessaire de calculer la quantité totale de CO2 émise par toutes les voitures sur une distance donnée.

<center>![](https://pbs.twimg.com/media/BvAYeK4IAAA372K.png) </center>

Vous disposez d'un fichier "embouteillage.txt" qui contient une liste des modèles de voitures présentes dans un embouteillage. Chaque marque de voiture a une valeur d'émission de CO2 en grammes par kilomètre associée.

- Renault: 15gCO2/km
- Peugeot: 16gCO2/km
- Citroen: 17gCO2/km
- Opel: 16gCO2/km
- Volkswagen: 18gCO2/km
- BMW: 20gCO2/km
- Toyota: 15gCO2/km
- Mercedes: 19gCO2/km

Votre tâche consiste à développer un programme qui permet de calculer la quantité totale de CO2 émise sur 1 km par toutes les voitures présentes dans l'embouteillage, en utilisant les données fournies dans le fichier.

Pour ce faire, vous pouvez commencer votre programme comme il suit :

```python
with open("embouteillage.txt") as file:
    content = file.readlines()

total_emission = 0

for line in content:
    # your code here
```

> Le total des émissions en gCO2 est votre clé pour obtenir un indice.

!pagebreak

## II : Optimisation

Dans le but de réduire l'impact environnemental des véhicules, il est crucial d'optimiser leur consommation de carburant et, par conséquent, de limiter les émissions de CO2.

<center>![](https://img.lemde.fr/2017/10/19/0/0/1288/845/664/0/75/0/9ca59e2_31277-segu1q.854nobhuxr.jpg) </center>

Une des approches pour atteindre cet objectif consiste à régler la fréquence du moteur de manière à obtenir une efficacité maximale.

Une formule mathématique spécifique permet de déterminer la fréquence optimale du moteur pour minimiser les émissions de CO2.

$\sigma(\alpha)=\sum_{d|\alpha}^{}d$

Dans cette formule, $\alpha$ est l'autonomie du moteur en mètres, et $\sigma(\alpha)$ est la somme de tous les diviseurs de $\alpha$.

Sachant que la moyenne de l'autonomie des moteurs de voitures est de **482 653 mètres**, votre tâche consiste à développer un programme qui permet de calculer la fréquence optimale du moteur pour minimiser les émissions de CO2.

> La fréquence du moteur est exprimée en tours par minute (tr/min) et est votre clé pour obtenir un indice.

!pagebreak

## III : Pollution sonore

La pollution sonore générée par les embouteillages peut avoir un impact négatif sur la santé et le bien-être des personnes environnantes.

Dans le but de limiter cette pollution, il est essentiel d'évaluer et de contrôler les niveaux sonores émis par les véhicules, notamment ceux des klaxons.

Une approche consiste à mesurer la différence entre les klaxons présents dans l'embouteillage en utilisant leur phonétique.

<center>![](https://p8.storage.canalblog.com/80/80/399779/86894257.gif) </center>

Vous êtes chargé de réduire la pollution sonore dans un embouteillage en mesurant la différence entre deux klaxons.

Vous disposez des enregistrements phonétiques suivants pour chaque klaxon :

- Klaxon 1 : "TuuuuUUuuuuuuutuuuuuuutuuuuuuuUUUUUUTUTTUUUUUUUUTttt"
- Klaxon 2 : "Pwoiiiiiiinnnnnnnnnnnnnnoiiiiiiiiiiiiiinnnnnnnnnnnnn"

Votre tâche consiste à développer un programme qui permet de calculer la différence entre les deux klaxons en cumulant les distances entre chaque lettre présente dans leur phonétique (on ne tient pas compte de la casse).

> La distance cummulée obtenue est votre clé pour obtenir un indice.

!pagebreak

## IV : GPS

Lorsque les automobilistes se retrouvent pris dans un embouteillage, il est essentiel de trouver les meilleurs itinéraires pour minimiser le temps de trajet.

En utilisant des informations sur les distances et les vitesses des différentes routes, un système de navigation GPS peut aider les conducteurs à choisir les chemins les plus rapides et efficaces pour atteindre leur destination.

<center>![](https://www.valeursactuelles.com/assets/uploads/2017/10/Capture-de%CC%81cran-2017-10-25-a%CC%80-17.01.37.png) </center>

Vous êtes responsable de développer un système de navigation GPS pour les automobilistes afin d'optimiser leur temps de trajet. Vous disposez d'un fichier "distances.txt" qui contient des lignes au format suivant :

```
<distance> <vitesse>
<distance> <vitesse>
<distance> <vitesse>
...
```

où :

`<distance>` représente la distance entre deux points en kilomètres (km).

`<vitesse>` indique la vitesse maximale autorisée sur cette route en kilomètres par heure (km/h).

Votre tâche consiste à développer un programme qui, en utilisant les informations fournies dans le fichier "distances.txt", détermine le temps minimum nécessaire pour atteindre l'objectif.

> Le temps en minutes tronqué à l'entier inférieur est votre clé pour obtenir un indice.

!pagebreak

## V : Suivi de consommation

Dans le cadre de l'amélioration de l'efficacité énergétique des véhicules, il est essentiel de pouvoir surveiller et analyser la consommation d'essence de manière régulière.

Cependant, certains logiciels embarqués dans les voitures sont protégés par des mots de passe chiffrés, ce qui limite l'accès aux fonctionnalités de suivi de consommation.

Dans cet exercice, vous êtes confronté au défi de déchiffrer un hash MD5 afin d'accéder au logiciel embarqué et installer un suivi de la consommation d'essence mensuel.

<center>![](https://www.affairesdegars.com/webroot/usr_img/3318283872/asterix.52350.jpg) </center>

Vous avez été chargé de débrider une voiture et d'installer un suivi de la consommation d'essence mensuel.

Cependant, le logiciel embarqué est protégé par un mot de passe chiffré en utilisant l'algorithme de hachage MD5. Le mot de passe chiffré est le suivant : b2afdf253f6c1391022115bbca0cd8b0.

Votre tâche consiste à développer un programme qui permet de déchiffrer ce mot de passe MD5 et d'accéder au logiciel embarqué.