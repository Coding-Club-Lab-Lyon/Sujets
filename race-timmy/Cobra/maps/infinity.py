"""
Infinity Track - Figure-8 circuit where the car crosses through the middle
"""

import numpy as np
import math


def create_infinity_track():
    """
    Create a figure-8 (infinity) track using a parametric lemniscate curve.
    Walls are stored as alternating left/right pairs for proper rendering.

    Returns (walls, checkpoints, spawn_pos, spawn_angle).
    checkpoints is an ordered list — car must cross each in sequence to complete a lap.
    The last checkpoint is the finish line.
    """
    walls = []
    road_width = 8
    half_width = road_width / 2

    # Parametric figure-8: x = a*sin(t), y = b*sin(2t)/2
    # Right loop: t in [0, π], Left loop: t in [π, 2π]
    # Crossing at origin when t = 0 and t = π
    a = 28
    b = 28

    # Angular gap at crossings — just wide enough for the road to pass through
    gap_t = 0.1

    segments = [
        (gap_t, math.pi - gap_t),                    # Right loop
        (math.pi + gap_t, 2 * math.pi - gap_t),      # Left loop
    ]

    for seg_start, seg_end in segments:
        n = 80
        left_points = []
        right_points = []

        for i in range(n):
            t = seg_start + (seg_end - seg_start) * i / (n - 1)

            # Curve point
            x = a * math.sin(t)
            y = b * math.sin(2 * t) / 2

            # Tangent direction
            dx = a * math.cos(t)
            dy = b * math.cos(2 * t)
            tlen = math.sqrt(dx**2 + dy**2)

            # Normal (perpendicular to tangent)
            nx = -dy / tlen
            ny = dx / tlen

            left_points.append(np.array([x + nx * half_width, y + ny * half_width]))
            right_points.append(np.array([x - nx * half_width, y - ny * half_width]))

        # Store walls as alternating left/right pairs (required by renderer)
        for i in range(n - 1):
            walls.append((left_points[i], left_points[i + 1]))
            walls.append((right_points[i], right_points[i + 1]))

    # Key positions on the figure-8 (from parametric curve):
    #   t=π/4  → upper-right (19.8, 14)
    #   t=3π/4 → lower-right (19.8, -14)
    #   t=5π/4 → upper-left  (-19.8, 14)
    #   t=7π/4 → lower-left  (-19.8, -14)
    #
    # Driving direction (increasing t, clockwise on both loops):
    #   Start/end (lower-right) → crossing → CP1 (upper-left) → CP2 (lower-left)
    #     → crossing → CP3 (upper-right) → Start/end

    ur_x = a * math.sin(math.pi / 4)   # ≈ 19.8
    ur_y = b * math.sin(math.pi / 2) / 2  # = 14

    # Checkpoints perpendicular to road at top/bottom of each loop
    cp1 = (np.array([-ur_x, ur_y - half_width]), np.array([-ur_x, ur_y + half_width]))   # top-left
    cp2 = (np.array([-ur_x, -ur_y - half_width]), np.array([-ur_x, -ur_y + half_width])) # bottom-left
    cp3 = (np.array([ur_x, ur_y - half_width]), np.array([ur_x, ur_y + half_width]))     # top-right
    finish = (np.array([ur_x, -ur_y - half_width]), np.array([ur_x, -ur_y + half_width])) # bottom-right

    checkpoints = [cp1, cp2, cp3, finish]

    # Spawn at start/finish (bottom-right of right loop), heading left
    spawn_pos = np.array([ur_x, -ur_y])
    spawn_angle = 180.0  # degrees, facing left

    return walls, checkpoints, spawn_pos, spawn_angle
