# Race Timmy Maps

This directory contains track definitions for Race Timmy.

## Available Maps

### Donut Track (`donut`)
- Classic oval racing circuit
- Simple, wide turns
- Good for beginners
- Start position: (0, -17)
- Two checkpoints: bottom (finish) and top (halfway)

### Infinity Track (`infinity`)
- Figure-8 circuit where the car crosses through the middle
- More challenging with tighter turns
- Requires precise control at the center crossing
- Start position: (15, 0) - right side of the track
- Two checkpoints: right loop (finish) and center crossing (halfway)

## Usage

Run the game with a specific map:

```bash
# Default map (donut)
python main.py

# Donut track
python main.py --map donut

# Infinity track
python main.py --map infinity
```

## Creating New Maps

To create a new map:

1. Create a new file in this directory (e.g., `mymap.py`)
2. Define a function that returns `(walls, checkpoint1, checkpoint2)`:
   - `walls`: list of wall segments (tuples of two numpy arrays)
   - `checkpoint1`: tuple of two numpy arrays defining the finish line
   - `checkpoint2`: tuple of two numpy arrays defining the halfway checkpoint
3. Import and register it in `__init__.py`
4. Add it to the choices in `main.py`

Example structure:

```python
import numpy as np
import math

def create_mymap_track():
    walls = []
    # ... create your track geometry ...
    
    checkpoint1 = (np.array([x1, y1]), np.array([x2, y2]))
    checkpoint2 = (np.array([x3, y3]), np.array([x4, y4]))
    
    return walls, checkpoint1, checkpoint2
```
