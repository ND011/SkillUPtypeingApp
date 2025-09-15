"""
Unit tests for paragraph formatting word generation
"""

import unittest
from unittest.mock import Mock, patch
from speed_word_generator import WordGenerator
from models.difficulty import Difficulty


class TestWordGeneratorParagraph(unittest.TestCase):
    """Test cases for paragraph formatting word generation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = WordGenerator(seed=42)
    
    def test_generate_paragraph_basic(self):
        """Test basic paragraph generation"""
        mock_words = ["short", "word", "test", "line", "break", "here", "more", "words"]
        
        with patch.object(self.generator, 'generate_words', return_value=mock_words):
            result = self.generator.generate_paragraph(Difficulty.MEDIUM, 3, 20)
        
        self.assertEqual(len(result), 3)  # Should have 3 lines
        for line in result:
            self.assertIsInstance(line, str)
            self.assertLessEqual(len(line), 20)  # Each line should respect char limit
            self.assertGreater(len(line), 0)  # Each line should have content
    
    def test_generate_paragraph_character_limits(self):
        """Test that paragraph respects character limits"""
        mock_words = ["word", "test", "example", "line", "break", "character", "limit"]
        
        with patch.object(self.generator, 'generate_words', return_value=mock_words):
            result = self.generator.generate_paragraph(Difficulty.MEDIUM, 2, 15)
        
        for line in result:
            self.assertLessEqual(len(line), 15, f"Line '{line}' exceeds 15 characters")
    
    def test_generate_paragraph_single_line(self):
        """Test generating a single line paragraph"""
        mock_words = ["one", "line", "only", "test"]
        
        with patch.object(self.generator, 'generate_words', return_value=mock_words):
            result = self.generator.generate_paragraph(Difficulty.MEDIUM, 1, 50)
        
        self.assertEqual(len(result), 1)
        self.assertIn("one", result[0])
    
    def test_generate_paragraph_long_words(self):
        """Test paragraph generation with words longer than line limit"""
        mock_words = ["supercalifragilisticexpialidocious", "short", "word"]
        
        with patch.object(self.generator, 'generate_words', return_value=mock_words):
            result = self.generator.generate_paragraph(Difficulty.HARD, 2, 10)
        
        self.assertEqual(len(result), 2)
        # First line should contain the long word (forced)
        self.assertIn("supercalifragilisticexpialidocious", result[0])
    
    def test_generate_paragraph_exact_character_fit(self):
        """Test paragraph generation where words fit exactly"""
        # "word test" = 9 characters, fits exactly in 10 char limit
        mock_words = ["word", "test", "more", "words"]
        
        with patch.object(self.generator, 'generate_words', return_value=mock_words):
            result = self.generator.generate_paragraph(Difficulty.MEDIUM, 1, 9)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "word test")
    
    def test_generate_paragraph_insufficient_words(self):
        """Test paragraph generation when initial words are insufficient"""
        # Mock generate_words to be called multiple times
        call_count = 0
        def mock_generate_words(difficulty, count):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return ["first", "batch"]
            else:
                return ["second", "batch", "more", "words"]
        
        with patch.object(self.generator, 'generate_words', side_effect=mock_generate_words):
            result = self.generator.generate_paragraph(Difficulty.MEDIUM, 3, 20)
        
        self.assertEqual(len(result), 3)
        # Should have called generate_words multiple times
        self.assertGreater(call_count, 1)
    
    def test_generate_paragraph_zero_lines(self):
        """Test that zero lines raises ValueError"""
        with self.assertRaises(ValueError) as context:
            self.generator.generate_paragraph(Difficulty.MEDIUM, 0, 20)
        
        self.assertIn("Lines must be positive", str(context.exception))
    
    def test_generate_paragraph_negative_lines(self):
        """Test that negative lines raises ValueError"""
        with self.assertRaises(ValueError) as context:
            self.generator.generate_paragraph(Difficulty.MEDIUM, -2, 20)
        
        self.assertIn("Lines must be positive", str(context.exception))
    
    def test_generate_paragraph_zero_max_chars(self):
        """Test that zero max chars raises ValueError"""
        with self.assertRaises(ValueError) as context:
            self.generator.generate_paragraph(Difficulty.MEDIUM, 3, 0)
        
        self.assertIn("Max line chars must be positive", str(context.exception))
    
    def test_generate_paragraph_negative_max_chars(self):
        """Test that negative max chars raises ValueError"""
        with self.assertRaises(ValueError) as context:
            self.generator.generate_paragraph(Difficulty.MEDIUM, 3, -10)
        
        self.assertIn("Max line chars must be positive", str(context.exception))
    
    def test_generate_paragraph_very_short_lines(self):
        """Test paragraph generation with very short line limits"""
        mock_words = ["a", "b", "c", "d", "e", "f"]
        
        with patch.object(self.generator, 'generate_words', return_value=mock_words):
            result = self.generator.generate_paragraph(Difficulty.MEDIUM, 3, 3)
        
        self.assertEqual(len(result), 3)
        for line in result:
            self.assertLessEqual(len(line), 3)
    
    def test_generate_paragraph_very_long_lines(self):
        """Test paragraph generation with very long line limits"""
        mock_words = ["word"] * 20
        
        with patch.object(self.generator, 'generate_words', return_value=mock_words):
            result = self.generator.generate_paragraph(Difficulty.MEDIUM, 2, 200)
        
        self.assertEqual(len(result), 2)
        # Lines should contain multiple words
        for line in result:
            self.assertGreater(line.count(" "), 3)  # At least 4 words per line
    
    def test_generate_paragraph_all_difficulties(self):
        """Test paragraph generation for all difficulty levels"""
        mock_words = ["test", "words", "for", "all", "difficulty", "levels"]
        
        for difficulty in Difficulty:
            with patch.object(self.generator, 'generate_words', return_value=mock_words):
                result = self.generator.generate_paragraph(difficulty, 2, 25)
                
                self.assertEqual(len(result), 2, f"Failed for difficulty {difficulty}")
                for line in result:
                    self.assertLessEqual(len(line), 25)
    
    def test_generate_paragraph_word_distribution(self):
        """Test that words are distributed across lines"""
        mock_words = ["one", "two", "three", "four", "five", "six", "seven", "eight"]
        
        with patch.object(self.generator, 'generate_words', return_value=mock_words):
            result = self.generator.generate_paragraph(Difficulty.MEDIUM, 4, 15)
        
        self.assertEqual(len(result), 4)
        
        # Each line should have at least one word
        for line in result:
            self.assertGreater(len(line.strip()), 0)
        
        # All lines combined should contain words from the mock list
        all_text = " ".join(result)
        for word in mock_words[:6]:  # At least first 6 words should be used
            self.assertIn(word, all_text)
    
    def test_generate_paragraph_reproducible_with_seed(self):
        """Test that paragraph generation is reproducible with same seed"""
        mock_words = ["word1", "word2", "word3", "word4", "word5"] * 5
        
        generator1 = WordGenerator(seed=999)
        generator2 = WordGenerator(seed=999)
        
        with patch.object(generator1, 'generate_words', return_value=mock_words):
            with patch.object(generator2, 'generate_words', return_value=mock_words):
                result1 = generator1.generate_paragraph(Difficulty.MEDIUM, 3, 20)
                result2 = generator2.generate_paragraph(Difficulty.MEDIUM, 3, 20)
        
        self.assertEqual(result1, result2)


if __name__ == '__main__':
    unittest.main()