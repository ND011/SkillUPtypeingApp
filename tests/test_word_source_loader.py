"""
Unit tests for word source loader
"""

import unittest
import tempfile
import os
from unittest.mock import patch, mock_open
from game.word_source_loader import WordSourceLoader
from models.difficulty import Difficulty


class TestWordSourceLoader(unittest.TestCase):
    """Test cases for WordSourceLoader"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.loader = WordSourceLoader()
    
    def test_load_file_simple_words(self):
        """Test loading a simple word file"""
        test_content = "hello\nworld\ntest\n"
        
        with patch("builtins.open", mock_open(read_data=test_content)):
            with patch("os.path.exists", return_value=True):
                words = self.loader.load_file("test.txt")
        
        self.assertEqual(words, ["hello", "world", "test"])
    
    def test_load_file_with_phrases_allowed(self):
        """Test loading file with phrases when allow_phrases=True"""
        test_content = "hello world\nsingle\nphrase test\n"
        
        with patch("builtins.open", mock_open(read_data=test_content)):
            with patch("os.path.exists", return_value=True):
                words = self.loader.load_file("test.txt", allow_phrases=True)
        
        self.assertEqual(words, ["hello world", "single", "phrase test"])
    
    def test_load_file_with_phrases_not_allowed(self):
        """Test loading file with phrases when allow_phrases=False"""
        test_content = "hello world\nsingle\nphrase test\n"
        
        with patch("builtins.open", mock_open(read_data=test_content)):
            with patch("os.path.exists", return_value=True):
                words = self.loader.load_file("test.txt", allow_phrases=False)
        
        self.assertEqual(words, ["hello", "world", "single", "phrase", "test"])
    
    def test_load_file_skip_empty_lines(self):
        """Test that empty lines and comments are skipped"""
        test_content = "hello\n\n# This is a comment\nworld\n   \ntest\n"
        
        with patch("builtins.open", mock_open(read_data=test_content)):
            with patch("os.path.exists", return_value=True):
                words = self.loader.load_file("test.txt")
        
        self.assertEqual(words, ["hello", "world", "test"])
    
    def test_load_file_not_found(self):
        """Test FileNotFoundError when file doesn't exist"""
        with patch("os.path.exists", return_value=False):
            with self.assertRaises(FileNotFoundError) as context:
                self.loader.load_file("nonexistent.txt")
            self.assertIn("Word file not found", str(context.exception))
    
    def test_load_file_permission_error(self):
        """Test PermissionError when file can't be read"""
        with patch("os.path.exists", return_value=True):
            with patch("builtins.open", side_effect=PermissionError("Access denied")):
                with self.assertRaises(PermissionError) as context:
                    self.loader.load_file("test.txt")
                self.assertIn("Permission denied reading file", str(context.exception))
    
    def test_load_file_encoding_fallback(self):
        """Test that encoding fallback works"""
        test_content = "café\nnaïve\nresumé\n"
        
        def mock_open_with_encoding_error(*args, **kwargs):
            encoding = kwargs.get('encoding', 'utf-8')
            if encoding == 'utf-8':
                raise UnicodeDecodeError('utf-8', b'', 0, 1, 'invalid start byte')
            return mock_open(read_data=test_content)(*args, **kwargs)
        
        with patch("builtins.open", side_effect=mock_open_with_encoding_error):
            with patch("os.path.exists", return_value=True):
                words = self.loader.load_file("test.txt")
        
        self.assertEqual(words, ["café", "naïve", "resumé"])
    
    def test_get_words_for_difficulty_cached(self):
        """Test getting words from cache"""
        # Pre-populate cache
        test_words = ["cached", "words", "test"]
        self.loader._word_cache[Difficulty.MEDIUM] = test_words
        
        words = self.loader.get_words_for_difficulty(Difficulty.MEDIUM)
        
        self.assertEqual(words, test_words)
        # Verify it returns a copy, not the original
        words.append("modified")
        self.assertNotEqual(words, self.loader._word_cache[Difficulty.MEDIUM])
    
    def test_get_words_for_difficulty_load_from_file(self):
        """Test loading words from file when not cached"""
        test_content = "medium\nwords\ntest\n"
        
        with patch("builtins.open", mock_open(read_data=test_content)):
            with patch("os.path.exists", return_value=True):
                words = self.loader.get_words_for_difficulty(Difficulty.MEDIUM)
        
        self.assertEqual(words, ["medium", "words", "test"])
        # Verify it's cached
        self.assertIn(Difficulty.MEDIUM, self.loader._word_cache)
    
    def test_get_words_for_difficulty_fallback(self):
        """Test fallback words when file not found"""
        with patch("os.path.exists", return_value=False):
            words = self.loader.get_words_for_difficulty(Difficulty.SIMPLE)
        
        self.assertIsInstance(words, list)
        self.assertGreater(len(words), 0)
        # Should contain basic words
        self.assertIn("the", words)
        self.assertIn("and", words)
    
    def test_get_words_for_difficulty_invalid_difficulty(self):
        """Test error for invalid difficulty"""
        # Remove a difficulty from file mappings to test error
        original_mappings = self.loader._file_mappings.copy()
        del self.loader._file_mappings[Difficulty.MEDIUM]
        
        try:
            with self.assertRaises(ValueError) as context:
                self.loader.get_words_for_difficulty(Difficulty.MEDIUM)
            self.assertIn("No file mapping found", str(context.exception))
        finally:
            self.loader._file_mappings = original_mappings
    
    def test_fallback_words_different_difficulties(self):
        """Test that different difficulties have different fallback words"""
        simple_words = self.loader._get_fallback_words(Difficulty.SIMPLE)
        medium_words = self.loader._get_fallback_words(Difficulty.MEDIUM)
        hard_words = self.loader._get_fallback_words(Difficulty.HARD)
        extra_hard_words = self.loader._get_fallback_words(Difficulty.EXTRA_HARD)
        
        # Each difficulty should have more words than the previous
        self.assertLess(len(simple_words), len(medium_words))
        self.assertLess(len(medium_words), len(hard_words))
        self.assertLess(len(hard_words), len(extra_hard_words))
        
        # All should contain the base words
        for words in [simple_words, medium_words, hard_words, extra_hard_words]:
            self.assertIn("the", words)
            self.assertIn("and", words)
    
    def test_reload_sources(self):
        """Test that reload_sources clears the cache"""
        # Populate cache
        self.loader._word_cache[Difficulty.MEDIUM] = ["test", "words"]
        self.assertIn(Difficulty.MEDIUM, self.loader._word_cache)
        
        # Reload sources
        self.loader.reload_sources()
        
        # Cache should be empty
        self.assertEqual(len(self.loader._word_cache), 0)
    
    def test_get_available_difficulties(self):
        """Test getting list of available difficulties"""
        # Mock successful loading for some difficulties
        def mock_get_words(difficulty):
            if difficulty in [Difficulty.SIMPLE, Difficulty.MEDIUM]:
                return ["test", "words"]
            else:
                raise FileNotFoundError("Not found")
        
        with patch.object(self.loader, 'get_words_for_difficulty', side_effect=mock_get_words):
            available = self.loader.get_available_difficulties()
        
        self.assertIn(Difficulty.SIMPLE, available)
        self.assertIn(Difficulty.MEDIUM, available)
        self.assertNotIn(Difficulty.HARD, available)
        self.assertNotIn(Difficulty.EXTRA_HARD, available)
    
    def test_get_word_count_for_difficulty(self):
        """Test getting word count for a difficulty"""
        test_words = ["word1", "word2", "word3"]
        
        with patch.object(self.loader, 'get_words_for_difficulty', return_value=test_words):
            count = self.loader.get_word_count_for_difficulty(Difficulty.MEDIUM)
        
        self.assertEqual(count, 3)
    
    def test_get_word_count_for_difficulty_error(self):
        """Test getting word count when error occurs"""
        with patch.object(self.loader, 'get_words_for_difficulty', side_effect=Exception("Error")):
            count = self.loader.get_word_count_for_difficulty(Difficulty.MEDIUM)
        
        self.assertEqual(count, 0)


if __name__ == '__main__':
    unittest.main()