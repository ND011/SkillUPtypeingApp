#!/usr/bin/env python3
"""
Test script to check if statistics are working
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from ui.typing_interface import TypingInterface
from game.speed_engine import SpeedEngine
from game.database_manager import ScoreRecord
from datetime import datetime

def test_statistics():
    """Test the statistics functionality directly"""
    print("🔍 Testing Statistics Functionality")
    print("=" * 50)
    
    # Create QApplication
    app = QApplication(sys.argv)
    
    # Create speed engine and typing interface
    speed_engine = SpeedEngine()
    typing_interface = TypingInterface(speed_engine)
    
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
    
    print("📊 Testing statistics dialog directly...")
    
    # Test the statistics dialog directly
    try:
        typing_interface.show_session_statistics(fake_score)
        print("✅ Statistics dialog test completed!")
    except Exception as e:
        print(f"❌ Statistics dialog failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Test the leaderboard dialog
    try:
        print("🏆 Testing leaderboard dialog...")
        typing_interface.show_leaderboard()
        print("✅ Leaderboard dialog test completed!")
    except Exception as e:
        print(f"❌ Leaderboard dialog failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("🎉 Statistics test complete!")

if __name__ == "__main__":
    test_statistics()