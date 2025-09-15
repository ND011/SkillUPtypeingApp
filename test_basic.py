#!/usr/bin/env python3
"""
Basic test to verify SPEED application components work
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all main components can be imported"""
    try:
        print("Testing imports...")
        
        # Test game components
        from game.database_manager import DatabaseManager
        from game.speed_engine import SpeedEngine, GameMode, DifficultyLevel
        from game.word_manager import WordManager
        from game.performance_calculator import PerformanceCalculator
        print("✓ Game components imported successfully")
        
        # Test models
        from models.user_models import UserProfile, UserLevel, Theme
        print("✓ User models imported successfully")
        
        # Test UI components (basic imports)
        from ui.theme_manager import ThemeManager
        print("✓ UI components imported successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality of core components"""
    try:
        print("\nTesting basic functionality...")
        
        # Import components for testing
        from game.database_manager import DatabaseManager
        from game.word_manager import WordManager
        from game.performance_calculator import PerformanceCalculator
        from game.speed_engine import DifficultyLevel
        from ui.theme_manager import ThemeManager
        from models.user_models import UserProfile, UserLevel
        
        # Test database manager
        db_manager = DatabaseManager(":memory:")  # Use in-memory database for testing
        if db_manager.initialize():
            print("✓ Database manager initialized")
        else:
            print("✗ Database manager failed to initialize")
            return False
        
        # Test word manager
        word_manager = WordManager()
        practice_text = word_manager.get_practice_text(DifficultyLevel.BEGINNER, 60)
        if practice_text and len(practice_text) > 0:
            print("✓ Word manager generated practice text")
        else:
            print("✗ Word manager failed to generate text")
            return False
        
        # Test performance calculator
        perf_calc = PerformanceCalculator()
        wpm = perf_calc.calculate_wpm("hello world", 10.0)
        accuracy = perf_calc.calculate_accuracy("hello world", "hello world")
        if wpm > 0 and accuracy == 100.0:
            print("✓ Performance calculator working")
        else:
            print("✗ Performance calculator failed")
            return False
        
        # Test theme manager
        theme_manager = ThemeManager()
        themes = theme_manager.get_available_themes()
        if len(themes) > 0:
            print("✓ Theme manager loaded themes")
        else:
            print("✗ Theme manager failed to load themes")
            return False
        
        # Test user profile
        user_profile = UserProfile("test_user", "Test User", UserLevel.BEGINNER)
        if user_profile.username == "test_user":
            print("✓ User profile created successfully")
        else:
            print("✗ User profile creation failed")
            return False
        
        # Clean up
        db_manager.close()
        
        return True
        
    except Exception as e:
        print(f"✗ Functionality test error: {e}")
        return False

def test_speed_engine():
    """Test the speed engine functionality"""
    try:
        print("\nTesting speed engine...")
        
        # Import speed engine components
        from game.speed_engine import SpeedEngine, GameMode, DifficultyLevel
        
        speed_engine = SpeedEngine()
        
        # Test session creation
        success = speed_engine.start_session(
            "test_user", 
            GameMode.PRACTICE, 
            DifficultyLevel.BEGINNER, 
            5  # 5 seconds for quick test
        )
        
        if success:
            print("✓ Speed engine session started")
        else:
            print("✗ Speed engine session failed to start")
            return False
        
        # Test session status
        if speed_engine.is_session_active():
            print("✓ Speed engine session is active")
        else:
            print("✗ Speed engine session not active")
            return False
        
        # Test text update
        speed_engine.update_typed_text("hello")
        current_session = speed_engine.get_current_session()
        if current_session and current_session.typed_text == "hello":
            print("✓ Speed engine text update working")
        else:
            print("✗ Speed engine text update failed")
            return False
        
        # Clean up
        speed_engine.cleanup()
        
        return True
        
    except Exception as e:
        print(f"✗ Speed engine test error: {e}")
        return False

def main():
    """Run all tests"""
    print("=== SPEED Application Basic Tests ===\n")
    
    tests_passed = 0
    total_tests = 3
    
    # Run tests
    if test_imports():
        tests_passed += 1
    
    if test_basic_functionality():
        tests_passed += 1
    
    if test_speed_engine():
        tests_passed += 1
    
    # Results
    print(f"\n=== Test Results ===")
    print(f"Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("✓ All tests passed! SPEED application is ready.")
        return 0
    else:
        print("✗ Some tests failed. Check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())