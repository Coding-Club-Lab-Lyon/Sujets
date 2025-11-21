#!/usr/bin/env python3
"""
Car Controller - Student Implementation

Your mission: Make Timmy complete a full lap around the track!

Timmy is equipped with a LIDAR sensor that gives you distance measurements
in a 90-degree arc in front of the car.
"""


class CarController:
    """
    Controls the car based on LIDAR sensor data

    TODO: Implement the control() method to drive Timmy around the track!
    """

    def __init__(self):
        """
        Initialize your controller here

        You can store any variables you need between control() calls
        """
        # TODO: Add any initialization you need
        pass

    def control(self, lidar_data):
        """
        Control the car based on LIDAR sensor readings

        Args:
            lidar_data: List of 91 integers representing distances to walls
                       - Index 0 = -45 degrees (right side)
                       - Index 45 = 0 degrees (straight ahead)
                       - Index 90 = +45 degrees (left side)
                       - Values range from 0 (wall touching) to 50 (max range)

        Returns:
            tuple: (acceleration, wheel_angle)
                acceleration: float between -10 (brake) and 10 (full throttle)
                wheel_angle: float between -45 (turn right) and 45 (turn left) degrees

        Example:
            # Go straight at medium speed
            return 5.0, 0.0

            # Turn left while accelerating
            return 8.0, 20.0

            # Brake and turn right
            return -5.0, -15.0
        """

        # TODO: Implement your control logic here!
        #
        # Tips:
        # - lidar_data[45] tells you the distance straight ahead
        # - Compare left and right distances to stay centered
        # - Slow down when approaching walls
        # - Use smooth steering changes for better control

        # Default behavior: do nothing (car will coast)
        acceleration = 0.0
        wheel_angle = 0.0

        print(lidar_data)

        return acceleration, wheel_angle
