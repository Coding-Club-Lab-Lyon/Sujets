class Orb
{
  int orb_size;
  int line_number;
  int position_x;
  int position_y;
  int speed;
  color orb_color;
  boolean clicked;
  
  Orb()
  {
    orb_size = int(random(25, 50)); //On choisit une orb_size au hasard
    int[] lines = {180, 300, 420, 540, 660}; //Les 5 valeurs possible pour position_y
    line_number = int(random(0, 5)); //On tire aléatoirement la ligne sur laquelle la zombitrouille va arriver
    position_x = 1250; //On le fait apparaitre en dehors de la fenêtre
    position_y = lines[line_number]; //On choisit la position verticale correspondant a son numéro de ligne
    orb_color = color(225, 127, 0); //La couleur orange
    speed = int(random(2, 5)); //On lui donne une vitesse au hasard entre 2 et 5
    clicked = false;
  }
  
  void display() //Permet d'afficher un cercle a la position de notre orbe
  {
    pushStyle(); //Permet de mettre en place l'apparence de ton orbe
    fill(orb_color); //Donne une couleur à ton cercle
    noStroke(); //On ne veut pas de contour sur le cercle
    circle(position_x, position_y, orb_size); //On affiche le cercle
    popStyle(); //Fin de l'affichage
  }
  
  void move() //Permet de déplacer l'orbe vers la gauche de l'écran
  {
    position_x -= speed;
  }
  
  int is_alive()
  {
    if (position_x < orb_size)
    {
      return 1;
    }
    if (clicked == true)
    {
      return 2;
    }
    return 0;
  }
  
  void click()
  {
    if (mouseX > position_x - orb_size && mouseX < position_x + orb_size
      && mouseY > position_y - orb_size && mouseY < position_y + orb_size)
    {
      clicked = true;
    }
    else
    {
      clicked = false;
    }
  }
}
