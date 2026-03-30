#!/usr/bin/env python3
"""
Test Windows Single Instance

Test the Windows-specific single instance functionality.
"""

import subprocess
import time
import sys
import os

def test_windows_single_instance():
    """Test Windows single instance functionality"""
    
    print("TESTING WINDOWS SINGLE INSTANCE FUNCTIONALITY")
    print("=" * 50)
    
    # Test 1: Start first instance
    print("\n1. Starting first instance...")
    try:
        process1 = subprocess.Popen([sys.executable, "main.py"], 
                                   cwd=os.getcwd(),
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   text=True)
        
        # Give it time to start
        time.sleep(3)
        
        # Check if process is still running
        if process1.poll() is None:
            print("   PASS: First instance started successfully")
        else:
            stdout, stderr = process1.communicate()
            print(f"   FAIL: First instance failed: {stderr}")
            print(f"   stdout: {stdout}")
            return False
            
    except Exception as e:
        print(f"   FAIL: Error starting first instance: {e}")
        return False
    
    # Test 2: Try to start second instance
    print("\n2. Attempting to start second instance...")
    try:
        process2 = subprocess.Popen([sys.executable, "main.py"], 
                                   cwd=os.getcwd(),
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   text=True)
        
        # Give it time to attempt start
        time.sleep(3)
        
        # Check if second process has exited (it should)
        if process2.poll() is not None:
            stdout, stderr = process2.communicate()
            print("   PASS: Second instance correctly rejected")
            print(f"   Message: {stdout.strip()}")
            if stderr:
                print(f"   stderr: {stderr}")
        else:
            print("   FAIL: Second instance was not rejected")
            process2.terminate()
            return False
            
    except Exception as e:
        print(f"   FAIL: Error testing second instance: {e}")
        return False
    
    # Test 3: Clean up first instance
    print("\n3. Cleaning up first instance...")
    try:
        process1.terminate()
        process1.wait(timeout=5)
        print("   PASS: First instance terminated successfully")
    except:
        process1.kill()
        print("   WARN: First instance had to be killed")
    
    print("\n" + "=" * 50)
    print("WINDOWS SINGLE INSTANCE TEST COMPLETED")
    print("PASS: All tests passed!")
    return True

if __name__ == "__main__":
    success = test_windows_single_instance()
    
    if success:
        print("\nWindows single instance functionality is working correctly!")
        print("Only one instance of TomsGPXEditor can run at a time.")
    else:
        print("\nWindows single instance functionality needs attention.")
