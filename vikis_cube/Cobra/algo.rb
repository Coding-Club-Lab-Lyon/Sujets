require_relative "rubic.rb"
require_relative "resol.rb"

#ru = Rubic.new("chemin/vers/rubikscube.txt")
ru = Rubic.new("arrete_simple.txt")

ru.colorize true
ru.numberize true

############ Préparation du cube ############

def monter_face_blanche(ru)
  r = ru.get_rubic

  if r[4][1][1] == "1"
    return
  end
  if r[5][1][1] == "1"
    ru.transform_up
    ru.transform_up
    return
  end
  until r[1][1][1] == "1"
    ru.transform_left
  end
  ru.transform_up
end

############ Arrete blanche ############

def aretes_adj(ru)
  ru.r
  ru.u
  ru.ri
  ru.u
  ru.r
  ru.u
  ru.u
  ru.ri
  ru.u
end

def aretes_opp(ru)
  ru.r
  ru.u
  ru.ri
  ru.u
  ru.r
  ru.u
  ru.u
  ru.ri
  ru.transform_right
end

########### Coins Blancs ###############

def serie_coins(ru)
  ru.ri
  ru.di
  ru.r
  ru.d
end

########### 2e Couronne ###########

def deuxieme_couronne(ru)
  r = ru.get_rubic

  until is_2couronne_correct? r
    for i in 0..3
    if (r[1][0][1] == r[1][1][1] and r[4][2][1] == r[2][1][1]) or (r[1][1][2] == r[2][1][1] and r[2][1][0] == r[1][1][1])
        ru.u
        ru.r
        ru.ui
        ru.ri
        ru.ui
        ru.fi
        ru.u
        ru.f
     elsif (r[1][0][1] == r[1][1][1] and r[4][2][1] == r[0][1][1]) or (r[1][1][0] == r[0][1][1] and r[1][1][0] == r[1][1][1])
        ru.ui
        ru.li
        ru.u
        ru.l
        ru.u
        ru.f
        ru.ui
        ru.fi
      end
      ru.ui
    end
    ru.transform_right
  end
end

########### croix jaune ###########

def serie_croix_jaune(ru)
  ru.ri
  ru.ui
  ru.fi
  ru.u
  ru.f
  ru.r
end

######## Placement coins ##########

def placement_formule(ru)
  ru.u
  ru.r
  ru.ui
  ru.li
  ru.u
  ru.ri
  ru.ui
  ru.l
end

def coins_jaunes(ru)
  r = ru.get_rubic

  for i in 0..3
    if premiers_coin_bien_place(r)
      break
    end
    ru.transform_right
  end
  if premiers_coin_bien_place(r)
    placement_formule ru
    unless coins_bien_places(r)
      placement_formule ru
    end
  else
    placement_formule ru
    return coins_jaunes ru
  end
end

#############################

def algo(ru)
  monter_face_blanche ru
  print " ----  Monter Face Blanche ----\n", ru
  croix_blanche ru
  print " ----  Croix Blanche ----\n", ru
  coins_blanc ru
  print " ----  Face Blanche ----\n", ru
  # On retourn horizontalement le rubik
  ru.transform_down
  ru.transform_down
  deuxieme_couronne ru
  print " ----  2e Couronne ----\n", ru
  croix_jaune ru
  print " ----  Croix Jaune ----\n", ru
  croix_sup ru
  print " ----  Arrete Jaunes ----\n", ru
  coins_jaunes ru
  print " ----  Placements coins Jaunes ----\n", ru
  tourner_coins_jaunes ru
  print " ----  Fin ----\n", ru
end

algo ru
