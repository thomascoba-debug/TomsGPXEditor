#!/usr/bin/env python3
"""
Simple Single Instance Manager

A simpler approach to single instance functionality using file locking.
"""

import os
import sys
import time
import tempfile

# Only import fcntl on Unix systems
if sys.platform != 'win32':
    import fcntl

class SimpleSingleInstance:
    def __init__(self, app_name="TomsGPXEditor"):
        self.app_name = app_name
        self.lock_file = None
        self.lock_fd = None
        
    def _get_lock_file_path(self):
        """Get the path to the lock file"""
        temp_dir = tempfile.gettempdir()
        lock_file = os.path.join(temp_dir, f"{self.app_name}.lock")
        return lock_file
    
    def acquire(self):
        """Acquire single instance lock"""
        lock_file_path = self._get_lock_file_path()
        
        try:
            # Open lock file
            self.lock_file = open(lock_file_path, 'w')
            
            # Try to acquire exclusive lock
            # On Windows, we'll use a different approach
            if sys.platform == 'win32':
                # Windows approach - try to create file exclusively
                try:
                    # Write process info
                    self.lock_file.write(f"{os.getpid()}\n{time.time()}\n")
                    self.lock_file.flush()
                    
                    # Check if another process is using this file
                    with open(lock_file_path, 'r') as f:
                        content = f.read().strip()
                        if content:
                            lines = content.split('\n')
                            if len(lines) >= 2:
                                existing_pid = int(lines[0])
                                if existing_pid != os.getpid():
                                    # Check if process is still running
                                    if self._is_process_running(existing_pid):
                                        print(f"{self.app_name} is already running (PID: {existing_pid})")
                                        self.lock_file.close()
                                        return False
                    
                    return True
                    
                except (IOError, OSError):
                    # File is locked by another process
                    print(f"{self.app_name} is already running!")
                    self.lock_file.close()
                    return False
            else:
                # Unix approach - use fcntl
                fcntl.flock(self.lock_file.fileno(), fcntl.LOCK_EX)
                self.lock_file.write(f"{os.getpid()}\n{time.time()}\n")
                return True
                
        except Exception as e:
            print(f"Error acquiring single instance lock: {e}")
            if self.lock_file:
                self.lock_file.close()
            return False
    
    def _is_process_running(self, pid):
        """Check if a process is still running"""
        try:
            if sys.platform == 'win32':
                # Windows approach - try to open process
                import ctypes
                kernel32 = ctypes.windll.kernel32
                handle = kernel32.OpenProcess(0x0400, False, pid)
                if handle:
                    kernel32.CloseHandle(handle)
                    return True
                return False
            else:
                # Unix approach
                os.kill(pid, 0)
                return True
        except:
            return False
    
    def release(self):
        """Release single instance lock"""
        if self.lock_file:
            try:
                self.lock_file.close()
                # Remove lock file
                lock_file_path = self._get_lock_file_path()
                if os.path.exists(lock_file_path):
                    os.remove(lock_file_path)
            except:
                pass

def check_single_instance():
    """Check if this is the only instance"""
    manager = SimpleSingleInstance()
    return manager.acquire()

if __name__ == "__main__":
    # Test the single instance manager
    manager = SimpleSingleInstance()
    if manager.acquire():
        print("Single instance acquired successfully")
        print("Press Ctrl+C to release...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nReleasing single instance...")
            manager.release()
    else:
        print("Another instance is already running")
