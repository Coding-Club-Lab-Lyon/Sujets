# Race Timmy
## Autonomous Racing Challenge

---

## 🏎️ Project Overview

**Race Timmy** is an educational programming challenge where students implement an autonomous driving algorithm for a race car using LIDAR sensor data.

**Target Audience**: High school students learning Python  
**Difficulty**: Intermediate  
**Time Required**: 2-4 hours  
**Skills Practiced**: 
- Algorithm design
- Sensor data processing
- Control systems
- Physics simulation
- Problem-solving

---

## 📋 Challenge Description

### The Mission

Students must program "Timmy," an autonomous race car, to complete a full lap around a track using only LIDAR sensor data. The car is equipped with a front-facing LIDAR sensor that provides distance measurements in a 90-degree arc.

### Learning Objectives

1. Understand sensor-based control systems
2. Implement reactive algorithms
3. Work with real-time data processing
4. Apply physics concepts (velocity, acceleration, friction)
5. Debug and optimize algorithms iteratively

---

## 🔧 Technical Specifications

### LIDAR Sensor
- **Field of View**: 90° (-45° to +45°)
- **Resolution**: 91 measurements (1° intervals)
- **Range**: 0-50 units
- **Data Format**: List of 91 integers

### Car Controls
- **Acceleration**: -10 (brake) to +10 (throttle)
- **Steering**: -45° (right) to +45° (left)

### Physics Model
- Maximum speed: 30 units/second
- Realistic friction and momentum
- Collision detection
- Steering only effective when moving

---

## 📁 Project Structure

```
race-timmy/
├── README.md              # Main documentation
├── QUICKSTART.md          # 5-minute setup guide
├── requirements.txt       # Python dependencies
├── install.sh            # Installation script
│
├── Cobra/                # Reference implementation
│   ├── main.py           # Complete game engine
│   ├── car_controller.py # Working solution
│   └── run.sh            # Run script
│
├── Participants/         # Student workspace
│   ├── main.py           # Game engine (same as Cobra)
│   ├── car_controller.py # Student implementation (TODO)
│   ├── test_lidar.py     # LIDAR testing utility
│   └── run.sh            # Run script
│
└── subject/              # Challenge documentation
    └── race-timmy.md     # Detailed specifications
```

---

## 🚀 Getting Started

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or use the install script
./install.sh
```

### Testing the Reference

```bash
cd Cobra
python main.py
```

### Student Implementation

```bash
cd Participants
# Edit car_controller.py
python main.py
```

---

## 💻 Student Task

### File to Edit
`Participants/car_controller.py`

### Method to Implement

```python
class CarController:
    def control(self, lidar_data):
        """
        Args:
            lidar_data: List of 91 distances
        
        Returns:
            (acceleration, wheel_angle)
        """
        # TODO: Implement control logic
        return acceleration, wheel_angle
```

### Example Solution Approach

```python
def control(self, lidar_data):
    # Read sensors
    front = lidar_data[45]
    left = lidar_data[70]
    right = lidar_data[20]
    
    # Decide steering
    if left > right:
        wheel_angle = 10.0  # Turn left
    else:
        wheel_angle = -10.0  # Turn right
    
    # Decide speed
    if front < 10:
        acceleration = -5.0  # Brake
    else:
        acceleration = 8.0   # Go fast
    
    return acceleration, wheel_angle
```

---

## 🎮 Controls & Interface

### Keyboard Controls
- **SPACE**: Pause/Resume
- **R**: Restart race
- **ESC**: Quit

### Visual Elements
- **Blue car**: Timmy (red when crashed)
- **Green lines**: LIDAR rays
- **White line**: Start/finish
- **Gray walls**: Track boundaries
- **Timer**: Current lap time

---

## 📊 Evaluation Criteria

### Primary Goal (Required)
✓ Complete one full lap without crashing

### Secondary Goal (Optimization)
✓ Minimize lap time

### Bonus Points
- Smooth driving (minimal steering changes)
- Efficient racing line
- Consistent performance

---

## 🎓 Teaching Guide

### Recommended Progression

**Phase 1: Understanding (15 min)**
- Explain LIDAR concept
- Run reference implementation
- Discuss sensor data format

**Phase 2: Basic Movement (30 min)**
- Make car move forward
- Implement simple obstacle avoidance
- Test and debug

**Phase 3: Navigation (45 min)**
- Add turning logic
- Implement wall following
- Complete first lap

**Phase 4: Optimization (30+ min)**
- Improve lap time
- Smooth steering
- Advanced algorithms

### Discussion Topics

1. **Sensors in Real Life**: Self-driving cars, robots, drones
2. **Control Systems**: How do we make decisions from data?
3. **Trade-offs**: Speed vs. safety, simplicity vs. performance
4. **Debugging**: How to understand what the algorithm is "thinking"

### Extension Activities

- Add multiple tracks with different difficulty
- Implement racing against AI opponents
- Create a tournament with student solutions
- Add more sensors (rear LIDAR, speedometer)
- Implement machine learning approaches

---

## 🛠️ Technical Implementation

### Technologies Used
- **Python 3.8+**: Main language
- **Pygame**: Game loop and input handling
- **PyOpenGL**: 3D graphics rendering
- **NumPy**: Efficient numerical computations

### Key Features
- Real-time 3D visualization
- Accurate physics simulation
- Ray-casting LIDAR simulation
- Collision detection
- Lap timing system
- Pause/restart functionality

---

## 📚 Learning Resources

### Concepts Covered
- **Sensor Processing**: Converting raw data to decisions
- **Control Algorithms**: Reactive vs. predictive control
- **Physics**: Velocity, acceleration, friction, momentum
- **Geometry**: Angles, distances, ray casting
- **Optimization**: Iterative improvement

### Advanced Topics
- PID Control
- Path Planning
- Kalman Filtering
- State Machines
- Fuzzy Logic

---

## 🐛 Common Issues & Solutions

### Car doesn't move
→ Check that acceleration > 0

### Car crashes immediately
→ Start with lower speeds (acceleration = 3-5)

### Car spins out
→ Reduce steering angles, slow down before turns

### Erratic behavior
→ Add smoothing to steering changes

### Can't complete lap
→ Use wall-following strategy, look at reference

---

## 🏆 Success Stories

Students typically progress through these stages:

1. **First Movement** (5-10 min): Car moves forward
2. **Basic Avoidance** (15-30 min): Car avoids walls
3. **First Turn** (30-45 min): Car navigates a corner
4. **Lap Completion** (1-2 hours): Full lap without crashing
5. **Optimization** (2+ hours): Fast, smooth laps

---

## 📝 Assessment Rubric

| Criteria | Points | Description |
|----------|--------|-------------|
| Code Quality | 20 | Clean, commented, organized |
| Basic Movement | 20 | Car moves and responds to sensors |
| Obstacle Avoidance | 20 | Avoids walls consistently |
| Lap Completion | 30 | Completes full lap |
| Optimization | 10 | Fast lap time, smooth driving |

**Total**: 100 points

---

## 🔄 Variations & Extensions

### Easier Version
- Wider track
- Slower maximum speed
- More forgiving collision detection
- Simpler track shape (circle)

### Harder Version
- Narrower track
- Complex track shapes (S-curves, hairpins)
- Multiple laps required
- Time penalties for wall proximity
- Fuel/energy management

### Advanced Challenges
- Race against AI opponents
- Overtaking logic
- Weather effects (reduced sensor range)
- Damaged sensors (missing data)
- Multi-car coordination

---

## 📞 Support & Resources

### Included Files
- `README.md`: Complete user documentation
- `QUICKSTART.md`: Fast setup guide
- `subject/race-timmy.md`: Detailed specifications
- `test_lidar.py`: Sensor testing utility

### Reference Implementation
- `Cobra/car_controller.py`: Working solution
- Well-commented code
- Simple wall-following algorithm
- Can complete lap in ~20-30 seconds

---

## 🎯 Key Takeaways

Students will learn:

1. **Practical Programming**: Real-world application of code
2. **Sensor-Based Systems**: How robots "see" the world
3. **Algorithm Design**: Breaking problems into steps
4. **Iterative Development**: Test, debug, improve cycle
5. **Physics Application**: Concepts in action

---

## 📄 License & Usage

This project is designed for educational use in high school programming courses.

**Recommended for:**
- Computer Science classes
- Robotics clubs
- Programming competitions
- STEM workshops
- Self-directed learning

---

## 🏁 Conclusion

Race Timmy provides an engaging, hands-on introduction to autonomous systems and algorithm design. Students get immediate visual feedback, making it easy to understand the impact of their code changes.

The challenge scales from beginner-friendly to advanced optimization, ensuring students of all levels can participate and learn.

**Ready to race? Let's go!** 🏎️💨

---

*Race Timmy - Teaching autonomous systems through racing*
