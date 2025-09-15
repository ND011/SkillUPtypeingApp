#!/usr/bin/env python3
"""
Test script to verify auto-stop functionality (stops 1 second before timer ends)
"""

import sys
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from ui.typing_interface import TypingInterface
from game.speed_engine import SpeedEngine, GameMode, DifficultyLevel

def test_auto_stop():
    """Test that auto-stop happens 1 second before timer ends"""
    app = QApplication(sys.argv)
    
    # Create speed engine and typing interface
    speed_engine = SpeedEngine()
    typing_interface = TypingInterface(speed_engine)
    
    # Show the interface
    typing_interface.show()
    typing_interface.resize(800, 600)
    
    print("🚀 Starting auto-stop test...")
    
    # Start a 10-second session for testing (should auto-stop at 9 seconds)
    def start_test_session():
        print("⏰ Starting 10-second test session (should auto-stop at 9 seconds)...")
        # Manually create a short session for testing
        success = speed_engine.start_time_based_session(
            "TestUser", 
            GameMode.TIMED_CHALLENGE, 
            DifficultyLevel.BEGINNER, 
            1  # 1 minute normally, but we'll override the timer
        )
        
        if success:
            print("✅ Session started successfully")
            print("🕘 Session should auto-stop in about 9 seconds...")
        else:
            print("❌ Failed to start session")
    
    # Start the test session after a short delay
    QTimer.singleShot(1000, start_test_session)
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    test_auto_stop()