# Race Timmy - Programming Challenge

## Introduction

Welcome to **Race Timmy**, an autonomous racing challenge where you'll program a self-driving car to navigate a race track using only sensor data!

Meet Timmy - a race car equipped with a state-of-the-art LIDAR sensor. Timmy can see the world around him, but he needs your help to make decisions. Your mission is to write the control algorithm that will guide Timmy safely around the track and complete a full lap.

## The Story

Timmy is competing in the Autonomous Racing League, where human drivers are replaced by clever algorithms. The car is equipped with a front-facing LIDAR sensor that provides distance measurements in a 90-degree arc. Using only this information, you must program Timmy to:

1. Navigate the track without crashing
2. Complete a full lap
3. Achieve the fastest possible time

## Technical Specifications

### LIDAR Sensor

The LIDAR (Light Detection and Ranging) sensor is mounted at the front of Timmy and provides distance measurements:

- **Field of View**: 90 degrees (-45° to +45° from the car's forward direction)
- **Resolution**: 1 degree (91 measurements total)
- **Range**: 0 to 50 units
- **Update Rate**: Real-time (every frame)

#### LIDAR Data Format

The sensor returns a list of 91 integers:
- `lidar_data[0]` = distance at -45° (far right)
- `lidar_data[45]` = distance at 0° (straight ahead)
- `lidar_data[90]` = distance at +45° (far left)

Values represent the distance to the nearest wall in that direction.

### Car Controls

You control Timmy through two parameters:

#### 1. Acceleration
- **Range**: -10.0 to 10.0
- **Negative values**: Braking
- **Positive values**: Acceleration
- **Zero**: Coast (friction will slow the car)

#### 2. Wheel Angle
- **Range**: -45.0° to 45.0°
- **Negative values**: Turn right
- **Positive values**: Turn left
- **Zero**: Straight ahead

### Physics Model

The simulation includes realistic car physics:

- **Maximum Speed**: 30 units/second
- **Friction**: Constant deceleration when not accelerating
- **Steering**: Only effective when the car is moving
- **Momentum**: The car maintains velocity and requires braking to slow down
- **Collision**: Hitting a wall stops the car and ends the attempt

## Your Task

### Objective

Implement the `control()` method in the `CarController` class to make Timmy complete a full lap around the track.

### File to Edit

`Participants/car_controller.py`

### Method Signature

```python
def control(self, lidar_data):
    """
    Args:
        lidar_data: List of 91 integers (distances to walls)
    
    Returns:
        tuple: (acceleration, wheel_angle)
            - acceleration: float [-10.0, 10.0]
            - wheel_angle: float [-45.0, 45.0]
    """
    # Your code here
    return acceleration, wheel_angle
```

### Requirements

1. **Input**: Your function receives `lidar_data` - a list of 91 distance values
2. **Output**: Return a tuple of (acceleration, wheel_angle)
3. **Goal**: Complete one full lap without crashing
4. **Bonus**: Achieve the fastest lap time possible

## Getting Started

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Running the Simulation

```bash
cd Participants
python main.py
```

### Controls

- **SPACE**: Pause/Resume the simulation
- **R**: Restart the race
- **ESC**: Quit

### Visual Feedback

- **Green lines**: LIDAR rays showing sensor readings
- **Blue car**: Timmy (turns red when crashed)
- **White line**: Start/finish line
- **Gray walls**: Track boundaries
- **Timer**: Current lap time (top left)

## Strategy Guide

### Basic Approach

1. **Read the sensors**: Extract relevant distance values from `lidar_data`
2. **Make decisions**: Determine if you need to turn, brake, or accelerate
3. **Return controls**: Send acceleration and steering commands

### Example: Simple Obstacle Avoidance

```python
def control(self, lidar_data):
    front = lidar_data[45]  # Distance straight ahead
    
    if front < 10:
        # Wall ahead - brake and turn
        return -5.0, 30.0
    else:
        # Clear ahead - accelerate
        return 8.0, 0.0
```

### Recommended Techniques

#### 1. Wall Following
Maintain a consistent distance from one wall:
```python
left_distance = lidar_data[70]
right_distance = lidar_data[20]

# Steer to balance distances
steering = (left_distance - right_distance) * 2.0
```

#### 2. Look Ahead
Use multiple sensor angles to anticipate turns:
```python
near_front = lidar_data[45]
far_left = lidar_data[80]
far_right = lidar_data[10]

# Predict upcoming turns
if far_left < far_right:
    # Left turn coming, prepare
    steering = -10.0
```

#### 3. Speed Control
Adjust speed based on situation:
```python
if front < 15:
    acceleration = 2.0  # Slow down
elif front > 30:
    acceleration = 10.0  # Speed up
else:
    acceleration = 5.0  # Maintain
```

#### 4. Smooth Steering
Avoid sudden changes:
```python
def __init__(self):
    self.previous_steering = 0.0

def control(self, lidar_data):
    target_steering = calculate_steering(lidar_data)
    
    # Smooth transition
    steering = 0.7 * self.previous_steering + 0.3 * target_steering
    self.previous_steering = steering
    
    return acceleration, steering
```

## Evaluation Criteria

### Primary Goal: Completion
- Successfully complete one full lap
- Cross the start/finish line without crashing

### Secondary Goal: Speed
- Minimize lap time
- Faster times indicate better algorithms

### Bonus Points
- Smooth driving (minimal steering changes)
- Efficient racing line
- Consistent performance across multiple runs

## Common Pitfalls

1. **Too Fast**: High speeds make steering difficult
2. **Late Reactions**: Look ahead, not just straight
3. **Overcorrection**: Smooth, gradual adjustments work better
4. **Ignoring Momentum**: Remember to brake before turns
5. **Single Sensor**: Use multiple LIDAR angles for better awareness

## Advanced Challenges

Once you've completed a basic lap:

1. **Optimize Lap Time**: Refine your algorithm for speed
2. **Racing Line**: Follow the optimal path through corners
3. **PID Controller**: Implement proportional-integral-derivative control
4. **Adaptive Speed**: Dynamically adjust speed based on track curvature
5. **Predictive Steering**: Anticipate turns several frames ahead

## Debugging Tips

### Visualization
- Watch the green LIDAR lines to see what Timmy sees
- Pause (SPACE) to examine sensor readings at specific moments

### Print Debugging
```python
def control(self, lidar_data):
    front = lidar_data[45]
    print(f"Front distance: {front}")
    # Your logic here
```

### Incremental Development
1. First: Make the car move forward
2. Second: Add basic obstacle avoidance
3. Third: Implement turning logic
4. Fourth: Optimize for speed

## Reference Implementation

A working solution is provided in `Cobra/car_controller.py`. This implementation uses a simple wall-following algorithm and can complete the track. Study it for inspiration, but try to develop your own approach!

## Submission

Your submission should include:
- Modified `car_controller.py` with your implementation
- Any additional helper functions or classes you created
- Comments explaining your strategy

## Resources

### Concepts to Research
- PID Control
- Sensor Fusion
- Path Planning
- Reactive vs. Predictive Control

### Python Tips
- Use `numpy` for efficient calculations
- Store state in `__init__` for memory between calls
- Test individual components before combining

## Good Luck!

Remember: The best algorithm isn't always the most complex. Sometimes simple, robust solutions outperform sophisticated ones. Start simple, test often, and iterate!

May the fastest code win! 🏁

---

**Race Timmy** - An educational project for learning autonomous vehicle control
