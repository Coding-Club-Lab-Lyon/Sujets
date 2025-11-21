# Instructor Guide - Race Timmy

## Overview

Race Timmy is a 3D autonomous racing simulation designed for high school students learning Python. Students implement a control algorithm using LIDAR sensor data to navigate a race track.

## Quick Setup (5 minutes)

### 1. Installation
```bash
cd race-timmy
./install.sh
```

### 2. Test Reference Implementation
```bash
cd Cobra
python main.py
```

You should see a 3D simulation with a car completing the track automatically.

### 3. Verify Student Environment
```bash
cd ../Participants
python main.py
```

The car should appear but won't move (students need to implement the controller).

## Class Structure

### Recommended Timeline (2-3 hours)

**Introduction (15 min)**
- Explain autonomous vehicles and sensors
- Demo the reference implementation
- Show LIDAR visualization

**Exploration (15 min)**
- Students run reference implementation
- Examine `Cobra/car_controller.py`
- Run `test_lidar.py` to understand data format

**Implementation (60-90 min)**
- Students edit `Participants/car_controller.py`
- Iterative development: test, debug, improve
- Encourage experimentation

**Optimization (30+ min)**
- Students improve lap times
- Compare different approaches
- Discuss trade-offs

**Wrap-up (15 min)**
- Share solutions
- Discuss real-world applications
- Extension ideas

## Teaching Tips

### Key Concepts to Emphasize

1. **Sensor Data Processing**
   - Raw data → meaningful information
   - Multiple sensors provide context
   - Real-time decision making

2. **Control Systems**
   - Input (sensors) → Logic → Output (controls)
   - Reactive vs. predictive approaches
   - Feedback loops

3. **Physics & Constraints**
   - Momentum and friction
   - Steering only works when moving
   - Speed vs. control trade-off

4. **Iterative Development**
   - Start simple, add complexity
   - Test frequently
   - Debug with visualization

### Common Student Challenges

**Challenge 1: Car doesn't move**
- Solution: Check acceleration value is positive
- Tip: Start with `return 5.0, 0.0`

**Challenge 2: Immediate crash**
- Solution: Lower initial speed
- Tip: Add obstacle detection first

**Challenge 3: Erratic behavior**
- Solution: Add steering smoothing
- Tip: Use weighted average of old/new values

**Challenge 4: Can't complete lap**
- Solution: Implement wall-following
- Tip: Balance left and right sensor readings

**Challenge 5: Slow lap times**
- Solution: Increase speed on straights
- Tip: Vary acceleration based on front distance

## Differentiation Strategies

### For Struggling Students

1. **Provide scaffolding**
   - Show `example_strategies.py`
   - Start with `BasicAvoidance` strategy
   - Break problem into smaller steps

2. **Simplify the task**
   - Focus on completing lap (not speed)
   - Provide pseudocode
   - Pair programming

3. **Visual debugging**
   - Use pause feature (SPACE)
   - Print sensor values
   - Watch LIDAR rays

### For Advanced Students

1. **Optimization challenges**
   - Minimize lap time
   - Smooth driving (minimal steering changes)
   - Implement PID control

2. **Extensions**
   - Add multiple laps
   - Create new track shapes
   - Implement overtaking logic

3. **Research topics**
   - Real autonomous vehicle algorithms
   - Machine learning approaches
   - Sensor fusion techniques

## Assessment Options

### Formative Assessment
- Code review during implementation
- Debugging conversations
- Strategy explanations

### Summative Assessment Options

**Option 1: Completion-Based**
- 70%: Complete one lap
- 20%: Code quality and comments
- 10%: Explanation of approach

**Option 2: Performance-Based**
- 50%: Complete one lap
- 30%: Lap time (scaled)
- 20%: Code quality

**Option 3: Portfolio-Based**
- Working implementation
- Written explanation of algorithm
- Reflection on challenges and solutions

## Discussion Questions

### During Implementation
- "What information do you need to make a decision?"
- "How do you know if you're too close to a wall?"
- "What should happen when you see an obstacle ahead?"

### After Completion
- "How is this similar to real self-driving cars?"
- "What are the limitations of this approach?"
- "How would you handle a more complex track?"
- "What other sensors might be useful?"

### Real-World Connections
- Self-driving cars (Tesla, Waymo)
- Warehouse robots (Amazon)
- Drones and UAVs
- Mars rovers

## Extension Activities

### In-Class Extensions

1. **Track Design**
   - Students modify track shape in code
   - Create challenging sections
   - Share custom tracks

2. **Tournament**
   - Students compete for fastest lap
   - Bracket-style competition
   - Prizes for different categories

3. **Algorithm Comparison**
   - Test different strategies
   - Measure performance metrics
   - Analyze trade-offs

### Take-Home Projects

1. **Research Report**
   - How do real self-driving cars work?
   - Compare different sensor types
   - Ethics of autonomous vehicles

2. **Advanced Implementation**
   - Add machine learning
   - Implement path planning
   - Create multi-car simulation

3. **Creative Extension**
   - Different vehicle types
   - Weather effects
   - Obstacle avoidance scenarios

## Technical Notes

### System Requirements
- Python 3.8+
- OpenGL support (usually built-in)
- ~100MB disk space
- Works on Windows, Mac, Linux

### Common Installation Issues

**Issue: PyOpenGL not installing**
```bash
# Try with pip upgrade
pip install --upgrade pip
pip install PyOpenGL PyOpenGL-accelerate
```

**Issue: "No module named OpenGL"**
```bash
# Install system OpenGL libraries (Linux)
sudo apt-get install python3-opengl
```

**Issue: Display/graphics errors**
- Update graphics drivers
- Try without accelerate: `pip uninstall PyOpenGL-accelerate`

### Performance Tips
- Runs at 60 FPS on most systems
- Lower resolution if needed (edit main.py)
- Disable LIDAR visualization for speed

## File Reference

### Student Files
- `Participants/car_controller.py` - Main implementation file
- `Participants/main.py` - Game engine (don't modify)
- `Participants/test_lidar.py` - Testing utility
- `Participants/example_strategies.py` - Example approaches

### Reference Files
- `Cobra/car_controller.py` - Working solution
- `Cobra/main.py` - Same as Participants version

### Documentation
- `README.md` - Student-facing documentation
- `QUICKSTART.md` - Fast setup guide
- `subject/race-timmy.md` - Detailed specifications
- `Race-Timmy.pdf.md` - Comprehensive overview

## Grading Rubric

### Basic Rubric (100 points)

| Criteria | Points | Description |
|----------|--------|-------------|
| Code Quality | 20 | Clean, commented, organized |
| Basic Movement | 20 | Car moves and responds |
| Obstacle Avoidance | 20 | Avoids walls consistently |
| Lap Completion | 30 | Completes full lap |
| Optimization | 10 | Fast/smooth driving |

### Detailed Rubric (100 points)

**Implementation (50 points)**
- Correct use of LIDAR data (10)
- Logical control algorithm (15)
- Proper acceleration control (10)
- Proper steering control (15)

**Code Quality (20 points)**
- Clear variable names (5)
- Helpful comments (5)
- Organized structure (5)
- Follows Python conventions (5)

**Performance (20 points)**
- Completes lap (10)
- Lap time (5)
- Smooth driving (5)

**Documentation (10 points)**
- Explanation of approach (5)
- Comments in code (5)

## FAQ

**Q: How long does this take?**
A: 2-3 hours for most students to complete a lap. Advanced optimization can take longer.

**Q: What if students get stuck?**
A: Show `example_strategies.py`, encourage pair programming, or provide pseudocode.

**Q: Can this run on Chromebooks?**
A: Not directly. Consider using repl.it or similar cloud IDE with graphics support.

**Q: Is this suitable for beginners?**
A: Students should know basic Python (functions, lists, if/else). No prior robotics knowledge needed.

**Q: Can I modify the track?**
A: Yes! Edit the `_create_oval_track()` method in main.py.

**Q: How do I create a tournament?**
A: Students save their controllers, you run each one and record lap times.

## Support

For issues or questions:
1. Check the README.md
2. Review example_strategies.py
3. Examine the reference implementation
4. Test with test_lidar.py

## License & Sharing

This project is designed for educational use. Feel free to:
- Use in your classroom
- Modify for your needs
- Share with other educators
- Create derivative works

---

**Happy Teaching! 🏎️**

*Race Timmy - Making autonomous systems accessible and fun*
