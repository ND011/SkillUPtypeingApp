"""
Unit tests for fixed count word generation
"""

import unittest
from unittest.mock import Mock, patch
from speed_word_generator import WordGenerator
from models.difficulty import Difficulty


class TestWordGeneratorFixedCount(unittest.TestCase):
    """Test cases for fixed count word generation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = WordGenerator(seed=42)
    
    def test_generate_words_valid_count(self):
        """Test generating words with valid count"""
        mock_words = ["word1", "word2", "word3", "word4", "word5"]
        
        with patch.object(self.generator, '_get_words_for_difficulty', return_value=mock_words):
            result = self.generator.generate_words(Difficulty.MEDIUM, 3)
        
        self.assertEqual(len(result), 3)
        self.assertTrue(all(word in mock_words for word in result))
        # With seed=42, should be deterministic
        self.assertIsInstance(result, list)
    
    def test_generate_words_exact_available_count(self):
        """Test generating words when count equals available words"""
        mock_words = ["word1", "word2", "word3"]
        
        with patch.object(self.generator, '_get_words_for_difficulty', return_value=mock_words):
            result = self.generator.generate_words(Difficulty.MEDIUM, 3)
        
        self.assertEqual(len(result), 3)
        self.assertEqual(set(result), set(mock_words))
    
    def test_generate_words_more_than_available(self):
        """Test generating more words than available (with repetition)"""
        mock_words = ["word1", "word2", "word3"]
        
        with patch.object(self.generator, '_get_words_for_difficulty', return_value=mock_words):
            result = self.generator.generate_words(Difficulty.MEDIUM, 7)
        
        self.assertEqual(len(result), 7)
        # Should contain repeated words
        word_counts = {}
        for word in result:
            word_counts[word] = word_counts.get(word, 0) + 1
        
        # At least one word should appear more than once
        self.assertTrue(any(count > 1 for count in word_counts.values()))
    
    def test_generate_words_large_count_with_repetition(self):
        """Test generating a large number of words with repetition"""
        mock_words = ["word1", "word2"]
        
        with patch.object(self.generator, '_get_words_for_difficulty', return_value=mock_words):
            result = self.generator.generate_words(Difficulty.MEDIUM, 10)
        
        self.assertEqual(len(result), 10)
        # All words should be from the original set
        self.assertTrue(all(word in mock_words for word in result))
        
        # Should have roughly equal distribution (with some randomness)
        word1_count = result.count("word1")
        word2_count = result.count("word2")
        self.assertEqual(word1_count + word2_count, 10)
    
    def test_generate_words_zero_count(self):
        """Test that zero count raises ValueError"""
        with self.assertRaises(ValueError) as context:
            self.generator.generate_words(Difficulty.MEDIUM, 0)
        
        self.assertIn("Count must be positive", str(context.exception))
    
    def test_generate_words_negative_count(self):
        """Test that negative count raises ValueError"""
        with self.assertRaises(ValueError) as context:
            self.generator.generate_words(Difficulty.MEDIUM, -5)
        
        self.assertIn("Count must be positive", str(context.exception))
    
    def test_generate_words_no_available_words(self):
        """Test error when no words are available for difficulty"""
        with patch.object(self.generator, '_get_words_for_difficulty', return_value=[]):
            with self.assertRaises(RuntimeError) as context:
                self.generator.generate_words(Difficulty.MEDIUM, 5)
        
        self.assertIn("No words available for difficulty", str(context.exception))
    
    def test_generate_words_single_word_available(self):
        """Test generating multiple words when only one is available"""
        mock_words = ["onlyword"]
        
        with patch.object(self.generator, '_get_words_for_difficulty', return_value=mock_words):
            result = self.generator.generate_words(Difficulty.MEDIUM, 5)
        
        self.assertEqual(len(result), 5)
        self.assertTrue(all(word == "onlyword" for word in result))
    
    def test_generate_words_reproducible_with_seed(self):
        """Test that generation is reproducible with the same seed"""
        mock_words = ["word1", "word2", "word3", "word4", "word5"]
        
        # Generate words twice with same seed
        generator1 = WordGenerator(seed=123)
        generator2 = WordGenerator(seed=123)
        
        with patch.object(generator1, '_get_words_for_difficulty', return_value=mock_words):
            with patch.object(generator2, '_get_words_for_difficulty', return_value=mock_words):
                result1 = generator1.generate_words(Difficulty.MEDIUM, 3)
                result2 = generator2.generate_words(Difficulty.MEDIUM, 3)
        
        self.assertEqual(result1, result2)
    
    def test_generate_words_different_with_different_seed(self):
        """Test that generation differs with different seeds"""
        mock_words = ["word1", "word2", "word3", "word4", "word5", "word6", "word7", "word8"]
        
        generator1 = WordGenerator(seed=123)
        generator2 = WordGenerator(seed=456)
        
        with patch.object(generator1, '_get_words_for_difficulty', return_value=mock_words):
            with patch.object(generator2, '_get_words_for_difficulty', return_value=mock_words):
                result1 = generator1.generate_words(Difficulty.MEDIUM, 5)
                result2 = generator2.generate_words(Difficulty.MEDIUM, 5)
        
        # Results should be different (very high probability with different seeds)
        self.assertNotEqual(result1, result2)
    
    def test_generate_words_all_difficulties(self):
        """Test generating words for all difficulty levels"""
        mock_words = ["test1", "test2", "test3"]
        
        with patch.object(self.generator, '_get_words_for_difficulty', return_value=mock_words):
            for difficulty in Difficulty:
                result = self.generator.generate_words(difficulty, 2)
                self.assertEqual(len(result), 2)
                self.assertTrue(all(word in mock_words for word in result))


if __name__ == '__main__':
    unittest.main()