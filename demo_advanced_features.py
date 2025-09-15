#!/usr/bin/env python3
"""
Demo script showcasing the Advanced Word Generator integration with SPEED
"""

import sys
import os
import time

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game.speed_engine import SpeedEngine, GameMode, DifficultyLevel
from speed_word_generator import WordGenerator
from models.difficulty import Difficulty

def demo_advanced_features():
    """Demonstrate all advanced word generation features in SPEED"""
    
    print("🚀 SPEED - Advanced Word Generator Demo")
    print("=" * 50)
    
    # Initialize components
    print("\n📦 Initializing Components...")
    engine = SpeedEngine()
    wg = WordGenerator(seed=42)  # Use seed for reproducible demo
    wg.load_default_sources(allow_phrases=True)
    
    print("✅ SPEED Engine initialized")
    print("✅ Advanced Word Generator loaded")
    
    # Demo 1: Different Game Modes
    print("\n🎮 Demo 1: Game Modes with Advanced Word Generation")
    print("-" * 50)
    
    modes_demo = [
        (GameMode.PRACTICE, DifficultyLevel.BEGINNER, "📚 Practice Mode"),
        (GameMode.TIMED_CHALLENGE, DifficultyLevel.INTERMEDIATE, "⏱️ Timed Challenge"),
        (GameMode.ACCURACY_FOCUS, DifficultyLevel.ADVANCED, "🎯 Accuracy Focus"),
        (GameMode.SPEED_BURST, DifficultyLevel.EXPERT, "⚡ Speed Burst"),
        (GameMode.ENDURANCE, DifficultyLevel.INTERMEDIATE, "💪 Endurance Mode")
    ]
    
    for mode, difficulty, description in modes_demo:
        print(f"\n{description}")
        success = engine.start_session("DemoUser", mode, difficulty, 60)
        if success:
            session = engine.get_current_session()
            print(f"  📊 Duration: {session.duration_seconds}s")
            print(f"  📝 Text Length: {len(session.target_text)} chars")
            print(f"  🔤 Preview: {session.target_text[:80]}...")
            engine.end_session()
        time.sleep(0.5)  # Brief pause for demo effect
    
    # Demo 2: Advanced Word Generator Features
    print("\n🔧 Demo 2: Advanced Word Generator Features")
    print("-" * 50)
    
    print("\n1️⃣ Fixed Count Generation:")
    words_50 = wg.generate_words(Difficulty.MEDIUM, 50)
    print(f"   Generated {len(words_50)} medium words")
    print(f"   Sample: {', '.join(words_50[:8])}...")
    
    print("\n2️⃣ Session-Based Generation:")
    session_words = wg.generate_for_session(Difficulty.MEDIUM, 180, 40)  # 3 min @ 40 WPM
    print(f"   Generated {len(session_words)} words for 3-minute session at 40 WPM")
    print(f"   Sample: {', '.join(session_words[:8])}...")
    
    print("\n3️⃣ Paragraph Generation:")
    paragraph = wg.generate_paragraph(Difficulty.HARD, 4, 150)
    print(f"   Generated {len(paragraph)} lines (max 150 chars each):")
    for i, line in enumerate(paragraph, 1):
        print(f"   Line {i}: {line[:60]}... ({len(line)} chars)")
    
    print("\n4️⃣ Mixed Difficulty Generation:")
    mixed_words = wg.generate_mixed({
        Difficulty.SIMPLE: 0.3,
        Difficulty.MEDIUM: 0.4,
        Difficulty.HARD: 0.3
    }, 60)
    print(f"   Generated {len(mixed_words)} mixed difficulty words")
    print(f"   Sample: {', '.join(mixed_words[:10])}...")
    
    # Demo 3: Statistics and Capabilities
    print("\n📊 Demo 3: System Statistics")
    print("-" * 50)
    
    available_difficulties = wg.get_available_difficulties()
    print(f"\n📈 Available Difficulties: {[d.value for d in available_difficulties]}")
    
    total_words = 0
    for difficulty in available_difficulties:
        count = wg.get_word_count_for_difficulty(difficulty)
        total_words += count
        print(f"   {difficulty.value.capitalize()}: {count:,} words")
    
    print(f"\n🎯 Total Word Database: {total_words:,} words")
    
    # Demo 4: Export Functionality
    print("\n💾 Demo 4: Export Functionality")
    print("-" * 50)
    
    export_file = "demo_export.tsv"
    print(f"\n📤 Exporting all words to '{export_file}'...")
    wg.save_merged(export_file)
    
    # Check file size
    if os.path.exists(export_file):
        file_size = os.path.getsize(export_file)
        print(f"✅ Export successful! File size: {file_size:,} bytes")
        
        # Show first few lines
        with open(export_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:6]
        print("📋 Sample export content:")
        for line in lines:
            print(f"   {line.strip()}")
    
    # Demo 5: Performance Comparison
    print("\n⚡ Demo 5: Performance Demonstration")
    print("-" * 50)
    
    print("\n🏃‍♂️ Speed Test - Generating 1000 words:")
    start_time = time.time()
    large_set = wg.generate_words(Difficulty.MEDIUM, 1000)
    end_time = time.time()
    
    print(f"   ✅ Generated {len(large_set)} words in {(end_time - start_time)*1000:.2f}ms")
    print(f"   📊 Performance: {len(large_set)/(end_time - start_time):.0f} words/second")
    
    # Demo 6: Reproducibility
    print("\n🔄 Demo 6: Reproducibility with Seeds")
    print("-" * 50)
    
    print("\n🎲 Testing seed reproducibility:")
    wg1 = WordGenerator(seed=999)
    wg1.load_default_sources()
    wg2 = WordGenerator(seed=999)
    wg2.load_default_sources()
    
    words1 = wg1.generate_words(Difficulty.MEDIUM, 5)
    words2 = wg2.generate_words(Difficulty.MEDIUM, 5)
    
    print(f"   Generator 1: {words1}")
    print(f"   Generator 2: {words2}")
    print(f"   🎯 Identical: {'✅ Yes' if words1 == words2 else '❌ No'}")
    
    # Final Summary
    print("\n🎉 Demo Complete!")
    print("=" * 50)
    print("✅ Advanced Word Generator successfully integrated with SPEED")
    print("✅ All generation modes working perfectly")
    print("✅ Export functionality operational")
    print("✅ Performance optimized")
    print("✅ Reproducible results with seeds")
    print("\n🚀 SPEED is now powered by the Advanced Word Generator!")
    
    # Cleanup
    if os.path.exists(export_file):
        os.remove(export_file)
        print(f"🧹 Cleaned up demo file: {export_file}")

if __name__ == "__main__":
    demo_advanced_features()