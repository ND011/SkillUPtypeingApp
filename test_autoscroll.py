#!/usr/bin/env python3
"""
Test script to demonstrate the auto-scroll feature
"""
import sys
import os
# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from ui.typing_interface import TypingInterface
from game.speed_engine import SpeedEngine

def test_autoscroll():
    """Test the auto-scroll functionality"""
    print("🔍 Testing Auto-Scroll Feature")
    print("=" * 50)
    
    # Create QApplication
    app = QApplication(sys.argv)
    
    # Create speed engine
    speed_engine = SpeedEngine()
    
    # Create typing interface
    typing_interface = TypingInterface(speed_engine)
    
    # Create main window
    main_window = QMainWindow()
    main_window.setWindowTitle("SPEED - Auto-Scroll Test")
    main_window.setCentralWidget(typing_interface)
    main_window.resize(800, 600)
    main_window.show()
    
    print("✅ Auto-scroll test window created!")
    print("📝 Instructions:")
    print("   1. Click 'Start Session' to begin")
    print("   2. Start typing - notice the text scrolls automatically")
    print("   3. The current typing position is highlighted in blue")
    print("   4. Correct characters are highlighted in green")
    print("   5. Incorrect characters are highlighted in red")
    print("   6. The text automatically scrolls to keep your position visible")
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(test_autoscroll())