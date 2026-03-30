#!/usr/bin/env python3
"""
Single Instance Manager

This script ensures that only one instance of TomsGPXEditor can run at a time.
"""

import os
import sys
import time
import socket
import tempfile
import threading
from pathlib import Path

class SingleInstanceManager:
    def __init__(self, app_name="TomsGPXEditor"):
        self.app_name = app_name
        self.lock_file = None
        self.socket_port = self._get_free_port()
        self.socket_thread = None
        self.running = False
        
    def _get_lock_file_path(self):
        """Get the path to the lock file"""
        temp_dir = tempfile.gettempdir()
        lock_file = os.path.join(temp_dir, f"{self.app_name}.lock")
        return lock_file
    
    def _get_free_port(self):
        """Get a free port for the socket"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.listen(1)
            port = s.getsockname()[1]
        return port
    
    def _create_lock_file(self):
        """Create a lock file with process info"""
        lock_file_path = self._get_lock_file_path()
        
        try:
            # Check if lock file already exists
            if os.path.exists(lock_file_path):
                with open(lock_file_path, 'r') as f:
                    content = f.read().strip()
                    if content:
                        # Try to parse existing lock info
                        parts = content.split(':')
                        if len(parts) >= 2:
                            existing_pid = parts[0]
                            existing_port = parts[1]
                            
                            # Try to connect to existing instance
                            if self._test_existing_instance(existing_port):
                                print(f"{self.app_name} is already running (PID: {existing_pid})")
                                print("Bringing existing instance to foreground...")
                                self._bring_to_front(existing_port)
                                return False
                            else:
                                print(f"Stale lock file found (PID: {existing_pid})")
                                os.remove(lock_file_path)
            
            # Create new lock file
            pid = os.getpid()
            lock_content = f"{pid}:{self.socket_port}:{time.time()}"
            
            with open(lock_file_path, 'w') as f:
                f.write(lock_content)
            
            self.lock_file = lock_file_path
            return True
            
        except Exception as e:
            print(f"Error creating lock file: {e}")
            return False
    
    def _test_existing_instance(self, port):
        """Test if existing instance is still running"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex(('localhost', int(port)))
            sock.close()
            return result == 0
        except:
            return False
    
    def _bring_to_front(self, port):
        """Send message to existing instance to bring it to front"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect(('localhost', int(port)))
            sock.send(b'BRING_TO_FRONT')
            sock.close()
        except:
            pass
    
    def _start_socket_server(self):
        """Start socket server to listen for bring-to-front requests"""
        def server_thread():
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind(('localhost', self.socket_port))
                    s.listen(1)
                    s.settimeout(1)  # Non-blocking
                    
                    while self.running:
                        try:
                            conn, addr = s.accept()
                            data = conn.recv(1024)
                            if data == b'BRING_TO_FRONT':
                                self._handle_bring_to_front()
                            conn.close()
                        except socket.timeout:
                            continue
                        except:
                            break
            except:
                pass
        
        self.socket_thread = threading.Thread(target=server_thread, daemon=True)
        self.socket_thread.start()
    
    def _handle_bring_to_front(self):
        """Handle bring-to-front request"""
        try:
            # This would be implemented in the main application
            # For now, we just print a message
            print("Bring to front request received")
        except:
            pass
    
    def acquire(self):
        """Acquire single instance lock"""
        if not self._create_lock_file():
            return False
        
        self.running = True
        self._start_socket_server()
        return True
    
    def release(self):
        """Release single instance lock"""
        self.running = False
        
        if self.lock_file and os.path.exists(self.lock_file):
            try:
                os.remove(self.lock_file)
            except:
                pass
        
        if self.socket_thread:
            self.socket_thread.join(timeout=2)

def check_single_instance():
    """Check if this is the only instance"""
    manager = SingleInstanceManager()
    return manager.acquire()

if __name__ == "__main__":
    # Test the single instance manager
    manager = SingleInstanceManager()
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
