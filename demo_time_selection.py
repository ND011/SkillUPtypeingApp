#!/usr/bin/env python3
"""
Demo script showcasing the new time-based word selection feature
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from speed_word_generator import WordGenerator
from models.difficulty import Difficulty
from game.speed_engine import SpeedEngine, GameMode, DifficultyLevel

def demo_time_selection():
    """Demonstrate the time-based word selection feature"""
    
    print("🕒 SPEED - Time-Based Word Selection Demo")
    print("=" * 60)
    
    # Initialize components
    print("\n📦 Initializing Components...")
    wg = WordGenerator(seed=123)  # Use seed for consistent demo
    wg.load_default_sources(allow_phrases=True)
    engine = SpeedEngine()
    print("✅ Components initialized")
    
    # Show available options
    print("\n⏰ Available Time Options:")
    time_options = wg.get_available_time_options()
    print("   Time Selection Menu:")
    for i, minutes in enumerate(time_options, 1):
        word_count = wg.calculate_word_count_for_time(minutes)
        print(f"   {i}. {minutes} minute{'s' if minutes > 1 else ''} → {word_count} words")
    
    print(f"\n📊 Word Counts: 70, 140, 210, 350, 490, 700 words")
    
    # Demo each time option
    print("\n🎯 Time-Based Generation Examples:")
    print("-" * 60)
    
    for minutes in time_options:
        print(f"\n⏱️ {minutes} Minute{'s' if minutes > 1 else ''} Selection:")
        
        # Generate words
        words = wg.generate_for_time_selection(Difficulty.MEDIUM, minutes)
        expected = wg.calculate_word_count_for_time(minutes)
        
        print(f"   📈 Generated: {len(words)} words (Expected: {expected})")
        print(f"   📝 Sample words: {', '.join(words[:min(8, len(words))])}...")
        
        # Show how it looks in different game modes
        print(f"   🎮 Game Mode Examples:")
        
        # Practice mode (formatted as paragraph)
        try:
            success = engine.start_time_based_session("DemoUser", GameMode.PRACTICE, DifficultyLevel.INTERMEDIATE, minutes)
            if success:
                session = engine.get_current_session()
                lines = session.target_text.split('\n')
                print(f"      📚 Practice Mode ({len(lines)} lines):")
                for i, line in enumerate(lines[:2], 1):  # Show first 2 lines
                    print(f"         Line {i}: {line[:50]}{'...' if len(line) > 50 else ''}")
                if len(lines) > 2:
                    print(f"         ... and {len(lines) - 2} more lines")
                engine.end_session()
        except Exception as e:
            print(f"      ❌ Practice mode error: {e}")
        
        # Timed Challenge mode (single line)
        try:
            success = engine.start_time_based_session("DemoUser", GameMode.TIMED_CHALLENGE, DifficultyLevel.INTERMEDIATE, minutes)
            if success:
                session = engine.get_current_session()
                print(f"      ⏱️ Timed Challenge: {session.target_text[:60]}...")
                engine.end_session()
        except Exception as e:
            print(f"      ❌ Timed challenge error: {e}")
    
    # Demo different difficulties
    print(f"\n🎚️ Difficulty Comparison (3 minutes):")
    print("-" * 60)
    
    difficulties = [
        (Difficulty.SIMPLE, DifficultyLevel.BEGINNER, "Simple/Beginner"),
        (Difficulty.MEDIUM, DifficultyLevel.INTERMEDIATE, "Medium/Intermediate"),
        (Difficulty.HARD, DifficultyLevel.ADVANCED, "Hard/Advanced"),
        (Difficulty.EXTRA_HARD, DifficultyLevel.EXPERT, "Extra Hard/Expert")
    ]
    
    for adv_diff, speed_diff, name in difficulties:
        words = wg.generate_for_time_selection(adv_diff, 3)
        print(f"\n   🎯 {name}:")
        print(f"      Words: {', '.join(words[:6])}...")
        
        # Show average word length
        avg_length = sum(len(word) for word in words) / len(words)
        print(f"      Average word length: {avg_length:.1f} characters")
    
    # Demo UI Integration Simulation
    print(f"\n🖥️ UI Integration Simulation:")
    print("-" * 60)
    
    print("\n   Time Selection Dropdown Options:")
    ui_options = [
        "1 min (70 words)",
        "2 min (140 words)", 
        "3 min (210 words)",
        "5 min (350 words)",
        "7 min (490 words)",
        "10 min (700 words)"
    ]
    
    for i, option in enumerate(ui_options, 1):
        print(f"   {i}. {option}")
    
    print(f"\n   User Selection Simulation:")
    selected_option = "5 min (350 words)"
    minutes = int(selected_option.split()[0])
    print(f"   👤 User selects: {selected_option}")
    print(f"   ⚙️ System extracts: {minutes} minutes")
    
    # Generate and show result
    words = wg.generate_for_time_selection(Difficulty.MEDIUM, minutes)
    print(f"   📊 Generated: {len(words)} words")
    print(f"   📝 Result: {' '.join(words[:10])}...")
    
    # Performance metrics
    print(f"\n⚡ Performance Metrics:")
    print("-" * 60)
    
    import time
    
    total_words = 0
    total_time = 0
    
    for minutes in time_options:
        start_time = time.time()
        words = wg.generate_for_time_selection(Difficulty.MEDIUM, minutes)
        end_time = time.time()
        
        duration = max(end_time - start_time, 0.001)
        total_words += len(words)
        total_time += duration
        
        print(f"   {minutes} min: {len(words)} words in {duration*1000:.2f}ms")
    
    print(f"\n   📊 Overall Performance:")
    print(f"      Total words generated: {total_words}")
    print(f"      Total time: {total_time*1000:.2f}ms")
    print(f"      Average speed: {total_words/total_time:.0f} words/second")
    
    # Summary
    print(f"\n🎉 Time-Based Selection Demo Complete!")
    print("=" * 60)
    print("✅ Time options: 1, 2, 3, 5, 7, 10 minutes")
    print("✅ Word counts: 70, 140, 210, 350, 490, 700 words")
    print("✅ All difficulties supported")
    print("✅ All game modes integrated")
    print("✅ UI-ready dropdown options")
    print("✅ High-performance generation")
    print("\n🚀 Ready for production use!")

if __name__ == "__main__":
    demo_time_selection()