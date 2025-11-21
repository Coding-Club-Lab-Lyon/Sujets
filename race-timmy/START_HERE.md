# 🏎️ Race Timmy - START HERE

## Welcome to Race Timmy!

This is a complete 3D autonomous racing simulation where you program a self-driving car using Python.

---

## ⚡ Quick Start (2 minutes)

### 1. Install
```bash
./install.sh
```

### 2. See It Working
```bash
cd Cobra
python main.py
```
Watch the reference implementation complete a lap!

### 3. Start Coding
```bash
cd ../Participants
# Edit car_controller.py
python main.py
```

---

## 📚 What Should I Read?

### 👨‍🎓 I'm a Student
1. **[QUICKSTART.md](QUICKSTART.md)** ← Start here (5 min)
2. **[README.md](README.md)** ← Full guide (15 min)
3. **[LIDAR_REFERENCE.md](LIDAR_REFERENCE.md)** ← Sensor help (10 min)

### 👨‍🏫 I'm an Instructor
1. **[INSTRUCTOR_GUIDE.md](INSTRUCTOR_GUIDE.md)** ← Teaching guide (20 min)
2. **[Race-Timmy.pdf.md](Race-Timmy.pdf.md)** ← Complete overview (30 min)
3. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** ← Project details (10 min)

### 🤔 I Just Want to Explore
1. **[VISUAL_GUIDE.txt](VISUAL_GUIDE.txt)** ← See what it looks like
2. **[PROJECT_MAP.txt](PROJECT_MAP.txt)** ← Project structure
3. **[INDEX.md](INDEX.md)** ← Complete file index

---

## 🎯 Your Mission

Program Timmy (the car) to complete a full lap around the track using only LIDAR sensor data!

### What You Get
- 91 distance measurements (LIDAR sensor)
- Real-time 3D visualization
- Realistic physics
- Immediate feedback

### What You Control
- Acceleration (-10 to +10)
- Steering (-45° to +45°)

### The Challenge
- Navigate the track
- Avoid walls
- Complete the lap
- Optimize your time!

---

## 📁 Project Structure

```
race-timmy/
├── 📖 Documentation (10 files)
│   ├── START_HERE.md ............... This file!
│   ├── QUICKSTART.md ............... 5-minute setup
│   ├── README.md ................... Main docs
│   ├── INSTRUCTOR_GUIDE.md ......... Teaching guide
│   ├── LIDAR_REFERENCE.md .......... Sensor reference
│   └── ... and more
│
├── 👨‍🎓 Participants/ (Your workspace)
│   ├── car_controller.py ........... EDIT THIS FILE
│   ├── main.py ..................... Run this
│   ├── example_strategies.py ....... 7 examples
│   └── test_lidar.py ............... Test utility
│
└── ✅ Cobra/ (Reference solution)
    ├── car_controller.py ........... Working solution
    └── main.py ..................... Run this to see it work
```

---

## 🎮 Controls

- **SPACE**: Pause/Resume
- **R**: Restart
- **ESC**: Quit

---

## 💡 Quick Tips

1. **Start Simple**: Make the car move first
2. **Use the Sensor**: Check `lidar_data[45]` for front distance
3. **Avoid Walls**: Turn when distance < 10
4. **Watch the Rays**: Green lines show what Timmy sees
5. **Iterate**: Test, debug, improve, repeat!

---

## 📊 What's Included

### Code
- ✅ Complete 3D game engine (466 lines)
- ✅ Reference implementation (77 lines)
- ✅ Student template (67 lines)
- ✅ 7 example strategies
- ✅ Testing utilities

### Documentation
- ✅ 10 comprehensive guides
- ✅ 2,700+ lines of documentation
- ✅ Code examples
- ✅ Visual aids
- ✅ Teaching materials

### Features
- ✅ 3D graphics (PyOpenGL)
- ✅ Realistic physics
- ✅ LIDAR simulation
- ✅ Visual debugging
- ✅ Lap timing
- ✅ Pause/restart

---

## 🎓 Learning Path

### Beginner (30-60 min)
1. Run reference implementation
2. Make car move forward
3. Add basic obstacle avoidance

### Intermediate (1-2 hours)
4. Implement wall following
5. Add speed control
6. Complete first lap

### Advanced (2+ hours)
7. Optimize lap time
8. Smooth steering
9. Advanced algorithms

---

## 🆘 Need Help?

### Code Not Working?
→ Check **[LIDAR_REFERENCE.md](LIDAR_REFERENCE.md)**
→ Try **[example_strategies.py](Participants/example_strategies.py)**
→ Run **[test_lidar.py](Participants/test_lidar.py)**

### Don't Understand LIDAR?
→ Read **[LIDAR_REFERENCE.md](LIDAR_REFERENCE.md)**
→ Check **[VISUAL_GUIDE.txt](VISUAL_GUIDE.txt)**

### Want Examples?
→ See **[example_strategies.py](Participants/example_strategies.py)**
→ Study **[Cobra/car_controller.py](Cobra/car_controller.py)**

### Teaching This?
→ Read **[INSTRUCTOR_GUIDE.md](INSTRUCTOR_GUIDE.md)**

---

## ✅ Installation Requirements

- Python 3.8+
- pip
- ~100 MB disk space

### Dependencies (auto-installed)
- pygame
- PyOpenGL
- numpy

---

## 🎉 Ready to Race?

### Students
```bash
./install.sh
cd Participants
python main.py
```
Then edit `car_controller.py` and make Timmy drive!

### Instructors
```bash
./install.sh
```
Then read `INSTRUCTOR_GUIDE.md`

---

## 📖 Complete File Index

See **[INDEX.md](INDEX.md)** for a complete guide to all files.

---

## 🌟 What Makes This Special?

- ✅ **Complete**: Everything included, nothing to add
- ✅ **Professional**: High-quality code and docs
- ✅ **Educational**: Designed for learning
- ✅ **Visual**: 3D graphics, not just text
- ✅ **Progressive**: Beginner to advanced
- ✅ **Documented**: 2,700+ lines of guides
- ✅ **Ready**: Use immediately in classroom

---

## 🏁 Let's Go!

Pick your path:

**Want to code right now?**
→ `./install.sh` → `cd Participants` → `python main.py`

**Want to understand first?**
→ Read **[QUICKSTART.md](QUICKSTART.md)**

**Want to see it working?**
→ `cd Cobra` → `python main.py`

**Want to teach this?**
→ Read **[INSTRUCTOR_GUIDE.md](INSTRUCTOR_GUIDE.md)**

---

**Happy Racing! 🏎️💨**

*Race Timmy - Learn autonomous systems through racing*
