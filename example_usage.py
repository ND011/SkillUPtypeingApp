#!/usr/bin/env python3
"""
Example usage of the Advanced Word Generator
This script demonstrates all the generation methods available
"""

from speed_word_generator import WordGenerator
from models.difficulty import Difficulty

def main():
    """Demonstrate all word generation features"""
    
    print("=== Advanced Word Generator Example ===\n")
    
    # Initialize the word generator with a seed for reproducible results
    wg = WordGenerator(seed=7)
    
    # Load default word sources with phrase support
    print("Loading default word sources...")
    wg.load_default_sources(allow_phrases=True)  # keeps lines as-is, including phrases
    print("✓ Word sources loaded successfully\n")
    
    # 1) 50 medium words
    print("1. Generating 50 medium words:")
    words = wg.generate_words(Difficulty.MEDIUM, count=50)
    print(f"   Generated {len(words)} words")
    print(f"   Sample: {', '.join(words[:10])}...")
    print()
    
    # 2) Time-sized set: 3 minutes @ 40 WPM (+10% buffer)
    print("2. Generating words for 3-minute session at 40 WPM:")
    session_words = wg.generate_for_session(Difficulty.MEDIUM, duration_seconds=180, target_wpm=40)
    print(f"   Generated {len(session_words)} words (includes 10% buffer)")
    print(f"   Sample: {', '.join(session_words[:10])}...")
    print()
    
    # 3) Paragraph for hard difficulty (6 lines, ~200 chars/line)
    print("3. Generating paragraph (6 lines, max 200 chars/line):")
    para_lines = wg.generate_paragraph(Difficulty.HARD, lines=6, max_line_chars=200)
    print(f"   Generated {len(para_lines)} lines:")
    for i, line in enumerate(para_lines, 1):
        print(f"   Line {i} ({len(line)} chars): {line}")
    print()
    
    # 4) Mixed difficulties: 50% medium, 30% hard, 20% extra-hard; total 120 words
    print("4. Generating mixed difficulty words:")
    mixed = wg.generate_mixed(
        weights={
            Difficulty.MEDIUM: 0.5, 
            Difficulty.HARD: 0.3, 
            Difficulty.EXTRA_HARD: 0.2
        },
        total_count=120
    )
    print(f"   Generated {len(mixed)} mixed difficulty words")
    print(f"   Sample: {', '.join(mixed[:15])}...")
    print()
    
    # 5) Save merged (tsv: difficulty\tentry)
    print("5. Saving merged word list to TSV file:")
    output_filename = "merged_words.tsv"
    wg.save_merged(output_filename)
    print(f"   ✓ Saved all words to '{output_filename}'")
    
    # Display some statistics
    print("\n=== Statistics ===")
    available_difficulties = wg.get_available_difficulties()
    print(f"Available difficulties: {[d.value for d in available_difficulties]}")
    
    for difficulty in available_difficulties:
        count = wg.get_word_count_for_difficulty(difficulty)
        print(f"  {difficulty.value}: {count} words available")
    
    print("\n=== Advanced Features Demo ===")
    
    # Demonstrate reproducibility with seeds
    print("\n6. Demonstrating seed reproducibility:")
    wg1 = WordGenerator(seed=42)
    wg1.load_default_sources()
    wg2 = WordGenerator(seed=42)
    wg2.load_default_sources()
    
    words1 = wg1.generate_words(Difficulty.MEDIUM, 10)
    words2 = wg2.generate_words(Difficulty.MEDIUM, 10)
    
    print(f"   Generator 1: {words1}")
    print(f"   Generator 2: {words2}")
    print(f"   Identical: {words1 == words2}")
    
    # Demonstrate different generation strategies
    print("\n7. Comparing generation strategies:")
    
    # Short session vs long session
    short_session = wg.generate_for_session(Difficulty.MEDIUM, 60, 30)  # 1 min, 30 WPM
    long_session = wg.generate_for_session(Difficulty.MEDIUM, 300, 60)  # 5 min, 60 WPM
    
    print(f"   Short session (1 min @ 30 WPM): {len(short_session)} words")
    print(f"   Long session (5 min @ 60 WPM): {len(long_session)} words")
    
    # Different paragraph formats
    short_lines = wg.generate_paragraph(Difficulty.SIMPLE, 3, 50)
    long_lines = wg.generate_paragraph(Difficulty.SIMPLE, 2, 150)
    
    print(f"\n   Short lines (3 lines, 50 chars max):")
    for line in short_lines:
        print(f"     '{line}' ({len(line)} chars)")
    
    print(f"\n   Long lines (2 lines, 150 chars max):")
    for line in long_lines:
        print(f"     '{line}' ({len(line)} chars)")
    
    print("\n=== Example Complete ===")
    print("Check 'merged_words.tsv' for the exported word list!")


if __name__ == "__main__":
    main()