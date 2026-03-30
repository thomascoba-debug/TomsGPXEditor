#!/usr/bin/env python3
"""
Windows Single Instance Manager

Simple Windows-specific single instance implementation.
"""

import os
import sys
import time
import tempfile
import ctypes
from ctypes import wintypes

class WindowsSingleInstance:
    def __init__(self, app_name="TomsGPXEditor"):
        self.app_name = app_name
        self.lock_file = None
        self.mutex_handle = None
        
    def _get_lock_file_path(self):
        """Get the path to the lock file"""
        temp_dir = tempfile.gettempdir()
        lock_file = os.path.join(temp_dir, f"{self.app_name}.lock")
        return lock_file
    
    def _create_mutex(self):
        """Create a Windows mutex for single instance"""
        try:
            # Create a unique mutex name
            mutex_name = f"Global\\{self.app_name}_{os.getuid() if hasattr(os, 'getuid') else os.getpid()}"
            
            # Create or open mutex
            self.mutex_handle = ctypes.windll.kernel32.CreateMutexW(
                None, True, mutex_name
            )
            
            if self.mutex_handle == 0:
                return False
            
            # Check if mutex already existed
            error_code = ctypes.windll.kernel32.GetLastError()
            if error_code == 183:  # ERROR_ALREADY_EXISTS
                ctypes.windll.kernel32.CloseHandle(self.mutex_handle)
                self.mutex_handle = None
                return False
            
            return True
            
        except Exception:
            return False
    
    def acquire(self):
        """Acquire single instance lock"""
        # First try mutex approach
        if self._create_mutex():
            return True
        
        # Fallback to file-based approach
        lock_file_path = self._get_lock_file_path()
        
        try:
            # Try to open file in exclusive mode
            self.lock_file = open(lock_file_path, 'w')
            
            # Write process info
            self.lock_file.write(f"{os.getpid()}\n{time.time()}\n")
            self.lock_file.flush()
            
            # Try to lock the file (Windows doesn't have flock, so we use a different approach)
            # We'll check if another process is using this file
            try:
                # Try to open the file again - if it fails, it's locked
                test_file = open(lock_file_path, 'r')
                test_file.close()
                
                # File opened successfully, check content
                with open(lock_file_path, 'r') as f:
                    content = f.read().strip()
                    if content:
                        lines = content.split('\n')
                        if len(lines) >= 2:
                            existing_pid = int(lines[0])
                            if existing_pid != os.getpid():
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
                
        except Exception as e:
            print(f"Error acquiring single instance lock: {e}")
            if self.lock_file:
                self.lock_file.close()
            return False
    
    def _is_process_running(self, pid):
        """Check if a process is still running on Windows"""
        try:
            # Use Windows API to check if process exists
            handle = ctypes.windll.kernel32.OpenProcess(0x0400, False, pid)
            if handle:
                ctypes.windll.kernel32.CloseHandle(handle)
                return True
            return False
        except:
            return False
    
    def release(self):
        """Release single instance lock"""
        if self.mutex_handle:
            ctypes.windll.kernel32.CloseHandle(self.mutex_handle)
            self.mutex_handle = None
        
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
    manager = WindowsSingleInstance()
    return manager.acquire()

if __name__ == "__main__":
    # Test the single instance manager
    manager = WindowsSingleInstance()
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
