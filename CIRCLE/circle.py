#!/usr/bin/env python3
import math
import sys

def print_circle(rad):
    for i in range((2 * rad)+1):
        for j in range((2 * rad)+1):
            dist = math.sqrt((i - rad) * (i - rad) + (j - rad) * (j - rad))
            if (dist > rad - 0.5 and dist < rad + 0.5):
                print("*",end="")
            else:
                print(" ",end="")
        print()

if len(sys.argv) == 1:
    print("Usage : ./circle [rayon]")
else:
    rad = int(sys.argv[1])
    print_circle(rad)
