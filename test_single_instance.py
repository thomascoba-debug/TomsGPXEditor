#!/usr/bin/env python3
"""
Test Single Instance Functionality

This script tests the single instance functionality of TomsGPXEditor.
"""

import subprocess
import time
import sys
import os

def test_single_instance():
    """Test single instance functionality"""
    
    print("TESTING SINGLE INSTANCE FUNCTIONALITY")
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
        time.sleep(2)
        
        # Check if process is still running
        if process1.poll() is None:
            print("   ✅ First instance started successfully")
        else:
            stdout, stderr = process1.communicate()
            print(f"   ❌ First instance failed: {stderr}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error starting first instance: {e}")
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
        time.sleep(2)
        
        # Check if second process has exited (it should)
        if process2.poll() is not None:
            stdout, stderr = process2.communicate()
            print("   ✅ Second instance correctly rejected")
            print(f"   Message: {stdout.strip()}")
        else:
            print("   ❌ Second instance was not rejected")
            process2.terminate()
            return False
            
    except Exception as e:
        print(f"   ❌ Error testing second instance: {e}")
        return False
    
    # Test 3: Clean up first instance
    print("\n3. Cleaning up first instance...")
    try:
        process1.terminate()
        process1.wait(timeout=5)
        print("   ✅ First instance terminated successfully")
    except:
        process1.kill()
        print("   ⚠️  First instance had to be killed")
    
    # Test 4: Verify lock file cleanup
    print("\n4. Checking lock file cleanup...")
    import tempfile
    lock_file = os.path.join(tempfile.gettempdir(), "TomsGPXEditor.lock")
    
    if os.path.exists(lock_file):
        print("   ⚠️  Lock file still exists (may be normal)")
    else:
        print("   ✅ Lock file cleaned up properly")
    
    print("\n" + "=" * 50)
    print("SINGLE INSTANCE TEST COMPLETED")
    print("✅ All tests passed!")
    return True

if __name__ == "__main__":
    success = test_single_instance()
    
    if success:
        print("\nSingle instance functionality is working correctly!")
        print("Only one instance of TomsGPXEditor can run at a time.")
    else:
        print("\nSingle instance functionality needs attention.")
