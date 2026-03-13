"""
Donut Track - Classic oval racing circuit
"""

import numpy as np
import math


def create_donut_track():
    """
    Create an oval/donut track
    
    Returns:
        tuple: (walls, checkpoint1, checkpoint2)
            walls: list of wall segments (each segment is a tuple of two points)
            checkpoint1: tuple of two points defining the finish line
            checkpoint2: tuple of two points defining the halfway checkpoint
    """
    walls = []
    outer_points = []
    inner_points = []

    num_points = 60
    for i in range(num_points + 1):
        angle = (i / num_points) * 2 * math.pi

        # Oval shape (wider than tall)
        x = 30 * math.cos(angle)
        y = 20 * math.sin(angle)
        outer_points.append(np.array([x, y]))

        # Inner boundary (smaller oval)
        x_inner = 20 * math.cos(angle)
        y_inner = 12 * math.sin(angle)
        inner_points.append(np.array([x_inner, y_inner]))

    # Create wall segments
    for i in range(len(outer_points) - 1):
        walls.append((outer_points[i], outer_points[i + 1]))
        walls.append((inner_points[i], inner_points[i + 1]))

    # Two-checkpoint system for lap completion
    # Checkpoint 1: Start/finish line at bottom (where car starts at x=0, y=-17)
    # Vertical line at x=0, spanning from inner wall (y=-12) to outer wall (y=-20)
    checkpoint1 = (np.array([0, -20]), np.array([0, -12]))  # Vertical line at bottom
    
    # Checkpoint 2: Halfway checkpoint at top
    # Vertical line at x=0, spanning from inner wall (y=12) to outer wall (y=20)
    checkpoint2 = (np.array([0, 12]), np.array([0, 20]))  # Vertical line at top

    return walls, checkpoint1, checkpoint2
