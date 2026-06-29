# Aimbot AI Silent Aim Implementation

## Description
Silent aim algorithm implementation in Python using PyMem for gaming enhancement.

## Quick Start

```python
# Start silent aim thread
AimbotAI.work()

# Stop silent aim thread
AimbotAI.stop()

# Get best target
target = AimbotAI.get_best_target()
```

## Vector Math

```python
class Vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def distance_to(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    
    def distance_to(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2) ** 0.5
    
    def to_screen(self):
        # Convert world coordinates to screen
        # Implementation in AimbotAI
        pass
```

## Entity Structure

```python
class Entity:
    def __init__(self):
        self.pos = Vector3()
        self.head_pos = Vector3()
        self.bone_pos = Vector3()
        self.health = 0
        self.team = 0
        self.name = ""
```

## AimbotAI Implementation

```python
class AimbotAI:
    def __init__(self):
        self.stopped = True
        self.process_name = "HD-Player.exe"
        self.screen_center = {"x": 960, "y": 540}
        
    def get_best_target(self):
        # Find closest enemy to crosshair
        targets = self.get_entities()
        best_target = None
        best_distance = float('inf')
        
        for target in targets:
            if target.team != self.local_player.team and target.health > 0:
                distance = target.bone_pos.distance_to(self.screen_center)
                if distance < best_distance:
                    best_distance = distance
                    best_target = target
        
        return best_target
    
    def aim(self, target):
        # Move mouse to target bone position
        if target and target.bone_pos.to_screen():
            # Set cursor position (Windows API)
            pass
```

## Bone Offsets

| Offset | Bone |
|--------|------|
| `0x458` | Head |
| `0x454` | Spine |
| `0x45C` | Hip |
| `0x48C` | Left Shoulder |
| `0x490` | Right Shoulder |
| `0x4A4` | Head Collider |

## References
- REGIX Studio Memory.py
- REGIX Studio static/js/renderer.js