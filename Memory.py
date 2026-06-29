import pyexpat
import pymem
import pymem.pattern
import pymem.process
import time
import ctypes
import ctypes.wintypes
import os
import sys
import threading
from datetime import datetime
from pymem.memory import read_bytes, write_bytes
from pymem.pattern import pattern_scan_all

# ============ Win32 API ============
user32 = ctypes.windll.user32
VK_LBUTTON = 0x01

def get_async_key_state(v_key):
    """Get key state using Win32 API"""
    return user32.GetAsyncKeyState(v_key) & 0x8000

# ============ Vector Classes ============
class Vector2:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
    
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    
    def length(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    def distance_to(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

class Vector3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z
    
    def distance_to(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2) ** 0.5

# ============ Entity Class ============
class Entity:
    def __init__(self, address=0):
        self.Address = address
        self.IsDead = False
        self.IsKnocked = False
        self.Head = Vector3()
        self.Spine = Vector3()
        self.Hip = Vector3()
        self.LeftShoulder = Vector3()
        self.RightShoulder = Vector3()
        self.LeftHand = Vector3()
        self.RightWristJoint = Vector3()
        self.HeadCollider = 0

# ============ AimbotAI Class ============
class AimbotAI:
    aim_thread = None
    is_running = False
    patched_memory = {}
    last_click_start = None
    is_click_held = False
    last_silent_restore = datetime.now()
    
    # Bone offsets
    BONE_OFFSETS = {
        0: 0x4A4,  # Head
        1: 0x3F4,  # Spine
        2: 0x3F8,  # Hip
    }
    
    @staticmethod
    def is_alive():
        return AimbotAI.is_running and AimbotAI.aim_thread is not None and AimbotAI.aim_thread.is_alive()
    
    @staticmethod
    def work():
        if AimbotAI.is_running:
            return
        
        AimbotAI.is_running = True
        AimbotAI.patched_memory = {}
        AimbotAI.last_click_start = None
        AimbotAI.is_click_held = False
        
        def aim_thread_func():
            while AimbotAI.is_running:
                try:
                    # Auto-restore patched memory every 3000ms
                    if (datetime.now() - AimbotAI.last_silent_restore).total_seconds() >= 3:
                        AimbotAI.restore_patched_memory()
                        AimbotAI.last_silent_restore = datetime.now()
                    
                    # Check if aimbot is enabled and we have valid dimensions
                    if not Config.AimbotAIEnabled or Core.Width < 1 or Core.Height < 1 or not Core.HaveMatrix:
                        AimbotAI.restore_patched_memory()
                        time.sleep(0.01)
                        continue
                    
                    # Find best target
                    target = AimbotAI.find_best_target()
                    if target is None or target.Address == 0:
                        time.sleep(0.005)
                        continue
                    
                    # Get bone collider offset
                    bone_offset = AimbotAI.BONE_OFFSETS.get(Config.AimbotTargetBone, 0x4A4)
                    bone_collider = AimbotAI.read_uint(target.Address + bone_offset)
                    if bone_collider == 0:
                        time.sleep(0.005)
                        continue
                    
                    # Check mouse state
                    is_mouse_down = get_async_key_state(VK_LBUTTON) != 0
                    
                    if is_mouse_down:
                        if not AimbotAI.is_click_held:
                            AimbotAI.last_click_start = datetime.now()
                            AimbotAI.is_click_held = True
                        
                        held_duration = (datetime.now() - AimbotAI.last_click_start).total_seconds() * 1000
                        if held_duration >= Config.AimbotAIMaxHoldTime:
                            AimbotAI.restore_patched_memory()
                            time.sleep(0.001)
                            continue
                        
                        patch_addr = target.Address + 0x54
                        
                        # Store original value if not already patched
                        if patch_addr not in AimbotAI.patched_memory:
                            original = AimbotAI.read_uint(patch_addr)
                            if original:
                                AimbotAI.patched_memory[patch_addr] = original
                        
                        # Write silent aim patch
                        AimbotAI.write_uint(patch_addr, bone_collider)
                    else:
                        AimbotAI.is_click_held = False
                        AimbotAI.last_click_start = None
                        AimbotAI.restore_patched_memory()
                    
                    time.sleep(0.001)
                    
                except Exception as ex:
                    print(f"[AimbotAI] Error: {ex}")
                    time.sleep(0.1)
            
            AimbotAI.restore_patched_memory()
        
        AimbotAI.aim_thread = threading.Thread(target=aim_thread_func, daemon=True)
        AimbotAI.aim_thread.start()
    
    @staticmethod
    def stop():
        AimbotAI.is_running = False
        try:
            if AimbotAI.aim_thread:
                AimbotAI.aim_thread.join(timeout=0.3)
        except Exception:
            pass
        AimbotAI.restore_patched_memory()
    
    @staticmethod
    def restore_patched_memory():
        pm = None
        try:
            pm = pymem.Pymem("HD-Player.exe")
            for addr, value in AimbotAI.patched_memory.items():
                AimbotAI.write_uint_pm(pm, addr, value)
        except Exception as ex:
            print(f"[AimbotAI] Restore error: {ex}")
        finally:
            AimbotAI.patched_memory.clear()
    
    @staticmethod
    def read_uint(address):
        try:
            pm = pymem.Pymem("HD-Player.exe")
            return pm.read_uint(address)
        except:
            return 0
    
    @staticmethod
    def read_uint_pm(pm, address):
        try:
            return pm.read_uint(address)
        except:
            return 0
    
    @staticmethod
    def write_uint(address, value):
        try:
            pm = pymem.Pymem("HD-Player.exe")
            pm.write_uint(address, value)
        except Exception as ex:
            print(f"[AimbotAI] Write error: {ex}")
    
    @staticmethod
    def write_uint_pm(pm, address, value):
        try:
            pm.write_uint(address, value)
        except:
            pass
    
    @staticmethod
    def get_target_bone_position(entity):
        bone_map = {
            0: entity.Head,      # Head
            1: entity.Spine,     # Spine
            2: entity.Hip,       # Hip
            3: entity.LeftShoulder,
            4: entity.RightShoulder,
            5: entity.LeftHand,
            6: entity.RightWristJoint,
        }
        return bone_map.get(Config.AimbotTargetBone, entity.Head)
    
    @staticmethod
    def find_best_target():
        best_target = None
        closest_distance = float('inf')
        screen_center = Vector2(Core.Width / 2.0, Core.Height / 2.0)
        
        for entity_addr in Core.Entities.values():
            try:
                entity = AimbotAI.get_entity(entity_addr)
                if entity is None:
                    continue
                if entity.IsDead:
                    continue
                if Config.IgnoreKnocked and entity.IsKnocked:
                    continue
                
                target_bone = AimbotAI.get_target_bone_position(entity)
                bone_2d = AimbotAI.world_to_screen(Core.CameraMatrix, target_bone, Core.Width, Core.Height)
                
                if bone_2d.x < 1 or bone_2d.y < 1:
                    continue
                
                dist_3d = Core.LocalMainCamera.distance_to(target_bone)
                if dist_3d > Config.AimbotAIMaxDistance:
                    continue
                
                dist_2d = screen_center.distance_to(bone_2d)
                if dist_2d < closest_distance and dist_2d <= Config.AimbotAIFov:
                    closest_distance = dist_2d
                    best_target = entity
            except Exception:
                continue
        
        return best_target
    
    @staticmethod
    def get_entity(address):
        """Read entity data from memory"""
        try:
            pm = pymem.Pymem("HD-Player.exe")
            entity = Entity(address)
            
            # Read bone positions (offsets based on provided address map)
            entity.Head = AimbotAI.read_vector3(pm, address + 0x458)
            entity.Spine = AimbotAI.read_vector3(pm, address + 0x454)  # Added Spine
            entity.Hip = AimbotAI.read_vector3(pm, address + 0x45C)
            entity.LeftShoulder = AimbotAI.read_vector3(pm, address + 0x48C)
            entity.RightShoulder = AimbotAI.read_vector3(pm, address + 0x490)
            
            # Read collider at HeadCollider offset
            entity.HeadCollider = pm.read_uint(address + 0x4A4)
            
            return entity
        except Exception:
            return None
    
    @staticmethod
    def read_vector3(pm, address):
        try:
            x = pm.read_float(address)
            y = pm.read_float(address + 4)
            z = pm.read_float(address + 8)
            return Vector3(x, y, z)
        except:
            return Vector3()
    
    @staticmethod
    def world_to_screen(matrix, pos, width, height):
        try:
            # Simple W2S implementation
            x = pos.x * matrix[0] + pos.y * matrix[4] + pos.z * matrix[8] + matrix[12]
            y = pos.x * matrix[1] + pos.y * matrix[5] + pos.z * matrix[9] + matrix[13]
            w = pos.x * matrix[3] + pos.y * matrix[7] + pos.z * matrix[11] + matrix[15]
            
            if w < 0.001:
                return Vector2(-1, -1)
            
            screen_x = (width / 2 + x * width / 2) / w
            screen_y = (height / 2 - y * height / 2) / w
            
            return Vector2(screen_x, screen_y)
        except:
            return Vector2(-1, -1)

pm = None

# ============ MKP FUNCTION ============
def mkp(aob: str):
    if '??' in aob:
        if aob.startswith("??"):
            aob = f" {aob}"
            n = aob.replace(" ??", ".").replace(" ", "\\x")
            b = bytes(n.encode())
        else:
            n = aob.replace(" ??", ".").replace(" ", "\\x")
            b = bytes(f"\\x{n}".encode())
        del n
        return b
    else:
        m = aob.replace(" ", "\\x")
        c = bytes(f"\\x{m}".encode())
        del m
        return c

# ============ AOB PATTERNS (CLEAN STRINGS) ============
AIMBOT_PATTERN = "FF FF 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 FF FF FF FF FF FF FF FF FF FF FF FF ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? 00 00 00 00 00 00 00 00 00 00 00 00 A5 43"

DRAG_PATTERN = "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 FF FF FF FF FF FF FF FF FF FF FF FF 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ?? ?? ?? ?? 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? 00 00 00 00 00 00 00 00 00 00 00 00 00 00 A5 43 ?? ?? ?? 00 00 ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? 00 00 ?? ?? ?? ?? ?? ?? ?? ?? ??"

# ============ SCAN AND REPLACE ============
def scan_and_replace(processName, search, replace):
    try:
        pm = pymem.Pymem(processName)
        # If search is string, convert using mkp
        if isinstance(search, str):
            search = mkp(search)
        matches = pattern_scan_all(pm.process_handle, search, return_multiple=True)
        if matches:
            for match in matches:
                pm.write_bytes(match, replace, len(replace))
            return True
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_process(procesName):
    try:
        pm = pymem.Pymem(procesName)
        print('Process Found Please Continue')
        return pm.process_id
    except:
        print('Process Not Found Waiting for process')
        return False

def get_pid(processName):
    pm = pymem.Pymem(processName)
    return pm.process_id

def get_drive_serial_number():
    kernel32 = ctypes.windll.kernel32
    volume_name_buffer = ctypes.create_unicode_buffer(1024)
    file_system_name_buffer = ctypes.create_unicode_buffer(1024)
    serial_number = ctypes.c_ulong(0)
    max_component_length = ctypes.c_ulong(0)
    file_system_flags = ctypes.c_ulong(0)
    success = kernel32.GetVolumeInformationW(
        ctypes.c_wchar_p("C:\\"),
        volume_name_buffer,
        ctypes.sizeof(volume_name_buffer),
        ctypes.byref(serial_number),
        ctypes.byref(max_component_length),
        ctypes.byref(file_system_flags),
        file_system_name_buffer,
        ctypes.sizeof(file_system_name_buffer)
    )
    if success:
        return serial_number.value
    return None

def get_hwid():
    serial_number = get_drive_serial_number()
    if serial_number:
        return serial_number
    return None

def adjust_privileges():
    SE_DEBUG_NAME = "SeDebugPrivilege"
    SE_PRIVILEGE_ENABLED = 0x00000002
    token_handle = ctypes.c_void_p()
    luid = ctypes.c_longlong()
    
    ctypes.windll.advapi32.OpenProcessToken(
        ctypes.windll.kernel32.GetCurrentProcess(),
        0x20 | 0x8,
        ctypes.byref(token_handle)
    )
    ctypes.windll.advapi32.LookupPrivilegeValueA(
        0, SE_DEBUG_NAME.encode('ascii'), ctypes.byref(luid)
    )
    
    class LUID_AND_ATTRIBUTES(ctypes.Structure):
        _fields_ = [("Luid", ctypes.c_longlong), ("Attributes", ctypes.c_ulong)]
    class TOKEN_PRIVILEGES(ctypes.Structure):
        _fields_ = [("PrivilegeCount", ctypes.c_ulong), ("Privileges", LUID_AND_ATTRIBUTES)]
    
    new_privileges = TOKEN_PRIVILEGES(1, LUID_AND_ATTRIBUTES(luid.value, SE_PRIVILEGE_ENABLED))
    ctypes.windll.advapi32.AdjustTokenPrivileges(
        token_handle, False, ctypes.byref(new_privileges), 0, None, None
    )
    ctypes.windll.kernel32.CloseHandle(token_handle)

def find_pattern(pm, module_name, pattern):
    if isinstance(pattern, str):
        pattern = mkp(pattern)
    return pattern_scan_all(pm.process_handle, pattern, return_multiple=True)

# ============ AIMBOT FUNCTIONS ============
def aimbot_load():
    try:
        adjust_privileges()
        process_name = "HD-Player.exe"
        pm = pymem.Pymem(process_name)
        
        # ✅ FIX: Use mkp() to convert string pattern to bytes
        pattern = mkp(AIMBOT_PATTERN)
        addresses = find_pattern(pm, process_name, pattern)

        if not addresses:
            print("No addresses found")
            return False
        print(f"Found {len(addresses)} addresses")
        return addresses
    except Exception as e:
        print(f"Error: {e}")
        return False

original_values = []

def aimbot_on(addresses):
    global original_values
    if not addresses:
        return False
    try:
        pm = pymem.Pymem("HD-Player.exe")
        original_values.clear()
        for address in addresses:
            addressscan = address + 0xB6   # Source
            addressrep = address + 0xB2    # Target
            buffer = pm.read_int(addressscan)
            original_values.append(pm.read_int(addressrep))
            pm.write_int(addressrep, buffer)
        return True
    except Exception as e:
        print(f"Error in aimbot_on: {e}")
        return False

def aimbot_off(addresses):
    global original_values
    if not addresses or not original_values:
        return False
    try:
        pm = pymem.Pymem("HD-Player.exe")
        for index, address in enumerate(addresses):
            addressrep = address + 0xB2
            if index < len(original_values):
                pm.write_int(addressrep, original_values[index])
        return True
    except Exception as e:
        print(f"Error in aimbot_off: {e}")
        return False

# ============ DRAG FUNCTIONS ============
drag_addresses = []
original_drag_values = []

def drag_load():
    global drag_addresses
    try:
        adjust_privileges()
        process_name = "HD-Player.exe"
        pm = pymem.Pymem(process_name)
        
        # ✅ FIX: Use mkp() instead of raw bytes
        pattern = mkp(DRAG_PATTERN)
        drag_addresses = find_pattern(pm, process_name, pattern)

        if not drag_addresses:
            print("No drag addresses found")
            return False
        print(f"Found {len(drag_addresses)} drag addresses")
        return drag_addresses
    except Exception as e:
        print(f"Error in drag_load: {e}")
        return False

def aimdrag_on(drag_addresses):
    global original_drag_values
    if not drag_addresses:
        return False
    try:
        pm = pymem.Pymem("HD-Player.exe")
        original_drag_values.clear()
        for address in drag_addresses:
            addressscan = address + 0xE2
            addressrep = address + 0xAE
            buffer = pm.read_int(addressscan)
            original_drag_values.append(pm.read_int(addressrep))
            pm.write_int(addressrep, buffer)
        return True
    except Exception as e:
        print(f"Error in aimdrag_on: {e}")
        return False

def aimdrag_off(drag_addresses):
    global original_drag_values
    if not drag_addresses or not original_drag_values:
        return False
    try:
        pm = pymem.Pymem("HD-Player.exe")
        for index, address in enumerate(drag_addresses):
            addressrep = address + 0xAE
            if index < len(original_drag_values):
                pm.write_int(addressrep, original_drag_values[index])
        return True
    except Exception as e:
        print(f"Error in aimdrag_off: {e}")
        return False

# ============ Config Stub (for AimbotAI) ============
class Config:
    AimbotAIEnabled = True
    AimbotTargetBone = 0  # 0=Head, 1=Spine, 2=Hip
    AimbotAIMaxHoldTime = 1000  # ms
    AimbotAIMaxDistance = 200.0  # units
    AimbotAIFov = 100.0  # pixels
    IgnoreKnocked = True

# ============ Core Stub (for AimbotAI) ============
class Core:
    Width = 1920
    Height = 1080
    HaveMatrix = True
    CameraMatrix = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
    LocalMainCamera = Vector3()
    Entities = {}  # Dict of entity addresses to data