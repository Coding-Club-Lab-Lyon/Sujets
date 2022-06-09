25 Juin 7486.

Le monde a connu de grandes avancées technologiques, mais la planète Terre voit disparaître ses jungles et déserts, ses vents et marées, ses lacs et océans, et sa lumière naturelle provenant du soleil.

<center>![](assets/temple.jpg) </center>

Les 12 signes du zodiaque, entités protégeant autrefois la Terre et dont chaque être humain est sous la protection, ont été capturés par les 4 éléments primordiaux venus se venger de l'humanité : l'air, le feu, la terre et l'eau.

<center>![](assets/zodiac.jpg) </center>

C'est alors qu'une dernière entité, le Signe du Serpentaire, 13e signe du zodiaque, défie les 4 éléments afin de libérer les 12 autres Signes. Vous êtes choisi pour l'aider à faire face à cette menace. Serez-vous de taille ?


!pagebreak


## I : Les préparatifs

Le Serpentaire vous donne 4 fichiers : Classes.py, Astroders.py, Enemies.py et Player.py.

Il a d’abord besoin que tu l’aides à rejoindre l’espace !

Pour le moment, le contenu du programme permet de créer une fenêtre, de créer le joueur, de pouvoir arrêter le programme avec la touche « Echap », et enfin d’afficher cette fenêtre avec une image en fond.

Pour tester cela, effectue la commande « python3 ./Astroders.py » pour démarrer le programme.

On va commencer par aller dans le fichier « Player.py » afin de compléter la classe « Player » :

```python
...
class Player(PlayerClass):
    def __init__(self):
        super().__init__()
        self.bullets = []
        self.bullet_cooldown = 0
        # code here
...
```

Ces lignes de codes permettent de créer une classe « Player » qui hérite de la classe « PlayerClass » déjà présente dans le fichier « Classes.py ». Hérité d'une classe signifie que tous les attributs et les méthodes de la classe parent appartiennent aussi à la classe enfant. Il nous montre aussi comment créer les attributs __bullets__ et __bullet_cooldown__. Maintenant à vous de créer les attributs _hp_, _x_ et _y_ qui auront respectivement pour valeur 3, 0 et 800.

Maintenant que cela est fait, nous allons devoir créer la méthode permettant l'affichage du joueur, de ses points de vie ainsi que ses projectiles (pour lancer un projectile il faut appuyer sur la touche espace). Pour cela il va falloir compléter le code suivant dans le fichier  « Player.py » :

```python
...
def display(self, game):
    self.costume = (self.costume + 1) % (len(self.costumes) * 5)
    for bullet in self.bullets:
        # add a line here
    hp_text = game.font.render("HP: %d" % self.hp, True, (255, 255, 255))
    # here too
    game.screen.blit(self.costumes[self.costume // 5], (self.x, self.y + self.idle_relative[1]))
...
```

Les lignes que vous avez à compléter doivent permettre l'affichage de chaque projectile et du texte des HP. Pour cela vous allez devoir utiliser la méthode blite de Pygame qui fonctionne que cela :

```python
screen.blit(element_to_display, (x, y))
```

Pour que le code que vous venez de faire soit exécuter il faut rajouter cette ligne dans le fichier « Astroders.py » :

```python
...
def display_game_elements(game):
    game.screen.blit(game.background, (0, 0))
    game.player.display(game) # this one
    pygame.display.update()
...
```

!pagebreak

Une fois que notre joueur et ces projectiles peuvent s'afficher, il va falloir permettre à notre joueur de se déplacer. Pour cela nous allons devoir créer des méthodes pour chacun des mouvements possibles du joueur à la suite du fichier « Player.py »

Tu peux remarquer qu'il existe déjà une méthode permettant le déplacement vers la gauche :

```python
...
def move_left(self):
	if self.x > 0:
    	self.x -= self.player_speed
...
```

Tu auras remarqué que le mouvement ne s'effectue que lorsque la position du joueur à supérieur à 0 sur l'axe x. Pour les autres mouvements tu vas devoir appliquer la même logique mais avec des valeurs différentes :

- move_right, ssi la position x du joueur est strictement inférieur à 1150.
- move_up, ssi la position y du joueur est strictement supérieur à 600.
- move_down, ssi la position y du joueur est strictement inférieur à 800

Maintenant que nous avons fait les méthodes associées à chacun des mouvements, nous devons gérer les évènements relatifs à ceux-ci affins que nous puissions déplacer le joueur avec les touches du clavier. Pour cela nous allons modifier la fonction « key_inputs » du fichier « Astroders.py ».

```python
...
def key_inputs(player):
	keys = pygame.key.get_pressed()
	if keys[K_ESCAPE]:
        exit()
    if keys[K_SPACE]:
        player.shoot()
    # code here
...
```

Il ne vous reste plus qu'à implémenter les cas qu'il manque. Tu peux maintenant relancer le programme, et appuyer sur la flèche de droite. Le Serpentaire devrait maintenant bouger !

!pagebreak

## II. À l'attaque !

Bravo ! Le Serpentaire peut maintenant se déplacer librement dans la fenêtre. Mais pour l'instant aucun ennemis en vue...

Pour faire apparaitre  les ennemis il vous suffit de rajouter la ligne suivante dans le fichier « Astroders.py » :

```python
...
def display_game_elements(game):
    game.screen.blit(game.background, (0, 0))
    game.player.display(game)
    game.enemies.display(game) # this one
    pygame.display.update()
...
```

Une fois cela fait, il va falloir permettre aux ennemis de se déplacer en rejoutant la ligne suivante :

```python
def update_game_elements(game):À
    game.clock.tick(60)
    game.player.update()
    game.enemies.update(game) # this one
```

Maintenant, il va falloir permettre aux ennemis d'attaquer. Pour cela on va créer une fonction dans le fichier « Astroders.py » :

```python
...
def attack_on_tick(game):
...
```

Cette fonction devra :
- incrémenter la valeur de _game.frame_ de 1
- ssi _game.frame_ est strictement supérieur à 50, alors _game.frame_ est remis à zéro et on appel _game.enemies.attack(game.screen)_

Une fois cela fait, il ne faut pas oublier d'appeler cette nouvelle fonction dans la boucle du jeu :

```python
...
while game.running:
    check_events(game)
    attack_on_tick(game) # here
    update_game_elements(game)
    display_game_elements(game)
...
```

!pagebreak

## III. Attention au choque

Mais vous arez remarqué que tes projectiles, comme ceux de tes ennemis n'atteignent leur cible. Pour qu'ils soient pris en compte, il va falloir créer une méthode __check_attacks__ dans le fichier « Enemies.py »

```python
...
def check_attacks(self, player):
    for attack in self.attacks:
        # code here
...
```

Maintenant à vous de compléter la boucle pour qu'à chaque _attack_, ces conditions soient vérifiées :
- ssi la coordonnée y de l'_attack_ est strictement supérieur à 850, alors on la supprime de la liste des attack (c'est-à-dire de _attacks_). Et on passe au tour de boucle suivant.
- ssi la condition suivante est vrai, alors un supprime l'_attack_ de la liste _attacks_. Et on passe au tour de boucle suivant.

```python
    if attack.x <= player.x + 100 and player.x <= attack.x + 50 and attack.y + 50 >= player.y and player.y + 100 >= attack.y:

```

Il vous suffit maintenant d'appeler la méthode que vous venez de créer dans le fichier « Astroders.py » :
```python
...
def check_hit_boxes(game):
    game.enemies.check_attacks(game.player)
...
while game.running:
    check_events(game)
    attack_on_tick(game)
    update_game_elements(game)
    check_hit_boxes(game)
...
```

!pagebreak

Vous pouvez maintenant démarrer à nouveau le programme, et le joueur devrait normalement perdre des points de vie lorsqu'une attaque l'atteint, mais ces attaques à lui n'ont toujours aucun effet !

En effet, nous ne vérifions pas que les projectiles du joueur atteignent leur cible. Pour cela on va compléter la boucle contenue dans la fonction __check_bullets__ du fichier « Enemies.py »

```python
...
 def check_bullets(self, width, bullets):
    for line_index, line in enumerate(self.enemies):
        for enemie_index, enemy in enumerate(line):
            if not enemy.alive:
                continue
            top = self.enemies_top + line_index * 80
            left = (self.lines_pos[line_index] + enemie_index * 80) % width
            right = (self.lines_pos[line_index] + enemie_index * 80 + 50) % width
            bottom = self.enemies_top + line_index * 80 + 50
            for bullet in bullets:
                # code here
...
```
Vous devrez ajouter les conditions suivantes :
- ssi la coordonnée y de _bullet_ est strictement inférieure à la valeur de _top_ __OU__ si cette coordonnée est strictement supérieur à la valeur de _bottom_, alors passer au prochain tour de boucle.
- ssi la coordonnée x de _bullet_ est supérieur ou égale à la valeur de _left_ __ET__ que qu'elle est aussi inférrieur ou égale à la valeur de _right_, alors on met l'attribue _alive_ de l'_enemy_ à False et on suprime cet élément du tableau des projectiles

Avant de relancer notre programme pour vérifier s'il fonctionne, n'oubliez pas d'appeler cette méthode dans le fichier « Astroders.py » :

```python
...
def check_hit_boxes(game):
    game.enemies.check_attacks(game.player)
    game.enemies.check_bullets(game.window_width, game.player.bullets)
...
```

## IV. Pour la victoire !

Maintenant que le joueur peut perdre des points de vie et détruire ses ennemis, il faut mettre en place les conditions de victoire et de défaite. Pour ce faire nous allons de nouveau modifier le fichier « Astroders.py » pour y ajouter la fonction suivante :

```python
...
def check_end_conditions(game):
...
```

À vous maintenant d'y implémenter les conditions suivantes :

- si le nombre de points de vie du joueur (_game.player.hp_) est inférieur ou  égale à 0 __OU__ si la valeur de _game.enemies.top_ est strictement supérieur à _game.window_height_ - 150, alors on met la variable _game.running_ à False.
- si la valeur de _game.enemies.count_enemies()_ est strictement égale à 0, alors met la variable _game.running_ à False et la variable _game.win_ à True.

Bien évidemment, on n'oubliera pas d'appeler notre nouvelle fonction dans la boucle su jeu :

```python
while game.running:
    check_events(game)
    attack_on_tick(game)
    update_game_elements(game)
    check_hit_boxes(game)
    display_game_elements(game)
    check_end_conditions(game) # don't forget me
```

Maintenant que tu peux gagner ou perdre, à toi de mettre en place des messages de victoire ou de défaite :

```python
...
while game.running:
    check_events(game)
    attack_on_tick(game)
    update_game_elements(game)
    check_hit_boxes(game)
    display_game_elements(game)
    check_end_conditions(game)
if game.win:
    # add a line here
else:
    # here too
...
```

Il vous suffit alors d'appeler la fonction _print()_ qui permet d'afficher un message :

```python
print("Hello you !")

output :
Hello you !
```

!pagebreak

## V. The end

Tout d’abord : bravo !

Maintenant, libre à toi de modifier le jeu selon tes désirs ! Tu as normalement dû apprendre certaines choses, et tu peux modifier à ta guise des parties du programme ou ajouter de nouvelles choses facilement comme du texte, de nouveaux projectiles, etc… Voici quelques exemples d’ajouts sympathiques ! :

- Faire en sorte que chaque élément ajoute un bonus selon son type, comme plus de PV, augmentation de la vitesse de déplacement, augmentation de la vitesse de tir, et un bonus aléatoire entre ces  trois-là
- De la musique et des sons.
- Un score et un écran de Game Over.
- Un menu
- De nouveaux ennemis ou personnages jouables.

N’hésite surtout pas à demander de l’aide à un Cobra qi tu as du mal à appliquer certaines de tes idées !