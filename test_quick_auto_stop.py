#!/usr/bin/env python3
"""
Quick test to see auto-stop in action
"""

import sys
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from ui.typing_interface import TypingInterface
from game.speed_engine import SpeedEngine, GameMode, DifficultyLevel

def test_quick_auto_stop():
    """Test auto-stop with a very short session"""
    app = QApplication(sys.argv)
    
    # Create speed engine and typing interface
    speed_engine = SpeedEngine()
    typing_interface = TypingInterface(speed_engine)
    
    # Show the interface
    typing_interface.show()
    typing_interface.resize(800, 600)
    
    print("🚀 Testing auto-stop with 5-second session...")
    
    def start_quick_session():
        print("⏰ Starting session...")
        # Start a 1-minute session (will auto-stop at 59 seconds)
        success = speed_engine.start_time_based_session(
            "TestUser", 
            GameMode.TIMED_CHALLENGE, 
            DifficultyLevel.BEGINNER, 
            1  # 1 minute
        )
        
        if success:
            print("✅ Session started - should auto-stop in 59 seconds")
            print("🕘 Watch for auto-stop message and naming dialog...")
        else:
            print("❌ Failed to start session")
    
    # Start session after 1 second
    QTimer.singleShot(1000, start_quick_session)
    
    # Exit after 65 seconds to see the full process
    QTimer.singleShot(65000, app.quit)
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    test_quick_auto_stop()