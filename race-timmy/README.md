# Race Timmy 🏎️

A 3D racing simulation where you program an autonomous car to complete a lap around a track using LIDAR sensor data.

## The Challenge

Timmy is a self-driving race car equipped with a LIDAR sensor. Your mission is to write the control logic that will guide Timmy safely around the track and complete a full lap in the shortest time possible!

## The Setup

### LIDAR Sensor
- 90-degree field of view (-45° to +45°)
- 91 distance measurements (one per degree)
- Range: 0 to 50 units
- Index 45 = straight ahead
- Index 0 = 45° to the right
- Index 90 = 45° to the left

### Car Controls
You control two parameters:
- **Acceleration**: -10 (full brake) to 10 (full throttle)
- **Wheel Angle**: -45° (turn right) to 45° (turn left)

### Physics
- Realistic car physics with momentum and friction
- Maximum speed: 30 units/second
- Steering only works when the car is moving
- Crash into a wall and you'll need to restart!

## Installation

```bash
# Install required packages
pip install -r requirements.txt
```

## How to Play

### For Participants

1. Edit `Participants/car_controller.py`
2. Implement the `control()` method in the `CarController` class
3. Run the simulation:
```bash
cd Participants
python main.py
```

### Controls
- **SPACE**: Pause/Resume
- **R**: Restart race
- **ESC**: Quit

## Your Task

Open `Participants/car_controller.py` and implement the `control()` method. This method receives LIDAR data and must return acceleration and steering values.

### Example Strategy

```python
def control(self, lidar_data):
    # Get distances
    front = lidar_data[45]  # Straight ahead
    left = lidar_data[70]   # 25° left
    right = lidar_data[20]  # 25° right
    
    # Simple logic: avoid walls
    if front < 10:
        # Wall ahead! Turn towards more open side
        if left > right:
            return 3.0, 30.0  # Turn left
        else:
            return 3.0, -30.0  # Turn right
    else:
        # Clear ahead, go fast!
        return 8.0, 0.0
```

## Tips for Success

1. **Start Simple**: Get the car moving first, then refine
2. **Use Multiple Sensors**: Don't just look straight ahead
3. **Smooth Steering**: Gradual turns are more stable than sharp ones
4. **Speed Management**: Slow down for turns, speed up on straights
5. **Wall Following**: Try to maintain consistent distance from walls
6. **Look Ahead**: Use sensors at different angles to anticipate turns

## Scoring

- Complete the lap without crashing
- Faster lap times = better score
- The timer shows your current lap time
- Try to beat your personal best!

## Advanced Challenges

Once you can complete a lap:
- Optimize for the fastest time
- Implement smooth cornering
- Add predictive steering based on upcoming turns
- Try PID control for more stable driving

## Reference Implementation

The `Cobra/` folder contains a working reference implementation using a simple wall-following algorithm. Use it for inspiration, but try to create your own solution!

## Troubleshooting

**Car doesn't move**: Make sure you're returning positive acceleration values

**Car crashes immediately**: Start with lower speeds and gentler steering

**Car spins out**: Reduce steering angles and slow down before turning

**LIDAR visualization**: Green lines show what the sensor sees - use this to debug!

Good luck, and may the fastest code win! 🏁
