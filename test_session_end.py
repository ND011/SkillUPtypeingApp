#!/usr/bin/env python3
"""
Test script to trigger session end and see debug output
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QMainWindow
from ui.typing_interface import TypingInterface
from game.speed_engine import SpeedEngine
from game.database_manager import ScoreRecord
from datetime import datetime

def test_session_end():
    """Test session end to see debug output"""
    print("🔍 Testing Session End Debug")
    print("=" * 50)
    
    # Create QApplication
    app = QApplication(sys.argv)
    
    # Create speed engine and typing interface
    speed_engine = SpeedEngine()
    typing_interface = TypingInterface(speed_engine)
    
    # Create main window
    main_window = QMainWindow()
    main_window.setWindowTitle("SPEED - Session End Test")
    main_window.setCentralWidget(typing_interface)
    main_window.resize(800, 600)
    main_window.show()
    
    # Create a fake score record for testing
    fake_score = ScoreRecord(
        id=None,
        user_name="TestUser",
        wpm=75.5,
        accuracy=92.3,
        mode="timed_challenge",
        level="intermediate",
        date=datetime.now(),
        duration=60,
        total_characters=450,
        correct_characters=415
    )
    
    print("🎯 Triggering session end with fake score...")
    
    # Trigger session end directly
    typing_interface.on_session_end(fake_score)
    
    print("✅ Session end test completed!")
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(test_session_end())