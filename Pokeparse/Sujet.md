# Pokeparse

**Le but est de charger tous les pokemons dans ton nouveau pokedex**
**Le parser doit etre capable de gerer casiment n'importe quel probleme de formatage**

## Explications

```
Professeur Chen commence à se faire un peu vieux et t'as donné des
listes de pokemons a recuperer mais n'as pas tout formaté correctement

Tu dois recuperer touts les pokemons repartis dans différentes bases de donnés 
```

## Language

Python3

## Contraintes
```
Orienté objet indispensable
Tous les pokemons doivent etre des objets de class avec 2 parametres:
    - Le nom du pokemon
    - Le type du pokemon

Il ne doit pas y avoir de doublon
Les noms / types des pokemons ne peuvent pas contenir de caractère special
Les noms / types des pokemon ne peuvent pas contenir de chiffre
Le nom et le type a obligatoirement plus d'un caractère
Le type du pokemon doit etre en Majuscule
Le nom du pokemon doit commencer par une Majuscule et le reste en minuscule
```

## Example

Pokemon a ajouter:
```
nom: test
type: hydro
```

Resultat:
```
pokemon.name: Test
pokemon.type: HYDRO
```

