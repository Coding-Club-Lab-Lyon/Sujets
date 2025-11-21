# LIDAR Reference Guide

## Understanding the LIDAR Sensor

### Visual Representation

```
                    FRONT OF CAR
                         ↑
                    [45] 0°
                         |
              [55] 10°   |   [35] -10°
                    \    |    /
          [65] 20°   \   |   /   [25] -20°
                      \  |  /
            [75] 30°   \ | /   [15] -30°
                        \|/
                    ====CAR====
                        /|\
            [85] 40°   / | \   [5] -40°
                      /  |  \
          [90] 45°   /   |   \   [0] -45°
              LEFT       |       RIGHT
```

### Index to Angle Mapping

| Index | Angle | Direction | Common Use |
|-------|-------|-----------|------------|
| 0 | -45° | Far Right | Detect right turns |
| 10 | -35° | Right | Right side awareness |
| 20 | -25° | Right | Right wall distance |
| 35 | -10° | Front-Right | Anticipate right obstacles |
| 45 | 0° | **Straight Ahead** | **Main forward sensor** |
| 55 | +10° | Front-Left | Anticipate left obstacles |
| 70 | +25° | Left | Left wall distance |
| 80 | +35° | Left | Left side awareness |
| 90 | +45° | Far Left | Detect left turns |

## Quick Reference

### Formula
```python
angle_in_degrees = index - 45

# Examples:
# index 0  → -45° (right)
# index 45 →   0° (straight)
# index 90 → +45° (left)
```

### Common Sensor Groups

```python
# Forward sensors (for obstacle detection)
front_center = lidar_data[45]
front_left = lidar_data[50:60]
front_right = lidar_data[35:45]

# Side sensors (for wall following)
left_side = lidar_data[70]
right_side = lidar_data[20]

# Wide sensors (for turn detection)
far_left = lidar_data[85]
far_right = lidar_data[5]
```

## Example Usage Patterns

### 1. Basic Forward Detection
```python
front = lidar_data[45]
if front < 10:
    # Wall ahead!
    pass
```

### 2. Left vs Right Comparison
```python
left = lidar_data[70]   # 25° left
right = lidar_data[20]  # 25° right

if left > right:
    # More space on left
    wheel_angle = 20.0  # Turn left
else:
    # More space on right
    wheel_angle = -20.0  # Turn right
```

### 3. Multi-Sensor Average
```python
# Average of multiple left sensors
left_avg = (lidar_data[70] + lidar_data[80] + lidar_data[90]) / 3

# Average of multiple right sensors
right_avg = (lidar_data[20] + lidar_data[10] + lidar_data[0]) / 3
```

### 4. Scanning a Range
```python
# Check all forward sensors (30° cone)
forward_sensors = lidar_data[30:60]  # -15° to +15°
min_forward = min(forward_sensors)

if min_forward < 15:
    # Obstacle in forward cone
    pass
```

### 5. Finding Maximum Space
```python
# Find direction with most space
max_distance = max(lidar_data)
max_index = lidar_data.index(max_distance)
best_angle = max_index - 45

# Steer towards most open direction
wheel_angle = best_angle
```

## Distance Interpretation

### Distance Values
- **0-5**: DANGER! Wall very close
- **5-10**: Too close, need to turn
- **10-20**: Caution, prepare to turn
- **20-30**: Safe distance
- **30-50**: Plenty of space

### Example Decision Logic
```python
front = lidar_data[45]

if front < 5:
    acceleration = -10.0  # Emergency brake!
elif front < 10:
    acceleration = -5.0   # Brake hard
elif front < 20:
    acceleration = 2.0    # Slow down
elif front < 30:
    acceleration = 5.0    # Moderate speed
else:
    acceleration = 10.0   # Full speed ahead!
```

## Common Patterns

### Pattern 1: Wall Following
```python
# Stay centered between walls
left = lidar_data[70]
right = lidar_data[20]
balance = left - right
wheel_angle = balance * 2.0  # Proportional steering
```

### Pattern 2: Corridor Detection
```python
# Detect if in a straight corridor
left = lidar_data[70]
right = lidar_data[20]
front = lidar_data[45]

if abs(left - right) < 5 and front > 20:
    # Straight corridor, go fast!
    acceleration = 10.0
```

### Pattern 3: Turn Detection
```python
# Detect upcoming turn
far_left = lidar_data[85]
far_right = lidar_data[5]

if far_left < 10 and far_right > 20:
    # Left turn coming
    wheel_angle = 20.0
elif far_right < 10 and far_left > 20:
    # Right turn coming
    wheel_angle = -20.0
```

### Pattern 4: Obstacle Avoidance
```python
# Find clearest direction in front
left_front = lidar_data[55]
center = lidar_data[45]
right_front = lidar_data[35]

if center < 15:
    # Obstacle ahead, turn to clearer side
    if left_front > right_front:
        wheel_angle = 30.0
    else:
        wheel_angle = -30.0
```

## Debugging Tips

### Print Sensor Values
```python
def control(self, lidar_data):
    print(f"Front: {lidar_data[45]:.1f}")
    print(f"Left: {lidar_data[70]:.1f}")
    print(f"Right: {lidar_data[20]:.1f}")
    # Your logic here
```

### Visualize in Console
```python
def control(self, lidar_data):
    # Create simple bar chart
    front = lidar_data[45]
    bar = "█" * int(front / 2)
    print(f"Front: {bar} {front:.1f}")
    # Your logic here
```

### Use test_lidar.py
```bash
python test_lidar.py
```
This shows a visual representation of LIDAR data.

## Quick Tips

1. **Index 45 is your friend**: Always check straight ahead first
2. **Compare sides**: Use indices 20 and 70 for left/right balance
3. **Look ahead**: Use indices 5 and 85 to predict turns
4. **Average multiple sensors**: More stable than single readings
5. **Remember the formula**: `angle = index - 45`

## Practice Exercises

### Exercise 1: Print Key Sensors
```python
def control(self, lidar_data):
    print(f"Right: {lidar_data[20]}")
    print(f"Front: {lidar_data[45]}")
    print(f"Left: {lidar_data[70]}")
    return 0, 0  # Don't move yet
```

### Exercise 2: Find Minimum Distance
```python
def control(self, lidar_data):
    min_dist = min(lidar_data)
    min_index = lidar_data.index(min_dist)
    min_angle = min_index - 45
    print(f"Closest wall at {min_angle}° ({min_dist:.1f} units)")
    return 0, 0
```

### Exercise 3: Scan Sectors
```python
def control(self, lidar_data):
    left_sector = lidar_data[60:90]
    center_sector = lidar_data[30:60]
    right_sector = lidar_data[0:30]
    
    print(f"Left avg: {sum(left_sector)/len(left_sector):.1f}")
    print(f"Center avg: {sum(center_sector)/len(center_sector):.1f}")
    print(f"Right avg: {sum(right_sector)/len(right_sector):.1f}")
    return 0, 0
```

## Remember

- **91 total measurements** (indices 0-90)
- **Index 45 = straight ahead** (most important!)
- **Lower index = more right**
- **Higher index = more left**
- **Values are distances** (0 = touching wall, 50 = max range)

---

**Keep this reference handy while coding!** 📡
