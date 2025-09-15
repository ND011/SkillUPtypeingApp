#!/usr/bin/env python3
"""
Test script to simulate a complete session and check statistics
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QMainWindow
from ui.typing_interface import TypingInterface
from game.speed_engine import SpeedEngine
import time

def test_complete_session():
    """Test a complete session to see if statistics appear"""
    print("🔍 Testing Complete Session with Statistics")
    print("=" * 50)
    
    # Create QApplication
    app = QApplication(sys.argv)
    
    # Create speed engine and typing interface
    speed_engine = SpeedEngine()
    typing_interface = TypingInterface(speed_engine)
    
    # Create main window
    main_window = QMainWindow()
    main_window.setWindowTitle("SPEED - Session Test")
    main_window.setCentralWidget(typing_interface)
    main_window.resize(800, 600)
    main_window.show()
    
    print("✅ Application window created and shown")
    print("📝 Instructions:")
    print("   1. Click 'Start' to begin a session")
    print("   2. Type a few words (don't need to complete)")
    print("   3. Click 'Stop' to end the session")
    print("   4. Check if statistics dialog appears")
    print("   5. Close the application when done")
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(test_complete_session())