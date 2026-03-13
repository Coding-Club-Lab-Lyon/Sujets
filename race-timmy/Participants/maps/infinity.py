"""
Infinity Track - Figure-8 circuit where the car crosses through the middle
"""

import numpy as np
import math


def create_infinity_track():
    """
    Create a figure-8 (infinity) track where the car crosses through the middle
    
    Returns:
        tuple: (walls, checkpoint1, checkpoint2)
            walls: list of wall segments (each segment is a tuple of two points)
            checkpoint1: tuple of two points defining the finish line
            checkpoint2: tuple of two points defining the halfway checkpoint
    """
    walls = []
    outer_points = []
    inner_points = []
    
    num_points = 80
    road_width = 8
    
    # Create figure-8 shape using parametric equations
    for i in range(num_points + 1):
        t = (i / num_points) * 2 * math.pi
        
        # Lemniscate (figure-8) parametric equations
        # Scale factor for size
        scale = 20
        
        # Basic lemniscate: x = a*cos(t)/(1+sin²(t)), y = a*sin(t)*cos(t)/(1+sin²(t))
        denom = 1 + math.sin(t) ** 2
        x = scale * math.cos(t) / denom
        y = scale * math.sin(t) * math.cos(t) / denom
        
        # Calculate tangent for perpendicular direction (for road width)
        # Derivative approximation
        dt = 0.01
        denom_next = 1 + math.sin(t + dt) ** 2
        x_next = scale * math.cos(t + dt) / denom_next
        y_next = scale * math.sin(t + dt) * math.cos(t + dt) / denom_next
        
        dx = x_next - x
        dy = y_next - y
        length = math.sqrt(dx**2 + dy**2)
        
        if length > 0:
            # Perpendicular direction (normalized)
            perp_x = -dy / length
            perp_y = dx / length
            
            # Outer and inner points
            outer_points.append(np.array([x + perp_x * road_width, y + perp_y * road_width]))
            inner_points.append(np.array([x - perp_x * road_width, y - perp_y * road_width]))
        else:
            outer_points.append(np.array([x, y]))
            inner_points.append(np.array([x, y]))
    
    # Create wall segments
    for i in range(len(outer_points) - 1):
        walls.append((outer_points[i], outer_points[i + 1]))
        walls.append((inner_points[i], inner_points[i + 1]))
    
    # Checkpoints for figure-8 track
    # Checkpoint 1: Start/finish at the right loop (x=15, y=0)
    # Horizontal line spanning the road width
    checkpoint1 = (np.array([15, -road_width]), np.array([15, road_width]))
    
    # Checkpoint 2: At the center crossing (x=0, y=0)
    # Diagonal line (45 degrees) spanning the road width
    diag_offset = road_width * 0.707  # cos(45°) = sin(45°) ≈ 0.707
    checkpoint2 = (np.array([-diag_offset, -diag_offset]), np.array([diag_offset, diag_offset]))

    return walls, checkpoint1, checkpoint2
