## Avant Tout

L'objectif de cet atelier est de vous faire découvrir les bases du langage C, mais aussi l'ambiance et la philosophie de la piscine à Epitech.



Vous allez devoir faire preuve de rigueur et de persévérance. Si vous bloquez sur un problème, ici on ne passe pas au suivant, on demande à son voisin de droite, celui de gauche et en face de soi, puis internet. Si vous n'avez toujours pas trouvé, c'est là qu'interviennent les **Cobras**.



### Règles :



- Les différents exercices doivent être réalisés sans utiliser aucune bibliothèque. Deux fonctions ont été créées pour vous assister :



```c

void print_char(char c);

void print_number(int number);

```



>:danger !icon:diamond-exclamation Elles ne sont pas disponibles pour chaque exercice (ce sera précisé pour chacun).



- Pour chaque exercice, nous attendons de vous une **fonction** respectant le prototype imposé. Vous devez donc le respecter, sinon vous ne serez pas corrigé par la moulinette.



- Il est important de respecter les noms de fichiers ainsi que les prototypes donnés. Pour chaque exercice, vous créerez un nouveau fichier .c portant le nom de l'exercice. Par exemple, pour un exercice my_print_name :



```bash

touch my_print_name.c

```

```c

void my_print_name(void);

```



### Moulinette

Comme c'est le cas tout au long de votre piscine Epitech, nous avons mis en place une moulinette qui vous corrige à des intervalles aléatoires. Vous serez prévenu quand elle passera.

Dans votre repo vous trouverez un script python appelé client.py qui vous permettras différentes action. Tout d'abord de vous register à la mouli:
```bash
python3 client.py --register
```
 Ainsi que de consulter les résultat de la dernière mouli sur vos exercices.
```bash
python3 client.py --result
```

- **La moulinette a toujours raison**.



- **Ne laissez pas de fonction main() dans vos fichiers**.



- **Effectuez des commits réguliers (à vous de trouver comment faire)**.


### Allons-y !



Maintenant que vous avez bien lu ce qui précède, il ne vous reste plus qu'à vous lancer.



**Bonne chance !**


## My_Print_Ascii



> **Fichier de rendu:**  `my_print_ascii.c`



### Sujet :

L'objectif de cet exercice est d'écrire une fonction qui affichera l'ensemble des caracrtère affichable de la table ascii.

> Pour cet exercice vous pouvez utiliser print_char

La fonction devra être prototypée de la façon suivante :



```c

void  my_print_ascii(void);

```



### Exemple :

Un appel de votre fonction devra afficher ces résultats :



```C
int main(void)
{
    my_print_ascii();
    return 0;
}
```

```txt
$> !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghij
   klmnopqrstuvwxyz{|}~
```



## My_Print_N_Ascii



> **Fichier de rendu:** `my_print_n_ascii.c`



### Sujet :

L'objectif de cet exercice est d'écrire une fonction qui affichera les n premiers caracrtère affichable de la table ascii.



Si il y a un problème la fonction doit s'arreter sans rien faire.

> Pour cet exercice vous pouvez utiliser print_char

La fonction devra être prototypée de la façon suivante :



```c
void my_print_n_ascii(int howMany);
```



### Exemple :

Un appel de votre fonction devra afficher ces résultats :



```C
int main(void)
{
    my_print_n_ascii(5);
    return 0;
}
```

```txt
$> !"#$%
```

```C
int main(void)
{
    my_print_n_ascii(-2);
    return 0;
}
```

```txt
$>
```

```C
int main(void)
{
    my_print_n_ascii(100);
    return 0;
}
```

```txt
$>
```



## My_Print_Revert



> **Fichier de rendu:** `my_print_revert.c`



### Sujet :

L'objectif de cet exercice est d'écrire une fonction qui affichera une string à l'envers.

> Pour cet exercice vous pouvez utiliser print_char

La fonction devra être prototypée de la façon suivante :



```c

void my_print_revert(char *toRevert);

```



### Exemple :

Un appel de votre fonction devra afficher ces résultats :



```C
int main(void)
{
    my_print_revert("codingclub");
    return 0;
}
```

```txt
$> bulcgnidoc
```



## My_Char_Replace



> **Fichier de rendu:** `my_char_replace.c`



### Sujet :

L'objectif de cet exercice est d'écrire une fonction qui renverra une chaine de caractère avec dans laquelle un caractère est remplacer par un autre à chaque apparition.

> Pour cet exercice vous pouvez utiliser print_char

La fonction devra être prototypée de la façon suivante :



```c

void my_char_replace(char *origin, char toFind, char toReplace);

```



### Exemple :

Un appel de votre fonction devra afficher ce résultats :



```C
#include <stdio.h>

int main(int ac, char **av)
{
    char str[] = "bienvenue à epitech !";
    printf("%s\n", my_replace_char(str, 'e', 'a'));
    return 0;
}
```

```txt
$> biavanua à apitach !
```

## My_Get_Char_Repeat



> **Fichier de rendu:** `my_get_char_repeat.c`



### Sujet :

L'objectif de cet exercice est d'écrire une fonction capable de compté le nombre d'occurence de caractère dans une string.



La fonction devra être prototypée de la façon suivante :



```c

int  my_get_char_repeat(char to_find, const char *to_search);

```



### Exemple :

Un appel de votre fonction devra afficher ces résultats :



```C
#include <stdio.h>

int main(void)
{
    char str[] = "bienvenue à epitech";
    printf("%d\n", my_get_char_repeat('e', str));
    return 0;
}
```

```txt
$> 4
```

```C
#include <stdio.h>

int main(void)
{
    printf("%d\n", my_get_char_repeat('e', NULL));
    return 0;
}
```
```txt
$> 0
```


## My_Absolute



> **Fichier de rendu:** `my_absolute.c`



### Sujet :

L'objectif de cet exercice est d'écrire une fonction qui renverra la valeur absolue d'un nombre passé en argument.

La fonction devra être prototypée de la façon suivante :



```c

int my_absolute(int number);

```



### Exemple :

Un appel de votre fonction devra afficher ces résultats :



```C
#include <stdio.h>

int main(void)
{
    printf("%d\n", my_absolute(5));
    return 0;
}

```

```txt
$> 5
```

```C
#include <stdio.h>

int main(void)
{
    printf("%d\n", my_absolute(-5));
}
```

```txt
$> 5
```


## My_Square



> **Fichier de rendu:** `my_square.c`



### Sujet :

L'objectif de cet exercice est d'écrire une fonction qui renverra un nombre au carré.

La fonction devra être prototypée de la façon suivante :



```c

int my_square(int number);

```



### Exemple :

Un appel de votre fonction devra afficher ces résultats :



```C
#include <stdio.h>

int main(void)
{
    printf("%d\n", my_square(5));
    return 0;
}
```

```txt
$> 25
```



## My_Little_Bistro



> **Fichier de rendu:** `my_little_bistro.c`



### Sujet :

L'objectif de cet exercice est d'écrire une fonction qui prend 3 argument :

- un premier nombre sous forme d'un int.

- un caractère qui représente un symbole d'opération (+, -, *, /, %) sous forme d'un char.

- un deuxieme nombre sous forme d'un int

Votre fonction doit appliquer l'opération donner par le caractère sur les deux nombres et renvoyer le résultat sous forme d'un int.

Si il y a un prbolème la fonction renvoi 0.



Voici donc son prototype :



```c

int my_little_bistro(int value1, char op, int value2);

```



### Exemple :

Un appel de votre fonction devra afficher ces résultats :



```C
#include <stdio.h>

int main(void)
{
    printf("%d\n", my_little_bistro(40, '+', 2));
    return 0;
}

```

```txt
$> 42
```

```C
#include <stdio.h>

int main(void)
{
    printf("%d\n", my_little_bistro(85, '/', 2));
    return 0;
}
```

```txt
$> 42
```

```C
#include <stdio.h>

int main(void)
{
    printf("%d\n", my_little_bistro(150, '%', 54));
    return 0;
}
```

```txt
$> 42
```
## My_Print_Square



> **Fichier de rendu:** `my_print_square.c`



### Sujet :

L'objectif de cet exercice est d'écrire une fonction qui prend 2 argument :

- un premier nombre sous forme d'un int > 1.

- le second sous la forme d'un caractère.

Votre fonction doit afficher un carré de coté de la taille du premier argument avec le caractère du second.

Si il y a un prbolème la fonction ne fait rien.

> Pour cet exercice vous pouvez utiliser print_char

Voici donc son prototype :

```c

void my_print_square(int size, char c);

```



### Exemple :

Un appel de votre fonction devra afficher ces résultats :



```C
int main(void)
{
    my_print_square(2, 'g');
    return 0;
}
```
```txt
$> gg
   gg
```

```C
int main(void)
{
    my_print_square(-2, 'g');
    return 0;
}
```

```txt
$>
```
## My_Average



> **Fichier de rendu:** `my_average.c`



### Sujet :

Pour cette exercice vous devez rendre une fonction qui prend en argument un pointeur sur une liste de nombre (int *) ainsi que sa taille. Vous devez renvoyer la moyenne de ses valeur sous form d'un float.



Voici donc son prototype :



```c

float my_average(int *grades, int count);

```



### Exemple :

Un appel de votre fonction devra afficher ces résultats :



```C
#include <stdlib.h>
int main(void)
{
    int list[5] = {10, 17, 6, 14, 20};
    printf("%f\n", my_average(list, 5));
    return 0;
}
```

```txt
$> 13.4
```

## My_Get_Words



> **Fichier de rendu:** `my_get_words.c`



### Sujet :

Cette exercice à pour but de print chaque mot présent dans une string, donc séparer par: ' ' ou '\t'. Avec un \n entre chaque mot.

> Pour cet exercice vous pouvez utiliser print_char

Voici donc son prototype :



```c

void my_get_words(char *sentance);

```



### Exemple :

Un appel de votre fonction devra afficher ces résultats :



```C
#include <string.h>

int main(void)
{
    char *str = "bienvenue                     à    epite ch";
    my_get_words(str);
    return 0;
}
```

```txt
$> bienvenue
   à
   epite
   ch
```

## My_Rotate_Aplha



> **Fichier de rendu:** `my_rotate_alpha.c`



### Sujet :

La consigne de cet exercice est de créer une fonction appelée "my_rotate_alpha" qui prend en entrée une chaîne de caractères. La fonction doit effectuer une rotation alphabétique sur chaque caractère de la chaîne. Chaque caractère sera décalé de sa position dans l'alphabet (a -> 0, b -> 1...). La rotation doit être circulaire, c'est-à-dire que si un caractère atteint la fin de l'alphabet, il doit revenir au début. Finalement. La fonction doit retourner la chaîne de caractères modifiée. Si l'un des caractères de la string n'est pas une lettre minuscule la fonction s'arrête.

Voici donc son prototype :



```c

void my_rotate_alpha(char *sentance);

```



### Exemple :

Un appel de votre fonction devra afficher ces résultats :



```C

#include <stdio.h>

int main(void)
{
    char str[] = "abcdefghijklmnopqrstuvwxyz";
    printf("%s\n", my_rotate_alpha(str));
    return 0;
}
```

```txt
$> acegikmoqsuwybdfhjlnprtvxz
```

## My_Sort



> **Fichier de rendu:** `my_sort.c`



### Sujet :

La fonction de cet exercice prend un premier argument: une liste de nombres entiers, et un second: le nombre d'entier. Cette dernière doit trier et affiché les nombres de la liste.
Les techniques de trie sont nombreuse nous vous conseillons le Bubble sort.

Voici donc son prototype :

> Pour cet exercice vous pouvez utiliser print_number

```c

void my_sort(int *nlist, int size);

```



### Exemple :

Un appel de votre fonction devra afficher ces résultats :



```C
int main(void)
{
    char list[6] = {-84, 42, -21, 21, -42, 84};
    my_sort(list, 6);
}
```

```txt
$> -84
   -42
   -21
   21
   42
   84
```
## My_Get_Value



> **Fichier de rendu:** `my_get_value.c`



### Sujet :

La fonction de cet exercice prend un premier argument: un dictionnaire, et un second: une clé dont vous devez retrouver et print la valeur.

Exemple de Dictionnaire:
```
"ville:Lyon,    pays:France, continent=europe"
```
Le format se traduit donc par une clé séparer par ':' ou '=' de sa valeur sans espace. Chacun des ses ensembles clé valeur sont séparer par des  ',', ' ' , '\t'.

> Pour cet exercice vous pouvez utiliser print_char

> Pour cet exercice vous pouvez utiliser print_char

Voici donc son prototype :
```c
void my_get_value(char *dictionary,  char *toFind);
```

### Exemple :

Un appel de votre fonction devra afficher ces résultats :


```C
int main(void)
{
    char str[] = "ville:Lyon,    pays:France, continent=europe";
    char str1[] = "pays";
    char str2[] = "Ville";

    my_get_value(str, str1);
    my_get_value(str, str2);
    return 0;
}
```

```txt
$> France
```