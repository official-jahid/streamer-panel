# Windows Memory Manipulation with PyMem

## Description
Advanced patterns for Windows process memory reading/writing using PyMem library.

## Quick Start

```python
import pymem
import pymem.pattern

# Attach to process
pm = pymem.Pymem("HD-Player.exe")

# Read memory
value = pm.read_uint(address)
value = pm.read_int(address)

# Write memory
pm.write_uint(address, value)
pm.write_bytes(address, data, length)

# Pattern scan
pattern = b"\xFF\xFF\x00\x00"
matches = pattern_scan_all(pm.process_handle, pattern, return_multiple=True)
```

## Common Patterns

### Read/Write Types
- `read_uint(address)` - Read unsigned int (4 bytes)
- `read_int(address)` - Read signed int (4 bytes)
- `read_float(address)` - Read float (4 bytes)
- `read_bytes(address, length)` - Read raw bytes

### Pattern Scanning
```python
def mkp(aob: str):
    if '??' in aob:
        n = aob.replace(" ??", ".").replace(" ", "\\x")
        return bytes(f"\\x{n}".encode())
    m = aob.replace(" ", "\\x")
    return bytes(f"\\x{m}".encode())

pattern = mkp("FF FF 00 00 ?? ??")
matches = pattern_scan_all(pm.process_handle, pattern, return_multiple=True)
```

### Offsets Used in REGIX Studio
- `0x458` - Head position (Vector3)
- `0x454` - Spine position (Vector3)
- `0x45C` - Hip position (Vector3)
- `0x48C` - Left Shoulder
- `0x490` - Right Shoulder
- `0x4A4` - Head Collider
- `0x54` - Hitbox Patch Address

## Safety Patterns

Always restore original values:
```python
original_values = []

# Store before patching
original_values.append(pm.read_int(address + offset))

# Write patched value
pm.write_int(address + offset, new_value)

# Restore on exit
for i, addr in enumerate(addresses):
    pm.write_int(addr + offset, original_values[i])
```

## References
- REGIX Studio Memory.py for full implementation