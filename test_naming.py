#!/usr/bin/env python3
"""
Test script to verify naming dialog functionality
"""

import sys
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from ui.typing_interface import TypingInterface
from game.speed_engine import SpeedEngine, GameMode, DifficultyLevel

def test_naming_dialog():
    """Test that naming dialog appears after session ends"""
    app = QApplication(sys.argv)
    
    # Create speed engine and typing interface
    speed_engine = SpeedEngine()
    typing_interface = TypingInterface(speed_engine)
    
    # Show the interface
    typing_interface.show()
    typing_interface.resize(800, 600)
    
    print("🚀 Starting test session...")
    
    # Start a short 5-second session for testing
    def start_test_session():
        print("⏰ Starting 5-second test session...")
        # Start a very short session (5 seconds) to test the naming dialog
        success = speed_engine.start_time_based_session(
            "TestUser", 
            GameMode.TIMED_CHALLENGE, 
            DifficultyLevel.BEGINNER, 
            1  # 1 minute, but we'll end it early
        )
        
        if success:
            print("✅ Session started successfully")
            # End the session after 5 seconds to trigger the naming dialog
            QTimer.singleShot(5000, lambda: speed_engine.end_session())
        else:
            print("❌ Failed to start session")
    
    # Start the test session after a short delay
    QTimer.singleShot(1000, start_test_session)
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    test_naming_dialog()