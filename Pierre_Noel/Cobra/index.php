<!DOCTYPE html>
<html>
<head>
    <title>Carte de Noël de Pierre</title>
    <link rel="stylesheet" href="aesthetic.css">
</head>
<body>
    <h1>Joyeux Noël !</h1>
    <p>Cher ami,</p>
    <p>Je te souhaite un joyeux Noël et une nouvelle année pleine de Pokémon passionnants !</p>

    <?php
    $backgroundImage = "background-image.jpeg";
    $pokemonNumber = rand(1, 898);

    $apiUrl = "https://pokeapi.co/api/v2/pokemon/$pokemonNumber";
    $json = file_get_contents($apiUrl);
    $data = json_decode($json, true);

    $pokemonName = ucfirst($data['name']);
    $pokemonImage = $data['sprites']['front_default'];
    ?>

    <h2>Mon Pokémon préféré : <?php echo $pokemonName; ?></h2>
    <img src="<?php echo $pokemonImage; ?>" alt="<?php echo $pokemonName; ?>">

</body>
</html>
