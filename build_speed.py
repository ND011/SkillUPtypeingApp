#!/usr/bin/env python3
"""
Build script for creating SPEED executable
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import logging

def setup_logging():
    """Set up logging for the build process"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('build.log'),
            logging.StreamHandler()
        ]
    )

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = ['PyQt6', 'pyinstaller']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'PyQt6':
                import PyQt6
            elif package == 'pyinstaller':
                import PyInstaller
            logging.info(f"[OK] {package} is installed")
        except ImportError:
            missing_packages.append(package)
            logging.error(f"[MISSING] {package} is missing")
    
    if missing_packages:
        logging.error(f"Missing packages: {', '.join(missing_packages)}")
        logging.info("Install them with: pip install " + " ".join(missing_packages))
        return False
    
    return True

def clean_build_dirs():
    """Clean previous build directories"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            logging.info(f"Cleaning {dir_name}...")
            shutil.rmtree(dir_name)
    
    # Clean pycache in subdirectories
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                pycache_path = os.path.join(root, dir_name)
                logging.info(f"Cleaning {pycache_path}...")
                shutil.rmtree(pycache_path)

def create_spec_file():
    """Create PyInstaller spec file for SPEED"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtWidgets', 
        'PyQt6.QtGui',
        'ui.main_window',
        'ui.typing_interface',
        'ui.statistics_widget',
        'ui.leaderboard_widget',
        'ui.theme_manager',
        'ui.settings_dialog',
        'ui.user_profile_dialog',
        'models.user_models',
        'game.speed_engine',
        'game.database_manager',
        'game.word_manager',
        'game.performance_calculator'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'tkinter',
        'jupyter',
        'IPython',
        'notebook'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SPEED',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if you have one
    version_file=None,  # Add version file here if needed
)
'''
    
    with open('speed.spec', 'w') as f:
        f.write(spec_content)
    
    logging.info("✓ Created PyInstaller spec file")

def build_executable():
    """Build the executable using PyInstaller"""
    logging.info("Building SPEED executable...")
    
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--clean',
        '--noconfirm',
        'speed.spec'
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        logging.info("✓ Build completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"✗ Build failed with error: {e}")
        logging.error("STDOUT:", e.stdout)
        logging.error("STDERR:", e.stderr)
        return False

def verify_executable():
    """Verify that the executable was created"""
    exe_path = Path('dist/SPEED.exe')
    
    if not exe_path.exists():
        logging.error("✗ Executable not found!")
        return False
    
    file_size_mb = exe_path.stat().st_size / (1024*1024)
    logging.info(f"✓ Executable created: {exe_path}")
    logging.info(f"✓ File size: {file_size_mb:.1f} MB")
    
    return True

def create_distribution_folder():
    """Create a clean distribution folder"""
    dist_folder = Path('SPEED_Distribution')
    
    if dist_folder.exists():
        shutil.rmtree(dist_folder)
    
    dist_folder.mkdir()
    
    # Copy executable
    exe_source = Path('dist/SPEED.exe')
    if exe_source.exists():
        shutil.copy2(exe_source, dist_folder / 'SPEED.exe')
        logging.info(f"✓ Copied executable to {dist_folder}")
    
    # Create README
    readme_content = """# SPEED - Keyboard Speed Training

## 🚀 Advanced Typing Practice Application

SPEED is a professional keyboard speed training application with multiple game modes, comprehensive statistics, and beautiful themes.

## ✨ Features

### Multiple Practice Modes
- **Practice Mode**: Standard typing practice with customizable difficulty
- **Timed Challenge**: Competitive timed sessions
- **Accuracy Focus**: Specialized training for precision
- **Speed Burst**: Quick speed building sessions
- **Endurance Mode**: Extended stamina training

### Difficulty Levels
- **Beginner**: 3-6 character common words
- **Intermediate**: 5-10 character moderate complexity
- **Advanced**: 8-15 character complex vocabulary
- **Expert**: 10+ character highly complex words

### Advanced Features
- **Real-time Performance Tracking**: Live WPM and accuracy
- **Comprehensive Statistics**: Detailed analytics and progress tracking
- **Achievement System**: Unlock rewards for milestones
- **Leaderboards**: Compare performance with others
- **Multiple Themes**: 5 beautiful themes including Dark mode
- **Database Storage**: Persistent progress tracking

### Theme System
- **Default**: Clean, professional light theme
- **Dark**: Easy on the eyes for extended practice
- **High Contrast**: Accessibility-focused design
- **Ocean Blue**: Calming blue color scheme
- **Forest Green**: Natural green theme

## 🎯 Quick Start

1. **Double-click SPEED.exe** to launch the application
2. **Choose your difficulty level** (Beginner recommended for first use)
3. **Select a practice mode** from the Practice tab
4. **Start typing** and watch your real-time performance
5. **View your progress** in the Statistics tab
6. **Check rankings** in the Leaderboard tab

## 🌙 Theme Switching

- **Quick Toggle**: Click the 🌙/☀️ button in the header
- **Keyboard Shortcut**: Press Ctrl+T
- **Menu Option**: Settings → Theme

## 📊 Performance Metrics

- **WPM**: Words per minute (standard 5-character definition)
- **Accuracy**: Percentage of correctly typed characters
- **Consistency**: Measure of typing rhythm stability
- **Progress**: Real-time completion tracking

## 🎮 Game Modes

- **Practice**: Standard typing with adjustable duration
- **Timed Challenge**: Competitive mode with mixed difficulty
- **Accuracy Focus**: Precision training with tricky words
- **Speed Burst**: Short, intense speed building (15-60s)
- **Endurance**: Extended sessions for stamina (5-30min)

## 🏆 Achievement System

Unlock achievements for:
- Speed milestones (50, 75, 100+ WPM)
- Accuracy achievements (95%, 98%, 100%)
- Consistency rewards
- Practice streaks
- Special accomplishments

## 💡 Tips for Improvement

1. **Start with Practice Mode** on Beginner difficulty
2. **Focus on accuracy first**, then build speed
3. **Use the Dark theme** for extended practice sessions
4. **Practice regularly** to build muscle memory
5. **Check Statistics** to track your improvement
6. **Try different modes** to challenge yourself

## 🔧 System Requirements

- **Windows 10 or later**
- **No additional installation required**
- **No internet connection needed**
- **Approximately 40MB disk space**

## 🎉 Ready to Practice!

SPEED combines proven typing methodologies with modern technology to help you achieve your keyboard speed goals. Whether you're a beginner or looking to push your limits, SPEED provides the tools and motivation you need.

**Start your journey to typing mastery today!**

---

Version: 3.0
Built: February 2025
"""
    
    with open(dist_folder / 'README.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    # Create launcher batch file
    launcher_content = """@echo off
echo Starting SPEED - Keyboard Speed Training...
echo.

REM Check if executable exists
if not exist "SPEED.exe" (
    echo Error: SPEED.exe not found!
    echo Make sure this file is in the same folder as SPEED.exe
    pause
    exit /b 1
)

REM Launch SPEED
echo Launching application...
start "" "SPEED.exe"

REM Optional: Close this window after launch
timeout /t 2 /nobreak >nul
echo SPEED started successfully!
echo You can close this window now.
"""
    
    with open(dist_folder / 'Launch_SPEED.bat', 'w') as f:
        f.write(launcher_content)
    
    logging.info(f"✓ Created distribution folder: {dist_folder}")
    return dist_folder

def create_installer_info():
    """Create installation and sharing instructions"""
    info_content = """# 📦 SPEED Distribution Package

## ✅ Ready to Share!

This folder contains everything needed to run SPEED on any Windows computer.

## 📁 Contents

- **SPEED.exe** - Main application (standalone executable)
- **README.txt** - User guide and features overview
- **Launch_SPEED.bat** - Optional launcher script
- **How_to_Share.txt** - This file with sharing instructions

## 🚀 How to Share

### Method 1: Share the Entire Folder
1. **Zip the SPEED_Distribution folder**
2. **Send the zip file** to others via email, cloud storage, or USB
3. **Recipients extract** and run SPEED.exe

### Method 2: Share Just the Executable
1. **Send only SPEED.exe** (approximately 40MB)
2. **Recipients run it directly** - no installation needed

### Method 3: USB/Network Drive
1. **Copy the folder** to a USB drive or network location
2. **Others can run** SPEED.exe directly from the drive
3. **Or copy to their computer** for permanent installation

## 💡 Sharing Tips

### For Recipients
- **No installation required** - just double-click SPEED.exe
- **Works on Windows 10 and later**
- **No internet connection needed**
- **All data stored locally** - completely private

### Troubleshooting
- **Windows Defender warning**: Normal for new executables - click "More info" → "Run anyway"
- **Antivirus alerts**: Add SPEED.exe to antivirus exceptions (false positive)
- **Won't start**: Try running as administrator
- **Missing features**: Make sure to share the complete folder, not just the .exe

### File Sizes
- **SPEED.exe**: ~40MB (complete application)
- **Full folder**: ~40MB (includes documentation)
- **Zipped folder**: ~15MB (compressed for sharing)

## 🎯 What Recipients Get

### Complete Typing Practice Suite
- **5 Game Modes**: Practice, Challenge, Accuracy, Speed Burst, Endurance
- **4 Difficulty Levels**: Beginner to Expert
- **1000+ Words**: Comprehensive vocabulary database
- **Real-time Analytics**: WPM, accuracy, consistency tracking
- **Achievement System**: Unlock rewards and milestones
- **5 Beautiful Themes**: Including professional Dark mode
- **Statistics Tracking**: Detailed progress analysis
- **Leaderboards**: Performance comparison

### Professional Features
- **Database Storage**: All progress saved automatically
- **Theme Switching**: Instant dark/light mode toggle (Ctrl+T)
- **Keyboard Shortcuts**: Professional workflow support
- **Accessibility**: High contrast theme for visual impairments
- **Performance Optimized**: Smooth, responsive operation

## 🌟 Perfect For

- **Students**: Improve typing for academic work
- **Professionals**: Enhance workplace productivity
- **Gamers**: Build speed for competitive gaming
- **Anyone**: Learn touch typing or improve existing skills

## 🎉 Success!

Your SPEED application is now ready for distribution! Recipients will have access to a professional-grade typing practice tool that rivals commercial software.

**Share the joy of improved typing skills!**

---

*Built with ❤️ for the typing community*
"""
    
    dist_folder = Path('SPEED_Distribution')
    with open(dist_folder / 'How_to_Share.txt', 'w', encoding='utf-8') as f:
        f.write(info_content)
    
    logging.info("✓ Created sharing instructions")

def main():
    """Main build process"""
    setup_logging()
    logging.info("=== SPEED Executable Build Process ===")
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    # Clean previous builds
    clean_build_dirs()
    
    # Create spec file
    create_spec_file()
    
    # Build executable
    if not build_executable():
        return 1
    
    # Verify executable
    if not verify_executable():
        return 1
    
    # Create distribution folder
    dist_folder = create_distribution_folder()
    
    # Create sharing instructions
    create_installer_info()
    
    logging.info("\n=== Build Complete! ===")
    logging.info(f"✓ Executable ready: {dist_folder}/SPEED.exe")
    logging.info(f"✓ Distribution folder: {dist_folder}")
    logging.info("✓ README and instructions included")
    logging.info("\n🎉 SPEED is ready to share!")
    logging.info(f"📁 Share the '{dist_folder}' folder with others")
    logging.info("📧 Or zip it and send via email/cloud storage")
    logging.info("💾 Recipients just need to run SPEED.exe - no installation required!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())