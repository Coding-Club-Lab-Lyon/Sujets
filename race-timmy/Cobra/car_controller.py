#!/usr/bin/env python3
"""
Reference implementation of the car controller
This is what students need to implement
"""

import math


class CarController:
    """
    Controls the car based on LIDAR sensor data

    Students must implement the control() method
    """

    def __init__(self):
        """Initialize your controller here"""
        self.target_speed = 15.0
        self.previous_error = 0.0

    def control(self, lidar_data):
        """
        Control the car based on LIDAR sensor readings

        Args:
            lidar_data: List of 91 integers representing distances
                       Index 0 = -45 degrees (right)
                       Index 45 = 0 degrees (straight ahead)
                       Index 90 = +45 degrees (left)
                       Values are distances to nearest wall (0-50)

        Returns:
            tuple: (acceleration, wheel_angle)
                acceleration: float between -10 and 10
                wheel_angle: float between -45 and 45 degrees
                            negative = turn right, positive = turn left
        """

        # Simple wall-following algorithm
        # Get key sensor readings
        front = lidar_data[45]  # Straight ahead
        left = lidar_data[70]   # 25 degrees left
        right = lidar_data[20]  # 25 degrees right
        far_left = lidar_data[85]
        far_right = lidar_data[5]

        # Calculate steering based on wall distances
        # Try to stay centered between walls
        left_distance = (left + far_left) / 2
        right_distance = (right + far_right) / 2

        # Steering: aim to balance left and right distances
        balance = left_distance - right_distance
        wheel_angle = balance * 2.0  # Proportional control

        # Add correction based on front distance
        if front < 15:
            # Wall ahead, turn towards the more open side
            if left_distance > right_distance:
                wheel_angle += 20
            else:
                wheel_angle -= 20

        # Speed control: slow down for turns and obstacles
        if front < 10:
            acceleration = -5.0  # Brake hard
        elif front < 20 or abs(wheel_angle) > 20:
            acceleration = 2.0  # Slow down
        else:
            acceleration = 8.0  # Speed up

        # Clamp values
        wheel_angle = max(-45, min(45, wheel_angle))
        acceleration = max(-10, min(10, acceleration))

        return acceleration, wheel_angle
