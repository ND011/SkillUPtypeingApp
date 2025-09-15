#!/usr/bin/env python3
"""
Test script to verify the executable works
"""
import os
import subprocess
import sys
from pathlib import Path

def test_executable():
    """Test if the SPEED executable runs properly"""
    print("🔍 Testing SPEED Executable")
    print("=" * 50)
    
    exe_path = Path("dist/SPEED.exe")
    
    if not exe_path.exists():
        print("❌ SPEED.exe not found in dist directory")
        return False
    
    # Get file size
    size_mb = exe_path.stat().st_size / (1024 * 1024)
    print(f"📏 Executable size: {size_mb:.1f} MB")
    print(f"📍 Location: {exe_path.absolute()}")
    
    # Try to run the executable (it will open the GUI)
    print("🚀 Attempting to launch SPEED.exe...")
    print("   (This will open the GUI application)")
    
    try:
        # Start the process but don't wait for it to complete
        # since it's a GUI application
        process = subprocess.Popen([str(exe_path)], 
                                 cwd=exe_path.parent,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        
        print("✅ SPEED.exe launched successfully!")
        print(f"🔢 Process ID: {process.pid}")
        print("🎯 The application should now be running.")
        print("   Close the application window to continue...")
        
        # Wait a moment to see if there are immediate errors
        import time
        time.sleep(2)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Application is running normally")
            return True
        else:
            print("❌ Application exited immediately")
            stdout, stderr = process.communicate()
            if stdout:
                print("STDOUT:", stdout.decode())
            if stderr:
                print("STDERR:", stderr.decode())
            return False
            
    except Exception as e:
        print(f"❌ Failed to launch executable: {e}")
        return False

if __name__ == "__main__":
    success = test_executable()
    if success:
        print("\n🎉 Executable test completed successfully!")
        print("Your SPEED.exe is ready to use!")
    else:
        print("\n💥 Executable test failed.")
        sys.exit(1)