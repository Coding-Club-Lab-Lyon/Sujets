PImage background; //On prépare notre image
ArrayList<Orb> my_orbs; //On prépare notre tableau d'orbes
long time_counter;

void setup() //On initialise la fenêtre
{
  size(1200, 720); //On crée une fenêtre de 1200*720
  background = loadImage("resources/battle_background.png"); //On charge notre image
  my_orbs = new ArrayList<Orb>(); //On crée un tableau d'orbes
  time_counter = millis();
}

void draw() //On dessine dans la fenêtre
{
  clear(); //On se prépare à dessiner
  image(background, 0, 0); //On affiche notre image
  spawn();
  for (int i = 0; i < my_orbs.size(); i++) //Permet d'acceder a chacune de nos orbes préalablement crée
  {
    if (my_orbs.get(i).is_alive() == 0){
      my_orbs.get(i).move();
      my_orbs.get(i).display();
    }
    else{
      my_orbs.remove(i);
      i--;
    }
  }
}

void spawn() //Permet de gerer le temps pour faire apparaitre des orbes
{
  if (time_counter <= millis())
  {
    my_orbs.add(new Orb()); //Création d'une nouvelle orbes
    time_counter = millis() + 1000;
  }
}

void mousePressed() //On exécute la fonction lors du clic de la souris
{
  if (mouseButton == LEFT) { //Si on clique sur le bouton gauche
    for (int i = 0; i < my_orbs.size(); i++) //On vérifie pour chaque orbe si on a cliqué dessus
    {
      my_orbs.get(i).click();
    }
  }
}
