#!/usr/bin/python3

import argparse

import cv2
import numpy as np


def error_handling(args):
    if args.start < 0:
        raise Exception("Bad start number (only positive value)")
    if args.end < args.start:
        raise Exception("Bad end number (end >= start)")
    if args.end > 127:
        raise Exception("Please args.end will be in the ascii table")


def generate_letter_score(char : str) -> int:
    if not char.isprintable():
        return 0
    # Initialisation d'une nouvelle image
    image = np.ones((16, 16, 3), dtype=np.uint8) * 255
    # Les paramètres pour le texte
    font = cv2.FONT_HERSHEY_SIMPLEX
    position = (0, 12)  # position du coin inférieur gauche du texte
    fontScale = 0.5  # taille de la police
    color = (0, 0, 0)  # couleur du texte en BGR (noir)
    thickness = 1  # épaisseur de la ligne en px
    # Ajouter le texte à l'image
    cv2.putText(image, char, position, font, fontScale, color, thickness, cv2.LINE_AA)
    # Calculer la moyenne de chaque pixel
    pixel_averages = np.mean(image, axis=2)
    # Faire la somme de toutes les moyennes
    return np.sum(pixel_averages)


def main() -> None:
    parser = argparse.ArgumentParser(prog='', description='Create a ')

    parser.add_argument("-s", "--start", default=0, type=int)
    parser.add_argument("-e", "--end", required=True, type=int)
    args = parser.parse_args()
    error_handling(args)
    start, end = args.start, args.end
    print(*sorted([chr(i) for i in range(start, end + 1) if chr(i).isprintable()], key=generate_letter_score), sep="")

if __name__ == "__main__":
    main()