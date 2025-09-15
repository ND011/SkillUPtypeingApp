"""
Unit tests for base WordGenerator infrastructure
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from speed_word_generator import WordGenerator
from models.difficulty import Difficulty, GenerationResult


class TestWordGeneratorBase(unittest.TestCase):
    """Test cases for WordGenerator base functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = WordGenerator(seed=42)
    
    def test_init_with_seed(self):
        """Test WordGenerator initialization with seed"""
        generator = WordGenerator(seed=123)
        self.assertEqual(generator.seed, 123)
        self.assertFalse(generator._sources_loaded)
        self.assertFalse(generator._allow_phrases)
    
    def test_init_without_seed(self):
        """Test WordGenerator initialization without seed"""
        generator = WordGenerator()
        self.assertIsNone(generator.seed)
        self.assertFalse(generator._sources_loaded)
    
    def test_default_config(self):
        """Test that default configuration is set correctly"""
        expected_config = {
            'session_buffer_percentage': 10,
            'default_paragraph_lines': 6,
            'default_line_chars': 200,
            'cache_word_sources': True,
            'export_format': 'tsv'
        }
        self.assertEqual(self.generator.config, expected_config)
    
    @patch('speed_word_generator.WordSourceLoader')
    def test_load_default_sources_success(self, mock_loader_class):
        """Test successful loading of default sources"""
        # Mock the word loader
        mock_loader = Mock()
        mock_loader_class.return_value = mock_loader
        
        # Mock successful word loading for all difficulties
        def mock_get_words(difficulty):
            return [f"word1_{difficulty.value}", f"word2_{difficulty.value}"]
        
        mock_loader.get_words_for_difficulty.side_effect = mock_get_words
        
        generator = WordGenerator()
        generator.load_default_sources(allow_phrases=True)
        
        self.assertTrue(generator._sources_loaded)
        self.assertTrue(generator._allow_phrases)
        
        # Verify all difficulties were attempted
        self.assertEqual(mock_loader.get_words_for_difficulty.call_count, len(Difficulty))
    
    @patch('speed_word_generator.WordSourceLoader')
    def test_load_default_sources_partial_failure(self, mock_loader_class):
        """Test loading sources when some difficulties fail"""
        mock_loader = Mock()
        mock_loader_class.return_value = mock_loader
        
        # Mock partial success - only SIMPLE and MEDIUM work
        def mock_get_words(difficulty):
            if difficulty in [Difficulty.SIMPLE, Difficulty.MEDIUM]:
                return [f"word1_{difficulty.value}", f"word2_{difficulty.value}"]
            else:
                raise FileNotFoundError("File not found")
        
        mock_loader.get_words_for_difficulty.side_effect = mock_get_words
        
        generator = WordGenerator()
        generator.load_default_sources()
        
        self.assertTrue(generator._sources_loaded)
    
    @patch('speed_word_generator.WordSourceLoader')
    def test_load_default_sources_complete_failure(self, mock_loader_class):
        """Test loading sources when all difficulties fail"""
        mock_loader = Mock()
        mock_loader_class.return_value = mock_loader
        
        # Mock complete failure
        mock_loader.get_words_for_difficulty.side_effect = Exception("No files found")
        
        generator = WordGenerator()
        
        with self.assertRaises(RuntimeError) as context:
            generator.load_default_sources()
        
        self.assertIn("No word sources could be loaded", str(context.exception))
        self.assertFalse(generator._sources_loaded)
    
    def test_ensure_sources_loaded_when_not_loaded(self):
        """Test that _ensure_sources_loaded calls load_default_sources"""
        with patch.object(self.generator, 'load_default_sources') as mock_load:
            self.generator._ensure_sources_loaded()
            mock_load.assert_called_once_with(False)
    
    def test_ensure_sources_loaded_when_already_loaded(self):
        """Test that _ensure_sources_loaded doesn't reload when already loaded"""
        self.generator._sources_loaded = True
        
        with patch.object(self.generator, 'load_default_sources') as mock_load:
            self.generator._ensure_sources_loaded()
            mock_load.assert_not_called()
    
    def test_get_words_for_difficulty(self):
        """Test getting words for a specific difficulty"""
        mock_words = ["test", "words", "list"]
        
        with patch.object(self.generator, '_ensure_sources_loaded'):
            with patch.object(self.generator.word_loader, 'get_words_for_difficulty', return_value=mock_words):
                words = self.generator._get_words_for_difficulty(Difficulty.MEDIUM)
        
        self.assertEqual(words, mock_words)
    
    def test_create_generation_result(self):
        """Test creating a GenerationResult"""
        test_words = ["word1", "word2"]
        test_metadata = {"difficulty": "medium", "count": 2}
        
        with patch('time.time', return_value=1234567890.0):
            result = self.generator._create_generation_result(test_words, test_metadata)
        
        self.assertIsInstance(result, GenerationResult)
        self.assertEqual(result.words, test_words)
        self.assertEqual(result.metadata, test_metadata)
        self.assertEqual(result.generation_time, 1234567890.0)
        self.assertEqual(result.seed_used, 42)
    
    def test_get_available_difficulties(self):
        """Test getting available difficulties"""
        mock_difficulties = [Difficulty.SIMPLE, Difficulty.MEDIUM]
        
        with patch.object(self.generator, '_ensure_sources_loaded'):
            with patch.object(self.generator.word_loader, 'get_available_difficulties', return_value=mock_difficulties):
                difficulties = self.generator.get_available_difficulties()
        
        self.assertEqual(difficulties, mock_difficulties)
    
    def test_get_word_count_for_difficulty(self):
        """Test getting word count for a difficulty"""
        mock_count = 150
        
        with patch.object(self.generator, '_ensure_sources_loaded'):
            with patch.object(self.generator.word_loader, 'get_word_count_for_difficulty', return_value=mock_count):
                count = self.generator.get_word_count_for_difficulty(Difficulty.HARD)
        
        self.assertEqual(count, mock_count)
    
    def test_reload_sources(self):
        """Test reloading word sources"""
        self.generator._sources_loaded = True
        
        with patch.object(self.generator.word_loader, 'reload_sources') as mock_reload:
            self.generator.reload_sources()
        
        mock_reload.assert_called_once()
        self.assertFalse(self.generator._sources_loaded)


if __name__ == '__main__':
    unittest.main()