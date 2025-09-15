#!/usr/bin/env python3
"""
Build script to create SPEED executable
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_executable():
    """Build the SPEED executable using PyInstaller"""
    print("🚀 Building Fspeed Executable")
    print("=" * 50)
    
    # Clean previous builds
    if os.path.exists("build"):
        print("🧹 Cleaning previous build directory...")
        shutil.rmtree("build")
    
    if os.path.exists("dist"):
        print("🧹 Cleaning previous dist directory...")
        shutil.rmtree("dist")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Create single executable
        "--windowed",  # No console window
        "--name=Fspeed",  # Executable name
        "--icon=icon.ico" if os.path.exists("icon.ico") else "",  # Icon if available
        "--add-data=simple_words_large.txt;.",  # Include word files
        "--add-data=medium_unique_words.txt;.",
        "--add-data=hard_words_expanded.txt;.",
        "--add-data=extra_hard_words_extended.txt;.",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=sqlite3",
        "main.py"
    ]
    
    # Remove empty icon parameter if no icon exists
    cmd = [arg for arg in cmd if arg]
    
    print("📦 Running PyInstaller...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build successful!")
        print(result.stdout)
        
        # Check if executable was created
        exe_path = Path("dist/Fspeed.exe")
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"🎉 Executable created: {exe_path}")
            print(f"📏 Size: {size_mb:.1f} MB")
            
            # Copy word files to dist directory for testing
            word_files = [
                "simple_words_large.txt",
                "medium_unique_words.txt", 
                "hard_words_expanded.txt",
                "extra_hard_words_extended.txt"
            ]
            
            for word_file in word_files:
                if os.path.exists(word_file):
                    shutil.copy2(word_file, "dist/")
                    print(f"📄 Copied {word_file} to dist/")
            
            print("\n🎯 Build Complete!")
            print(f"Your executable is ready at: {exe_path.absolute()}")
            
        else:
            print("❌ Executable not found in dist directory")
            
    except subprocess.CalledProcessError as e:
        print("❌ Build failed!")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False
    
    return True

if __name__ == "__main__":
    success = build_executable()
    if success:
        print("\n✨ You can now run Fspeed.exe from the dist folder!")
    else:
        print("\n💥 Build failed. Check the error messages above.")
        sys.exit(1)