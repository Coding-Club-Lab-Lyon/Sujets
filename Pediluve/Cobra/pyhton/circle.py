#!/usr/bin/python3
import math
import sys

def draw_circle_outline(radius):
    if radius < 1:
        print("Radius trop petit :(")
        return

    for y in range(2 * radius + 1):
        row = ""
        for x in range(2 * radius + 1):
            distance = math.sqrt((x - radius) ** 2 + (y - radius) ** 2)
            if math.isclose(distance, radius, abs_tol=0.5):
                row += "*"
            else:
                row += " "
        print(row)

if len(sys.argv) != 2:
    print("Utilisation : python circle.py <rayon>")
else:
    try:
        radius = int(sys.argv[1])
        draw_circle_outline(radius)
    except ValueError:
        print("Le rayon doit être un nombre entier.")
