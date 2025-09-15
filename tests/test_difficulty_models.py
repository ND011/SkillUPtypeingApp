"""
Unit tests for difficulty models and data classes
"""

import unittest
from models.difficulty import Difficulty, WordEntry, GenerationRequest, GenerationResult


class TestDifficulty(unittest.TestCase):
    """Test cases for Difficulty enum"""
    
    def test_difficulty_values(self):
        """Test that all difficulty levels have correct values"""
        self.assertEqual(Difficulty.SIMPLE.value, "simple")
        self.assertEqual(Difficulty.MEDIUM.value, "medium")
        self.assertEqual(Difficulty.HARD.value, "hard")
        self.assertEqual(Difficulty.EXTRA_HARD.value, "extra_hard")
    
    def test_difficulty_enum_members(self):
        """Test that all expected difficulty levels exist"""
        expected_difficulties = {"SIMPLE", "MEDIUM", "HARD", "EXTRA_HARD"}
        actual_difficulties = {d.name for d in Difficulty}
        self.assertEqual(expected_difficulties, actual_difficulties)


class TestWordEntry(unittest.TestCase):
    """Test cases for WordEntry dataclass"""
    
    def test_valid_word_entry(self):
        """Test creating a valid word entry"""
        entry = WordEntry(
            text="hello",
            difficulty=Difficulty.MEDIUM,
            source_file="test.txt"
        )
        self.assertEqual(entry.text, "hello")
        self.assertEqual(entry.difficulty, Difficulty.MEDIUM)
        self.assertEqual(entry.source_file, "test.txt")
        self.assertFalse(entry.is_phrase)
    
    def test_word_entry_with_phrase(self):
        """Test creating a word entry marked as phrase"""
        entry = WordEntry(
            text="hello world",
            difficulty=Difficulty.HARD,
            source_file="phrases.txt",
            is_phrase=True
        )
        self.assertTrue(entry.is_phrase)
    
    def test_empty_text_raises_error(self):
        """Test that empty text raises ValueError"""
        with self.assertRaises(ValueError) as context:
            WordEntry(text="", difficulty=Difficulty.MEDIUM, source_file="test.txt")
        self.assertIn("Word text cannot be empty", str(context.exception))
    
    def test_whitespace_only_text_raises_error(self):
        """Test that whitespace-only text raises ValueError"""
        with self.assertRaises(ValueError) as context:
            WordEntry(text="   ", difficulty=Difficulty.MEDIUM, source_file="test.txt")
        self.assertIn("Word text cannot be empty", str(context.exception))
    
    def test_invalid_difficulty_raises_error(self):
        """Test that invalid difficulty raises ValueError"""
        with self.assertRaises(ValueError) as context:
            WordEntry(text="hello", difficulty="invalid", source_file="test.txt")
        self.assertIn("Difficulty must be a Difficulty enum value", str(context.exception))
    
    def test_empty_source_file_raises_error(self):
        """Test that empty source file raises ValueError"""
        with self.assertRaises(ValueError) as context:
            WordEntry(text="hello", difficulty=Difficulty.MEDIUM, source_file="")
        self.assertIn("Source file cannot be empty", str(context.exception))


class TestGenerationRequest(unittest.TestCase):
    """Test cases for GenerationRequest dataclass"""
    
    def test_valid_generation_request(self):
        """Test creating a valid generation request"""
        request = GenerationRequest(
            difficulty=Difficulty.MEDIUM,
            count=50,
            duration_seconds=180,
            target_wpm=40
        )
        self.assertEqual(request.difficulty, Difficulty.MEDIUM)
        self.assertEqual(request.count, 50)
        self.assertEqual(request.duration_seconds, 180)
        self.assertEqual(request.target_wpm, 40)
    
    def test_empty_generation_request(self):
        """Test creating an empty generation request"""
        request = GenerationRequest()
        self.assertIsNone(request.difficulty)
        self.assertIsNone(request.count)
        self.assertIsNone(request.duration_seconds)
    
    def test_negative_count_raises_error(self):
        """Test that negative count raises ValueError"""
        with self.assertRaises(ValueError) as context:
            GenerationRequest(count=-1)
        self.assertIn("Count must be positive", str(context.exception))
    
    def test_zero_count_raises_error(self):
        """Test that zero count raises ValueError"""
        with self.assertRaises(ValueError) as context:
            GenerationRequest(count=0)
        self.assertIn("Count must be positive", str(context.exception))
    
    def test_negative_duration_raises_error(self):
        """Test that negative duration raises ValueError"""
        with self.assertRaises(ValueError) as context:
            GenerationRequest(duration_seconds=-1)
        self.assertIn("Duration must be positive", str(context.exception))
    
    def test_negative_target_wpm_raises_error(self):
        """Test that negative target WPM raises ValueError"""
        with self.assertRaises(ValueError) as context:
            GenerationRequest(target_wpm=-1)
        self.assertIn("Target WPM must be positive", str(context.exception))
    
    def test_negative_lines_raises_error(self):
        """Test that negative lines raises ValueError"""
        with self.assertRaises(ValueError) as context:
            GenerationRequest(lines=-1)
        self.assertIn("Lines must be positive", str(context.exception))
    
    def test_negative_max_line_chars_raises_error(self):
        """Test that negative max line chars raises ValueError"""
        with self.assertRaises(ValueError) as context:
            GenerationRequest(max_line_chars=-1)
        self.assertIn("Max line chars must be positive", str(context.exception))


class TestGenerationResult(unittest.TestCase):
    """Test cases for GenerationResult dataclass"""
    
    def test_valid_generation_result(self):
        """Test creating a valid generation result"""
        result = GenerationResult(
            words=["hello", "world"],
            metadata={"difficulty": "medium", "count": 2},
            generation_time=0.05,
            seed_used=42
        )
        self.assertEqual(result.words, ["hello", "world"])
        self.assertEqual(result.metadata["difficulty"], "medium")
        self.assertEqual(result.generation_time, 0.05)
        self.assertEqual(result.seed_used, 42)
    
    def test_generation_result_without_seed(self):
        """Test creating a generation result without seed"""
        result = GenerationResult(
            words=["test"],
            metadata={},
            generation_time=0.01
        )
        self.assertIsNone(result.seed_used)
    
    def test_invalid_words_type_raises_error(self):
        """Test that non-list words raises ValueError"""
        with self.assertRaises(ValueError) as context:
            GenerationResult(
                words="not a list",
                metadata={},
                generation_time=0.01
            )
        self.assertIn("Words must be a list", str(context.exception))
    
    def test_invalid_metadata_type_raises_error(self):
        """Test that non-dict metadata raises ValueError"""
        with self.assertRaises(ValueError) as context:
            GenerationResult(
                words=[],
                metadata="not a dict",
                generation_time=0.01
            )
        self.assertIn("Metadata must be a dictionary", str(context.exception))
    
    def test_negative_generation_time_raises_error(self):
        """Test that negative generation time raises ValueError"""
        with self.assertRaises(ValueError) as context:
            GenerationResult(
                words=[],
                metadata={},
                generation_time=-0.01
            )
        self.assertIn("Generation time cannot be negative", str(context.exception))


if __name__ == '__main__':
    unittest.main()