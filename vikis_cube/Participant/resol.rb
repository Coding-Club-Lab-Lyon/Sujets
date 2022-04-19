
def rotate_up_until_free(ru, x, y)
  r = ru.get_rubic

  until r[4][y][x] != "1"
    ru.u
  end
end

def positionne_arrete_blanche(ru)
  r = ru.get_rubic

  for i in 0..3
    if r[1][0][1] == "1"
      rotate_up_until_free(ru, 1, 2)
      ru.f
      ru.f
      ru.d
      ru.r
      ru.f
      ru.fi
      ru.ri
    end
    if r[1][1][0] == "1"
      rotate_up_until_free(ru, 0, 1)
      ru.li
    end
    if r[1][1][2] == "1"
        rotate_up_until_free(ru, 2, 1)
        ru.r
    end
    if r[1][2][1] == "1"
      rotate_up_until_free(ru, 1, 2)
      ru.d
      ru.r
      ru.fi
      ru.ri
    end
    if r[5][0][1] == "1"
      rotate_up_until_free(ru, 1, 2)
      ru.f
      ru.f
    end
    ru.transform_left
  end
end

def croix_sup(ru)
  r = ru.get_rubic

  for i in 1..4
    if r[0][0][1] == r[0][1][1] and r[1][0][1] == r[1][1][1] and r[2][0][1] == r[2][1][1] and r[3][0][1] == r[3][1][1]
      break
    end
    ru.u
  end
  for j in 1..4
    for i in 1..2
      if r[1][0][1] == r[1][1][1] and r[3][0][1] == r[3][1][1]
        aretes_opp ru
      end
      ru.u
    end
    for i in 1..4
      if r[2][0][1] == r[2][1][1] and r[3][0][1] == r[3][1][1]
        aretes_adj ru
        return
      end
      ru.u
    end
    ru.transform_left
  end
end

def croix_blanche(ru)
  positionne_arrete_blanche ru
  croix_sup ru
end

def is_cible_correct?(r)
  r[4][2][2] == r[4][1][1] and r[1][0][2] == r[1][1][1] and r[2][0][0] == r[2][1][1]
end

def get_coin_cible(r)
  [r[4][1][1], r[1][1][1], r[2][1][1]]
end

def tourner_coins_jaunes(ru)
  r = ru.get_rubic

  until !is_jaune_correct? r
    ru.transform_right
  end
  for i in 0..3
    until is_jaune_correct? r
      serie_coins ru
    end
    ru.u
  end
end

def get_coin_haut(r)
  [r[4][2][2], r[1][0][2], r[2][0][0]]
end

def get_coin_bas(r)
  [r[1][2][2], r[5][0][2], r[2][2][0]]
end

def coins_blancs(ru)
  r = ru.get_rubic

  for i in 0..3
    if (get_coin_haut(r).include?(r[4][1][1]))
      while get_coin_bas(r).include?(r[4][1][1])
        ru.d
      end
      serie_coins ru
    end
    ru.transform_right
  end
  for i in 0..3
    until is_cible_correct? r
      if (get_coin_cible(r) & get_coin_bas(r)).length == 3 or (get_coin_cible(r) & get_coin_haut(r)).length == 3
        until is_cible_correct? r
          serie_coins ru
        end
      end
      ru.d
    end
    ru.transform_right
  end
end

def is_2couronne_correct?(r)
  for i in 0..3
    unless (r[i][1][0] == r[i][1][1]) and (r[i][1][1] == r[i][1][2])
      return false
    end
  end
  return true
end

def croix_jaune(ru)
  r = ru.get_rubic

  if r[4][0][1] == r[4][1][1] and r[4][1][0] == r[4][1][1] and r[4][2][1] == r[4][1][1] and r[4][1][2] == r[4][1][1]
    return
  end
  for i in 0..4
    if r[4][0][1] == r[4][1][1] and r[4][1][0] == r[4][1][1]
      serie_croix_jaune ru
      break
    elsif r[4][0][1] == r[4][1][1] and r[4][1][1] == r[4][2][1]
      serie_croix_jaune ru
      serie_croix_jaune ru
      break
    end
    ru.u
  end
  unless r[4][0][1] == r[4][1][1] and r[4][1][0] == r[4][1][1] and r[4][2][1] == r[4][1][1] and r[4][1][2] == r[4][1][1]
    serie_croix_jaune ru
    ru.u
    serie_croix_jaune ru
  end
end

def premiers_coin_bien_place(r)
  ([r[1][0][2], r[4][2][2], r[2][0][0]] & [r[1][1][1], r[4][1][1], r[2][1][1]]).length == 3
end

def coins_bien_places(r)
  unless ([r[1][0][2], r[4][2][2], r[2][0][0]] & [r[1][1][1], r[4][1][1], r[2][1][1]]).length == 3
    return false
  end
  unless ([r[1][0][0], r[4][2][0], r[0][0][2]] & [r[1][1][1], r[4][1][1], r[0][1][1]]).length == 3
    return false
  end
  unless ([r[0][0][0], r[4][0][0], r[3][0][2]] & [r[0][1][1], r[4][1][1], r[3][1][1]]).length == 3
    return false
  end
  unless ([r[2][0][2], r[4][0][2], r[3][0][0]] & [r[2][1][1], r[4][1][1], r[3][1][1]]).length == 3
    return false
  end
  return true
end

def is_jaune_correct?(r)
  r[4][2][2] == r[4][1][1]
end

