# Quick Start Guide - Race Timmy

## 5-Minute Setup

### 1. Install Dependencies

```bash
pip install pygame PyOpenGL PyOpenGL-accelerate numpy
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

### 2. Test the Reference Implementation

```bash
cd Cobra
python main.py
```

You should see a 3D racing simulation with a car (Timmy) driving around an oval track. The reference implementation will complete the lap automatically.

### 3. Start Your Implementation

```bash
cd ../Participants
```

Edit `car_controller.py` and implement the `control()` method:

```python
def control(self, lidar_data):
    # Your code here!
    # Example: go straight at medium speed
    return 5.0, 0.0  # (acceleration, wheel_angle)
```

### 4. Run Your Code

```bash
python main.py
```

### 5. Iterate and Improve

- Watch how Timmy behaves
- Adjust your algorithm
- Try to complete the lap
- Optimize for speed!

## Controls

- **SPACE**: Pause/Resume
- **R**: Restart
- **ESC**: Quit

## Quick Tips

1. Start with simple logic: "if wall ahead, turn"
2. Use `lidar_data[45]` for straight-ahead distance
3. Compare left vs right sensors to stay centered
4. Slow down before turns
5. Watch the green LIDAR lines to debug

## Need Help?

Check out:
- `README.md` - Full documentation
- `subject/race-timmy.md` - Detailed challenge description
- `Cobra/car_controller.py` - Reference implementation

Happy racing! 🏎️
