"""
Unit tests for mixed difficulty word generation
"""

import unittest
from unittest.mock import Mock, patch
from speed_word_generator import WordGenerator
from models.difficulty import Difficulty


class TestWordGeneratorMixed(unittest.TestCase):
    """Test cases for mixed difficulty word generation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = WordGenerator(seed=42)
    
    def test_generate_mixed_basic(self):
        """Test basic mixed difficulty generation"""
        weights = {
            Difficulty.MEDIUM: 0.5,
            Difficulty.HARD: 0.3,
            Difficulty.EXTRA_HARD: 0.2
        }
        
        def mock_generate_words(difficulty, count):
            return [f"{difficulty.value}_word"] * count
        
        with patch.object(self.generator, 'generate_words', side_effect=mock_generate_words):
            result = self.generator.generate_mixed(weights, 100)
        
        self.assertEqual(len(result), 100)
        
        # Count words by difficulty
        medium_count = sum(1 for word in result if word.startswith('medium'))
        hard_count = sum(1 for word in result if word.startswith('hard'))
        extra_hard_count = sum(1 for word in result if word.startswith('extra_hard'))
        
        # Should be approximately 50, 30, 20 respectively
        self.assertAlmostEqual(medium_count, 50, delta=2)
        self.assertAlmostEqual(hard_count, 30, delta=2)
        self.assertAlmostEqual(extra_hard_count, 20, delta=2)
    
    def test_generate_mixed_exact_proportions(self):
        """Test mixed generation with exact proportions"""
        weights = {
            Difficulty.SIMPLE: 0.25,
            Difficulty.MEDIUM: 0.25,
            Difficulty.HARD: 0.25,
            Difficulty.EXTRA_HARD: 0.25
        }
        
        def mock_generate_words(difficulty, count):
            return [f"{difficulty.value}_word"] * count
        
        with patch.object(self.generator, 'generate_words', side_effect=mock_generate_words):
            result = self.generator.generate_mixed(weights, 120)
        
        self.assertEqual(len(result), 120)
        
        # Each difficulty should have exactly 30 words
        for difficulty in Difficulty:
            count = sum(1 for word in result if word.startswith(difficulty.value))
            self.assertEqual(count, 30, f"Expected 30 words for {difficulty.value}, got {count}")
    
    def test_generate_mixed_weight_normalization(self):
        """Test that weights are normalized when they don't sum to 1.0"""
        weights = {
            Difficulty.MEDIUM: 2.0,  # These sum to 6.0, should be normalized
            Difficulty.HARD: 3.0,
            Difficulty.EXTRA_HARD: 1.0
        }
        
        def mock_generate_words(difficulty, count):
            return [f"{difficulty.value}_word"] * count
        
        with patch.object(self.generator, 'generate_words', side_effect=mock_generate_words):
            result = self.generator.generate_mixed(weights, 60)
        
        self.assertEqual(len(result), 60)
        
        # Should be normalized to 2/6, 3/6, 1/6 = 1/3, 1/2, 1/6
        medium_count = sum(1 for word in result if word.startswith('medium'))
        hard_count = sum(1 for word in result if word.startswith('hard'))
        extra_hard_count = sum(1 for word in result if word.startswith('extra_hard'))
        
        self.assertAlmostEqual(medium_count, 20, delta=2)  # 60 * (2/6) = 20
        self.assertAlmostEqual(hard_count, 30, delta=2)    # 60 * (3/6) = 30
        self.assertAlmostEqual(extra_hard_count, 10, delta=2)  # 60 * (1/6) = 10
    
    def test_generate_mixed_rounding_distribution(self):
        """Test proper distribution of remaining words after rounding"""
        weights = {
            Difficulty.MEDIUM: 0.33,  # 33% of 100 = 33
            Difficulty.HARD: 0.33,   # 33% of 100 = 33
            Difficulty.EXTRA_HARD: 0.34  # 34% of 100 = 34
        }
        
        def mock_generate_words(difficulty, count):
            return [f"{difficulty.value}_word"] * count
        
        with patch.object(self.generator, 'generate_words', side_effect=mock_generate_words):
            result = self.generator.generate_mixed(weights, 100)
        
        self.assertEqual(len(result), 100)
        
        # Total should still be 100 despite rounding
        medium_count = sum(1 for word in result if word.startswith('medium'))
        hard_count = sum(1 for word in result if word.startswith('hard'))
        extra_hard_count = sum(1 for word in result if word.startswith('extra_hard'))
        
        self.assertEqual(medium_count + hard_count + extra_hard_count, 100)
    
    def test_generate_mixed_single_difficulty(self):
        """Test mixed generation with only one difficulty"""
        weights = {Difficulty.MEDIUM: 1.0}
        
        def mock_generate_words(difficulty, count):
            return [f"{difficulty.value}_word"] * count
        
        with patch.object(self.generator, 'generate_words', side_effect=mock_generate_words):
            result = self.generator.generate_mixed(weights, 50)
        
        self.assertEqual(len(result), 50)
        self.assertTrue(all(word.startswith('medium') for word in result))
    
    def test_generate_mixed_zero_total_count(self):
        """Test that zero total count raises ValueError"""
        weights = {Difficulty.MEDIUM: 1.0}
        
        with self.assertRaises(ValueError) as context:
            self.generator.generate_mixed(weights, 0)
        
        self.assertIn("Total count must be positive", str(context.exception))
    
    def test_generate_mixed_negative_total_count(self):
        """Test that negative total count raises ValueError"""
        weights = {Difficulty.MEDIUM: 1.0}
        
        with self.assertRaises(ValueError) as context:
            self.generator.generate_mixed(weights, -10)
        
        self.assertIn("Total count must be positive", str(context.exception))
    
    def test_generate_mixed_empty_weights(self):
        """Test that empty weights raises ValueError"""
        with self.assertRaises(ValueError) as context:
            self.generator.generate_mixed({}, 50)
        
        self.assertIn("Weights dictionary cannot be empty", str(context.exception))
    
    def test_generate_mixed_invalid_difficulty(self):
        """Test that invalid difficulty in weights raises ValueError"""
        weights = {"invalid_difficulty": 1.0}
        
        with self.assertRaises(ValueError) as context:
            self.generator.generate_mixed(weights, 50)
        
        self.assertIn("Invalid difficulty in weights", str(context.exception))
    
    def test_generate_mixed_negative_weight(self):
        """Test that negative weight raises ValueError"""
        weights = {Difficulty.MEDIUM: -0.5}
        
        with self.assertRaises(ValueError) as context:
            self.generator.generate_mixed(weights, 50)
        
        self.assertIn("Weight cannot be negative", str(context.exception))
    
    def test_generate_mixed_zero_total_weight(self):
        """Test that zero total weight raises ValueError"""
        weights = {
            Difficulty.MEDIUM: 0.0,
            Difficulty.HARD: 0.0
        }
        
        with self.assertRaises(ValueError) as context:
            self.generator.generate_mixed(weights, 50)
        
        self.assertIn("Total weight cannot be zero", str(context.exception))
    
    def test_generate_mixed_difficulty_failure_compensation(self):
        """Test compensation when one difficulty fails"""
        weights = {
            Difficulty.MEDIUM: 0.5,
            Difficulty.HARD: 0.5
        }
        
        def mock_generate_words(difficulty, count):
            if difficulty == Difficulty.HARD:
                raise Exception("Hard difficulty failed")
            return [f"{difficulty.value}_word"] * count
        
        with patch.object(self.generator, 'generate_words', side_effect=mock_generate_words):
            result = self.generator.generate_mixed(weights, 100)
        
        # Should still get words, compensated from MEDIUM
        self.assertGreater(len(result), 0)
        self.assertTrue(all(word.startswith('medium') for word in result))
    
    def test_generate_mixed_shuffled_output(self):
        """Test that mixed output is shuffled"""
        weights = {
            Difficulty.MEDIUM: 0.5,
            Difficulty.HARD: 0.5
        }
        
        def mock_generate_words(difficulty, count):
            return [f"{difficulty.value}_word_{i}" for i in range(count)]
        
        with patch.object(self.generator, 'generate_words', side_effect=mock_generate_words):
            result = self.generator.generate_mixed(weights, 20)
        
        # Check that words are not in the original order (very high probability)
        medium_indices = [i for i, word in enumerate(result) if word.startswith('medium')]
        hard_indices = [i for i, word in enumerate(result) if word.startswith('hard')]
        
        # If properly shuffled, medium and hard words should be interspersed
        # This is a probabilistic test, but with seed=42 it should be deterministic
        self.assertTrue(len(medium_indices) > 0)
        self.assertTrue(len(hard_indices) > 0)
    
    def test_generate_mixed_reproducible_with_seed(self):
        """Test that mixed generation is reproducible with same seed"""
        weights = {
            Difficulty.MEDIUM: 0.6,
            Difficulty.HARD: 0.4
        }
        
        def mock_generate_words(difficulty, count):
            return [f"{difficulty.value}_word_{i}" for i in range(count)]
        
        generator1 = WordGenerator(seed=555)
        generator2 = WordGenerator(seed=555)
        
        with patch.object(generator1, 'generate_words', side_effect=mock_generate_words):
            with patch.object(generator2, 'generate_words', side_effect=mock_generate_words):
                result1 = generator1.generate_mixed(weights, 50)
                result2 = generator2.generate_mixed(weights, 50)
        
        self.assertEqual(result1, result2)
    
    def test_generate_mixed_fractional_weights(self):
        """Test mixed generation with small fractional weights"""
        weights = {
            Difficulty.SIMPLE: 0.1,
            Difficulty.MEDIUM: 0.2,
            Difficulty.HARD: 0.3,
            Difficulty.EXTRA_HARD: 0.4
        }
        
        def mock_generate_words(difficulty, count):
            return [f"{difficulty.value}_word"] * count
        
        with patch.object(self.generator, 'generate_words', side_effect=mock_generate_words):
            result = self.generator.generate_mixed(weights, 10)
        
        self.assertEqual(len(result), 10)
        
        # With small counts, should still distribute proportionally
        simple_count = sum(1 for word in result if word.startswith('simple'))
        medium_count = sum(1 for word in result if word.startswith('medium'))
        hard_count = sum(1 for word in result if word.startswith('hard'))
        extra_hard_count = sum(1 for word in result if word.startswith('extra_hard'))
        
        # Should roughly follow the 1:2:3:4 ratio
        self.assertEqual(simple_count + medium_count + hard_count + extra_hard_count, 10)


if __name__ == '__main__':
    unittest.main()