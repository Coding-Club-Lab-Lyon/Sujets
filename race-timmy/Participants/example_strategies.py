#!/usr/bin/env python3
"""
Example Strategies for Race Timmy

This file contains several example approaches to controlling Timmy.
Copy one of these into car_controller.py as a starting point!
"""


# ============================================================================
# STRATEGY 1: Simple Forward (Beginner)
# ============================================================================
class SimpleForward:
    """Just go forward - will crash quickly but good for testing"""
    
    def control(self, lidar_data):
        return 5.0, 0.0  # Constant speed, no steering


# ============================================================================
# STRATEGY 2: Basic Obstacle Avoidance (Beginner)
# ============================================================================
class BasicAvoidance:
    """Turn away from obstacles"""
    
    def control(self, lidar_data):
        front = lidar_data[45]
        left = lidar_data[70]
        right = lidar_data[20]
        
        # If wall ahead, turn towards more open side
        if front < 15:
            if left > right:
                return 3.0, 30.0  # Turn left
            else:
                return 3.0, -30.0  # Turn right
        else:
            return 8.0, 0.0  # Go straight


# ============================================================================
# STRATEGY 3: Wall Following (Intermediate)
# ============================================================================
class WallFollower:
    """Try to maintain consistent distance from walls"""
    
    def control(self, lidar_data):
        front = lidar_data[45]
        left = lidar_data[70]
        right = lidar_data[20]
        
        # Try to balance left and right distances
        balance = left - right
        wheel_angle = balance * 2.0
        
        # Slow down if wall ahead
        if front < 10:
            acceleration = -5.0
        elif front < 20:
            acceleration = 3.0
        else:
            acceleration = 8.0
        
        return acceleration, wheel_angle


# ============================================================================
# STRATEGY 4: Multi-Sensor (Intermediate)
# ============================================================================
class MultiSensor:
    """Use multiple sensor angles for better awareness"""
    
    def control(self, lidar_data):
        # Sample multiple angles
        far_right = lidar_data[10]
        right = lidar_data[25]
        front_right = lidar_data[35]
        front = lidar_data[45]
        front_left = lidar_data[55]
        left = lidar_data[65]
        far_left = lidar_data[80]
        
        # Calculate average distances on each side
        left_avg = (far_left + left + front_left) / 3
        right_avg = (far_right + right + front_right) / 3
        
        # Steering based on side balance
        wheel_angle = (left_avg - right_avg) * 1.5
        
        # Speed based on front clearance
        if front < 8:
            acceleration = -8.0  # Emergency brake
        elif front < 15:
            acceleration = 2.0
        elif front < 25:
            acceleration = 5.0
        else:
            acceleration = 10.0
        
        # Clamp values
        wheel_angle = max(-45, min(45, wheel_angle))
        
        return acceleration, wheel_angle


# ============================================================================
# STRATEGY 5: Smooth Steering (Advanced)
# ============================================================================
class SmoothSteering:
    """Gradually change steering for smoother driving"""
    
    def __init__(self):
        self.previous_steering = 0.0
        self.previous_speed = 0.0
    
    def control(self, lidar_data):
        front = lidar_data[45]
        left = lidar_data[70]
        right = lidar_data[20]
        
        # Calculate target steering
        balance = left - right
        target_steering = balance * 2.5
        
        # Smooth transition (70% old, 30% new)
        wheel_angle = 0.7 * self.previous_steering + 0.3 * target_steering
        self.previous_steering = wheel_angle
        
        # Calculate target speed
        if front < 10:
            target_accel = -5.0
        elif front < 20:
            target_accel = 3.0
        else:
            target_accel = 8.0
        
        # Smooth speed changes
        acceleration = 0.8 * self.previous_speed + 0.2 * target_accel
        self.previous_speed = acceleration
        
        return acceleration, wheel_angle


# ============================================================================
# STRATEGY 6: Predictive (Advanced)
# ============================================================================
class Predictive:
    """Look ahead to anticipate turns"""
    
    def control(self, lidar_data):
        # Near sensors
        front = lidar_data[45]
        left = lidar_data[70]
        right = lidar_data[20]
        
        # Far sensors (for prediction)
        far_left = lidar_data[85]
        far_right = lidar_data[5]
        
        # Detect upcoming turns
        left_trend = far_left - left
        right_trend = far_right - right
        
        # Base steering on current position
        wheel_angle = (left - right) * 2.0
        
        # Adjust for predicted turns
        if left_trend < -5:  # Left wall approaching
            wheel_angle -= 10
        if right_trend < -5:  # Right wall approaching
            wheel_angle += 10
        
        # Speed control
        min_side = min(left, right)
        if front < 10 or min_side < 5:
            acceleration = -3.0
        elif front < 20:
            acceleration = 4.0
        else:
            acceleration = 9.0
        
        wheel_angle = max(-45, min(45, wheel_angle))
        return acceleration, wheel_angle


# ============================================================================
# STRATEGY 7: Adaptive Speed (Advanced)
# ============================================================================
class AdaptiveSpeed:
    """Adjust speed based on track curvature"""
    
    def control(self, lidar_data):
        front = lidar_data[45]
        left = lidar_data[70]
        right = lidar_data[20]
        
        # Calculate steering
        wheel_angle = (left - right) * 2.0
        
        # Estimate track curvature
        left_far = lidar_data[80]
        right_far = lidar_data[10]
        curvature = abs(left_far - right_far)
        
        # Adjust speed based on curvature and steering
        if curvature > 20 or abs(wheel_angle) > 25:
            # Sharp turn ahead
            target_speed = 4.0
        elif curvature > 10 or abs(wheel_angle) > 15:
            # Moderate turn
            target_speed = 6.0
        else:
            # Straight section
            target_speed = 10.0
        
        # Emergency brake for obstacles
        if front < 10:
            acceleration = -8.0
        else:
            acceleration = target_speed
        
        return acceleration, wheel_angle


# ============================================================================
# HOW TO USE THESE STRATEGIES
# ============================================================================
"""
To use one of these strategies:

1. Copy the class you want to try
2. Paste it into car_controller.py
3. Rename it to 'CarController'
4. Run main.py

Example:
    # In car_controller.py
    class CarController:  # <-- Keep this name!
        # Paste the strategy code here
        def control(self, lidar_data):
            # ... strategy code ...

Try them in order from simple to complex!
"""


# ============================================================================
# TESTING
# ============================================================================
if __name__ == "__main__":
    print("Example Strategies for Race Timmy")
    print("=" * 50)
    print("\nAvailable strategies:")
    print("1. SimpleForward - Just go straight")
    print("2. BasicAvoidance - Turn away from walls")
    print("3. WallFollower - Stay centered between walls")
    print("4. MultiSensor - Use multiple sensor angles")
    print("5. SmoothSteering - Gradual steering changes")
    print("6. Predictive - Anticipate upcoming turns")
    print("7. AdaptiveSpeed - Adjust speed for curves")
    print("\nCopy one into car_controller.py to try it!")
