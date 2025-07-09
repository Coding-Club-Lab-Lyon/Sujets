from beaches import beaches
from math import sqrt
from itertools import permutations


def display_beaches():
    print("=== COMPARAISON DES ALGORITHMES ===")

    small_beaches = {k: beaches[k] for k in list(beaches.keys())[:8]}
    route_bf, dist_bf = brute_force_tsp(small_beaches)
    print(f"Force Brute: {route_bf}, {dist_bf:.2f} km")

    route_nn, dist_nn = nearest_neighbor_tsp(beaches)
    print(f"Plus Proche Voisin: {route_nn}, {dist_nn:.2f} km")


def calculate_distance(p1, p2):
    return sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def generate_all_routes(beach_list):
    return list(permutations(beach_list))


def brute_force_tsp(beaches_dict):

    beach_names = list(beaches_dict.keys())
    best_route = None
    best_distance = float('inf')
    pos = generate_all_routes(beach_names)

    tmp_dist = 0.0
    for elt in pos :
        for i in range(len(elt) - 1):
            tmp_dist += calculate_distance(beaches_dict[elt[i]], beaches_dict[elt[i+1]])
        if tmp_dist < best_distance:
            best_distance = tmp_dist
            best_route = elt
        tmp_dist = 0.0

    return best_route, best_distance

def nearest_neighbor_tsp(beaches_dict, start_beach=None):
    if start_beach is None:
        start_beach = list(beaches_dict.keys())[0]
    
    unvisited = list(beaches_dict.keys())
    route = [start_beach]
    unvisited.remove(start_beach)
    current = start_beach
    total_distance = 0.0

    while unvisited:
        city = None
        dist = float('inf')
        for elt in unvisited:
            tmp_dist = calculate_distance(beaches_dict[current], beaches_dict[elt])
            if tmp_dist < dist:
                dist = tmp_dist
                city = elt
        current = city
        total_distance += dist
        unvisited.remove(city)
        route.append(city)
        pass
    
    return route, total_distance

if __name__ == "__main__":
    display_beaches()