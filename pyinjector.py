"""
Pure-Python replacement for the 'pyinjector' package.
Provides the same `inject(pid, dll_path)` function using ctypes + Windows API.

This avoids the need for Microsoft Visual C++ 14.0 Build Tools
which is required to compile the original pyinjector C extension
on Python 3.14+.

Usage:
    from pyinjector import inject
    inject(pid, "path/to/dll.dll")
"""

import ctypes
import ctypes.wintypes
import os
import sys

# Windows API constants
PROCESS_ALL_ACCESS = 0x1F0FFF
MEM_COMMIT = 0x1000
MEM_RESERVE = 0x2000
PAGE_READWRITE = 0x04
INFINITE = 0xFFFFFFFF

# Get kernel32 handle
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)


def _get_process_handle(pid):
    """Open a handle to the target process with all access."""
    PROCESS_QUERY_INFORMATION = 0x0400
    PROCESS_VM_OPERATION = 0x0008
    PROCESS_VM_WRITE = 0x0020
    PROCESS_VM_READ = 0x0010
    PROCESS_CREATE_THREAD = 0x0002

    access = (
        PROCESS_QUERY_INFORMATION |
        PROCESS_VM_OPERATION |
        PROCESS_VM_WRITE |
        PROCESS_VM_READ |
        PROCESS_CREATE_THREAD
    )

    handle = kernel32.OpenProcess(access, False, pid)
    if not handle:
        error = ctypes.get_last_error()
        raise RuntimeError(f"OpenProcess failed with error code {error} (pid={pid})")
    return handle


def _get_load_library_address():
    """Get the address of LoadLibraryW in kernel32.dll."""
    # LoadLibraryW is in kernel32.dll which is loaded in every process
    load_library = kernel32.LoadLibraryW
    return load_library


def inject(pid, dll_path):
    """
    Inject a DLL into a process by PID.

    Args:
        pid (int): Process ID of the target process.
        dll_path (str): Absolute or relative path to the DLL file.

    Returns:
        int: The PID of the target process on success.

    Raises:
        RuntimeError: If injection fails at any step.
    """
    if not os.path.exists(dll_path):
        raise FileNotFoundError(f"DLL not found: {dll_path}")

    # Convert to absolute path
    dll_path = os.path.abspath(dll_path)

    # Encode the DLL path as UTF-16 (wide string) for LoadLibraryW
    dll_path_bytes = dll_path.encode('utf-16-le') + b'\x00\x00'

    # Open the target process
    process_handle = _get_process_handle(pid)

    try:
        # Allocate memory in the target process for the DLL path string
        remote_memory = kernel32.VirtualAllocEx(
            process_handle,
            None,
            len(dll_path_bytes),
            MEM_COMMIT | MEM_RESERVE,
            PAGE_READWRITE
        )
        if not remote_memory:
            error = ctypes.get_last_error()
            raise RuntimeError(f"VirtualAllocEx failed with error code {error}")

        # Write the DLL path into the allocated memory
        written = ctypes.c_size_t(0)
        success = kernel32.WriteProcessMemory(
            process_handle,
            remote_memory,
            dll_path_bytes,
            len(dll_path_bytes),
            ctypes.byref(written)
        )
        if not success:
            error = ctypes.get_last_error()
            raise RuntimeError(f"WriteProcessMemory failed with error code {error}")

        # Get the address of LoadLibraryW
        load_library_addr = kernel32.GetProcAddress(
            kernel32.GetModuleHandleW("kernel32.dll"),
            b"LoadLibraryW"
        )
        if not load_library_addr:
            error = ctypes.get_last_error()
            raise RuntimeError(f"GetProcAddress(LoadLibraryW) failed with error code {error}")

        # Create a remote thread that calls LoadLibraryW with our DLL path
        thread_id = ctypes.c_ulong(0)
        thread_handle = kernel32.CreateRemoteThread(
            process_handle,
            None,
            0,
            load_library_addr,
            remote_memory,
            0,
            ctypes.byref(thread_id)
        )
        if not thread_handle:
            error = ctypes.get_last_error()
            raise RuntimeError(f"CreateRemoteThread failed with error code {error}")

        # Wait for the thread to finish
        kernel32.WaitForSingleObject(thread_handle, INFINITE)

        # Get the exit code (the HMODULE of the loaded DLL)
        exit_code = ctypes.c_ulong(0)
        kernel32.GetExitCodeThread(thread_handle, ctypes.byref(exit_code))

        # Clean up
        kernel32.CloseHandle(thread_handle)
        kernel32.VirtualFreeEx(process_handle, remote_memory, 0, 0x8000)  # MEM_RELEASE

        if exit_code.value == 0:
            raise RuntimeError(f"LoadLibraryW returned NULL - DLL injection failed for {dll_path}")

        return pid

    finally:
        kernel32.CloseHandle(process_handle)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python pyinjector.py <pid> <dll_path>")
        sys.exit(1)
    pid = int(sys.argv[1])
    dll_path = sys.argv[2]
    inject(pid, dll_path)
    print(f"Injected {dll_path} into PID {pid}")