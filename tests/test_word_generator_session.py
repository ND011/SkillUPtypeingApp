"""
Unit tests for session-based word generation
"""

import unittest
from unittest.mock import Mock, patch
from speed_word_generator import WordGenerator
from models.difficulty import Difficulty


class TestWordGeneratorSession(unittest.TestCase):
    """Test cases for session-based word generation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = WordGenerator(seed=42)
    
    def test_generate_for_session_basic_calculation(self):
        """Test basic session word count calculation"""
        # 3 minutes at 40 WPM = 120 words + 10% buffer = 132 words
        mock_words = ["word"] * 200  # Enough words to avoid repetition
        
        with patch.object(self.generator, '_get_words_for_difficulty', return_value=mock_words):
            result = self.generator.generate_for_session(Difficulty.MEDIUM, 180, 40)
        
        # 3 minutes * 40 WPM * 1.1 buffer = 132 words
        expected_count = int(3 * 40 * 1.1)
        self.assertEqual(len(result), expected_count)
    
    def test_generate_for_session_different_durations(self):
        """Test session generation with different durations"""
        mock_words = ["word"] * 500
        
        test_cases = [
            (60, 30, int(1 * 30 * 1.1)),    # 1 minute at 30 WPM
            (120, 50, int(2 * 50 * 1.1)),   # 2 minutes at 50 WPM
            (300, 60, int(5 * 60 * 1.1)),   # 5 minutes at 60 WPM
        ]
        
        for duration, wpm, expected_count in test_cases:
            with patch.object(self.generator, '_get_words_for_difficulty', return_value=mock_words):
                result = self.generator.generate_for_session(Difficulty.MEDIUM, duration, wpm)
                self.assertEqual(len(result), expected_count, 
                               f"Failed for {duration}s at {wpm} WPM")
    
    def test_generate_for_session_custom_buffer_percentage(self):
        """Test session generation with custom buffer percentage"""
        mock_words = ["word"] * 200
        
        # Change buffer percentage to 20%
        original_buffer = self.generator.config['session_buffer_percentage']
        self.generator.config['session_buffer_percentage'] = 20
        
        try:
            with patch.object(self.generator, '_get_words_for_difficulty', return_value=mock_words):
                result = self.generator.generate_for_session(Difficulty.MEDIUM, 60, 40)
            
            # 1 minute * 40 WPM * 1.2 buffer = 48 words
            expected_count = int(1 * 40 * 1.2)
            self.assertEqual(len(result), expected_count)
        finally:
            self.generator.config['session_buffer_percentage'] = original_buffer
    
    def test_generate_for_session_minimum_word_count(self):
        """Test that session generation respects minimum word count"""
        mock_words = ["word"] * 50
        
        # Very short session that would calculate to < 10 words
        with patch.object(self.generator, '_get_words_for_difficulty', return_value=mock_words):
            result = self.generator.generate_for_session(Difficulty.MEDIUM, 5, 10)
        
        # Should be at least 10 words
        self.assertGreaterEqual(len(result), 10)
    
    def test_generate_for_session_fractional_minutes(self):
        """Test session calculation with fractional minutes"""
        mock_words = ["word"] * 100
        
        # 90 seconds (1.5 minutes) at 40 WPM
        with patch.object(self.generator, '_get_words_for_difficulty', return_value=mock_words):
            result = self.generator.generate_for_session(Difficulty.MEDIUM, 90, 40)
        
        # 1.5 minutes * 40 WPM * 1.1 buffer = 66 words
        expected_count = int(1.5 * 40 * 1.1)
        self.assertEqual(len(result), expected_count)
    
    def test_generate_for_session_zero_duration(self):
        """Test that zero duration raises ValueError"""
        with self.assertRaises(ValueError) as context:
            self.generator.generate_for_session(Difficulty.MEDIUM, 0, 40)
        
        self.assertIn("Duration must be positive", str(context.exception))
    
    def test_generate_for_session_negative_duration(self):
        """Test that negative duration raises ValueError"""
        with self.assertRaises(ValueError) as context:
            self.generator.generate_for_session(Difficulty.MEDIUM, -60, 40)
        
        self.assertIn("Duration must be positive", str(context.exception))
    
    def test_generate_for_session_zero_wpm(self):
        """Test that zero WPM raises ValueError"""
        with self.assertRaises(ValueError) as context:
            self.generator.generate_for_session(Difficulty.MEDIUM, 180, 0)
        
        self.assertIn("Target WPM must be positive", str(context.exception))
    
    def test_generate_for_session_negative_wpm(self):
        """Test that negative WPM raises ValueError"""
        with self.assertRaises(ValueError) as context:
            self.generator.generate_for_session(Difficulty.MEDIUM, 180, -40)
        
        self.assertIn("Target WPM must be positive", str(context.exception))
    
    def test_generate_for_session_high_wpm(self):
        """Test session generation with high WPM"""
        mock_words = ["word"] * 1000
        
        # 2 minutes at 100 WPM
        with patch.object(self.generator, '_get_words_for_difficulty', return_value=mock_words):
            result = self.generator.generate_for_session(Difficulty.HARD, 120, 100)
        
        # 2 minutes * 100 WPM * 1.1 buffer = 220 words
        expected_count = int(2 * 100 * 1.1)
        self.assertEqual(len(result), expected_count)
    
    def test_generate_for_session_all_difficulties(self):
        """Test session generation for all difficulty levels"""
        mock_words = ["word"] * 100
        
        for difficulty in Difficulty:
            with patch.object(self.generator, '_get_words_for_difficulty', return_value=mock_words):
                result = self.generator.generate_for_session(difficulty, 60, 30)
                
                # 1 minute * 30 WPM * 1.1 buffer = 33 words
                expected_count = int(1 * 30 * 1.1)
                self.assertEqual(len(result), expected_count, 
                               f"Failed for difficulty {difficulty}")
    
    def test_generate_for_session_uses_generate_words(self):
        """Test that session generation uses the generate_words method"""
        with patch.object(self.generator, 'generate_words', return_value=["test", "words"]) as mock_generate:
            result = self.generator.generate_for_session(Difficulty.MEDIUM, 60, 40)
            
            # Should call generate_words with calculated count
            expected_count = int(1 * 40 * 1.1)  # 44 words
            mock_generate.assert_called_once_with(Difficulty.MEDIUM, expected_count)
            self.assertEqual(result, ["test", "words"])
    
    def test_generate_for_session_reproducible_with_seed(self):
        """Test that session generation is reproducible with same seed"""
        mock_words = ["word1", "word2", "word3", "word4", "word5"] * 20
        
        generator1 = WordGenerator(seed=789)
        generator2 = WordGenerator(seed=789)
        
        with patch.object(generator1, '_get_words_for_difficulty', return_value=mock_words):
            with patch.object(generator2, '_get_words_for_difficulty', return_value=mock_words):
                result1 = generator1.generate_for_session(Difficulty.MEDIUM, 60, 30)
                result2 = generator2.generate_for_session(Difficulty.MEDIUM, 60, 30)
        
        self.assertEqual(result1, result2)


if __name__ == '__main__':
    unittest.main()