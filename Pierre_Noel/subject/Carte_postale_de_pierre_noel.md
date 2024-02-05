## I. Introduction

Pierre est un jeune dresseur, il sillonne le pays afin de pouvoir capturer tous les Pokémon et devenir le grand maître de la ligue. Un peu fatigué par toutes ses aventures, il a pour la première fois décidé de prendre des vacances pour les fêtes de Noël. Manquant d’inspiration, il a besoin de votre aide afin de créer la plus jolie et originale des cartes postales, dans le but de l’envoyer à tous ses proches.



!pagebreak
## II. Consignes

En cas de question, pensez à demander de l’aide à votre voisin de droite. Puis de gauche. Demandez enfin à un Cobra si vous êtes toujours bloqué(e).

Vous avez tout à fait le droit d’utiliser internet pour trouver des réponses ou pour vous renseigner

!pagebreak
## III. Préparez vos outils pour une carte postale miraculeuse

Pour réaliser la carte postale, vous utiliserez de l’HTML, du CSS et du PHP.

!pagebreak

## IV. Il est temps de se lancer dans une création artistique

###		a. Ecrivez vos plus belle paroles

Vous allez commencer par compléter votre fichier appelé index.php afin d’y mettre un peu d’HTML.
Dans un premier temps, vous pouvez donner un titre à votre page, ainsi que le contenu de votre lettre. Ces différentes zones de texte sont matérialisées par des balises telles que ```<title>, <h1> et <p>```. Vous devriez obtenir quelque chose qui ressemble à cela :

```

<!DOCTYPE html>
<html>
<head>
<title>Titre de votre page</title>
</head>
<body>

<h1>Titre de votre carte</h1>
<p>Contenu de votre message, soyez bavard !</p>

</body>
</html>

```

Pour tester le rendu de votre carte postale, il suffit de vous diriger sur votre navigateur puis accédez à l’adresse http://localhost/.

###		b. Décorez votre carte postale avec du style

Super ! Il y a du résultat, mais ce n’est pas très esthétique. Pour l’améliorer, vous compléterez le fichier qui s’appelle style.css. C’est ici que vont se trouver les modifications visuelles de votre page web.

Par la suite, il va falloir signaler à notre fichier index.php qu’il existe un fichier css. Il suffit de rajouter ces quelques lignes dans notre fichier php.

```

<!DOCTYPE html>
<html>
<head>
<title>Titre de votre page</title>
<link rel=”stylesheet” href=”style.css”/>
</head>
<body>

<h1>Titre de votre carte</h1>
<p>Contenu de votre message, soyez bavard !</p>

</body>
</html>

```

Maintenant que c’est bon, passez à votre fichier css et ajoutez votre première modification. Vous allez-vous occuper de vos titres et paragraphes. Par exemple, vous pouvez rajouter ce code :

```

h1 {
    font-size: 50px;
    font-weight: bolder;
    font-family: cursive;
}

```

Cela modifiera la taille, l’épaisseur et la famille de la police du titre h1. Ensuite, vous pouvez changer l’apparence des paramètres.

###		c. Montrez votre lieu de vacances

Ça commence à prendre forme ! Mais bon, avouez que le fond blanc ce n’est pas terrible! Et si vous montriez aux proches de Pierre un beau paysage ? À vous de choisir l’image !
Pour ajouter une image de fond, il suffira de rajouter dans votre .css l’url de ce que vous voulez afficher. Étant donné que vous voulez qu’elle fasse toute la page, il vous faudra l'ajouter dans le body.

```

body {
    background-image: url("https://www.wallpapertip.com/wmimgs/77-772959_christmas-wallpapers-hd-1920x1080-free-wallpapers-christmas-greetings.jpg");
}

```

###		d. Donnez vie à votre carte

Parfait, Pierre apprécie beaucoup le nouveau rendu ! Il suggère d’ajouter des petits détails afin de rendre notre carte bien plus vivante. D’après lui, il est nécessaire
d’utiliser hover pour modifier un élément de notre page lorsque vous passez le curseur dessus. Il vous invite à ajouter cette zone de code dans votre fichier .css

```
 h1:hover {
    font-size: 10px;
}
```

Surprise, quand vous passez votre curseur sur le titre de votre carte, il va réduire tout seul. Imaginez tout ce que vous allez pouvoir réaliser avec cela …

###		e. Enrichissez le style de votre carte

Vous avez désormais les bases et tout comme les grands artistes, vous allez devoir exprimer votre créativité. Pierre souhaite vous donner carte blanche sur le visuel, tant que celui-ci ressemble à une carte postale ! À vous de jouer !


## V. Ajoutez des pokémons à votre carte

Votre carte postale est maintenant une véritable œuvre d’art ! Cependant, Pierre trouve qu’il manque des pokémon.


###		a. Joyeux Noël et API New Year

Une API ? Mais qu’est-ce que c’est que cette bête-là ?
L'API peut être résumée à une solution informatique qui permet à des applications de communiquer entre elles et de s'échanger mutuellement des services ou des données.

###		b. Récupérez vos pokémons préférés

Vous allez réaliser une requête qui aura pour but de récupérer l’intégralité des données sur un pokémon choisi.
Pour pouvoir utiliser l’API, il va falloir utiliser le PHP. Rendez-vous dans le fichier index.php, et ajoutez en haut de votre code de nouvelles balises.

```

<?php
?>

```

C’est à l’intérieur que nous allons pouvoir écrire notre requête.
Maintenant il vous faut trouver quel serait celle dont vous avez besoin. Après quelques recherches vous devriez trouver celle-ci :

```
$pokemonName('NAME OR ID');

```

Vous avez donc besoin de lui donner soit le numéro dans le pokédex de pokémon qui vous intéresse, soit son nom en anglais.

```
<?php
$apiUrl = ‘https://pokeapi.co/api/v2/pokemon’;
$pokemonName = “pikachu”; 			// Ici on choisi pikachu
$request_url = url . ‘/’ . pokemon;

?>
```

Vous allez ensuite utiliser la fonction json_decode pour transformer les données reçues en tableau afin de les manipuler plus facilement.

```

$json = file_get_contents($apiUrl);
$data = json_decode($json, true);

```

Vous pouvez également récupérer son nom de cette manière :

```

$name_pkmn = json[“name”];

```

Pour tester une variable php, vous pouvez utiliser var_dump($LaVariableQueVousTestez). Cela interrompra votre code et marquera sa valeur.

Pour pouvoir afficher la photo directement sur votre page, il va falloir l’intégrer à votre code HTML. Toujours dans votre fichier index.php, vous allez devoir rajouter ce code à l’endroit que vous souhaitez :

```

<img src="<?php echo $sprite_pkmn; ?>" alt="Pokemon sprite">

```

###		c. Affichez des pokémons aléatoires

Super, l’image est bien affichée, c’est déjà pas mal du tout ! Par contre, Pierre possède énormément de Pokémon et il aimerait bien que sa carte change de photos et de pokémon au hasard pour éviter de les rendre jaloux.
C’est encore à vous de jouer ! Il va falloir trouver une solution pour qu’au lieu de rentrer vous-même le numéro ou le nom du Pokémon, il soit choisi de manière aléatoire.




Pour cela vous allez changer la variable pokémon en y assignant un nombre random :

```

$pokemonNumber = rand(0, 898);  // voici rand, c’est grâce à lui !

```

## V. Conclusion

Félicitations, vous avez terminé les étapes de la conception de la carte postale pour notre cher Pierre. C’est magnifique, voire même splendide. Il pense que sa famille va être ravie de recevoir une œuvre d’une telle qualité !

Malgré tout, vous pouvez toujours essayer d’atteindre la perfection en réalisant quelques bonus 😉
    • Affichez plus de détails sur le pokémon grâce à l’API
    • Envoyez la carte par mail
    • Rajoutez de la neige qui tombe !

Merci à vous et joyeux Noël !




