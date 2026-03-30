#!/usr/bin/env python3
"""
Basic Single Instance - Very Simple Approach

A very basic single instance implementation that should work reliably.
"""

import os
import sys
import tempfile
import time
import atexit

class BasicSingleInstance:
    def __init__(self, app_name="TomsGPXEditor"):
        self.app_name = app_name
        self.lock_file_path = None
        
        # Register cleanup on exit
        atexit.register(self.release)
        
    def _get_lock_file_path(self):
        """Get the path to the lock file"""
        temp_dir = tempfile.gettempdir()
        lock_file = os.path.join(temp_dir, f"{self.app_name}_{os.getpid()}.lock")
        return lock_file
    
    def acquire(self, force=False):
        """Acquire single instance lock"""
        self.lock_file_path = self._get_lock_file_path()
        
        try:
            # Check for existing lock files
            temp_dir = tempfile.gettempdir()
            existing_locks = []
            
            for filename in os.listdir(temp_dir):
                if filename.startswith(f"{self.app_name}_") and filename.endswith(".lock"):
                    existing_locks.append(os.path.join(temp_dir, filename))
            
            # Check if any existing lock files have running processes
            for lock_file in existing_locks:
                try:
                    # Check file age - if older than 30 seconds, assume stale
                    file_age = time.time() - os.path.getmtime(lock_file)
                    if file_age > 30 or force:  # 30 seconds timeout or force mode
                        print(f"Removing stale lock file: {os.path.basename(lock_file)}")
                        os.remove(lock_file)
                        continue
                    
                    with open(lock_file, 'r') as f:
                        pid_str = f.read().strip()
                        if pid_str:
                            pid = int(pid_str)
                            if self._is_process_running(pid):
                                print(f"{self.app_name} is already running (PID: {pid})")
                                return False
                            else:
                                # Clean up stale lock file
                                os.remove(lock_file)
                except:
                    # Can't read lock file or check process, remove it
                    try:
                        os.remove(lock_file)
                    except:
                        pass
            
            # Create our lock file
            with open(self.lock_file_path, 'w') as f:
                f.write(str(os.getpid()))
            
            return True
            
        except Exception as e:
            print(f"Error acquiring single instance lock: {e}")
            return False
    
    def _is_process_running(self, pid):
        """Check if a process is still running"""
        try:
            if sys.platform == 'win32':
                # Windows approach
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
        if self.lock_file_path and os.path.exists(self.lock_file_path):
            try:
                os.remove(self.lock_file_path)
            except:
                pass

def check_single_instance(force=False):
    """Check if this is the only instance"""
    manager = BasicSingleInstance()
    return manager.acquire(force)

def check_single_instance_with_force():
    """Check single instance with force option"""
    import sys
    
    # Check for --force flag
    force = "--force" in sys.argv or "-f" in sys.argv
    
    if not check_single_instance(force):
        if not force:
            print("Use --force or -f to start anyway")
            return False
        else:
            print("Force starting - removing existing locks...")
            # Force cleanup all locks
            temp_dir = tempfile.gettempdir()
            for filename in os.listdir(temp_dir):
                if filename.startswith("TomsGPXEditor_") and filename.endswith(".lock"):
                    try:
                        os.remove(os.path.join(temp_dir, filename))
                        print(f"Removed: {filename}")
                    except:
                        pass
    
    return True

if __name__ == "__main__":
    # Test the single instance manager
    manager = BasicSingleInstance()
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
