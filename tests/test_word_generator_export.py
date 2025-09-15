"""
Unit tests for export functionality
"""

import unittest
import tempfile
import os
from unittest.mock import Mock, patch, mock_open
from speed_word_generator import WordGenerator
from models.difficulty import Difficulty


class TestWordGeneratorExport(unittest.TestCase):
    """Test cases for export functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = WordGenerator(seed=42)
    
    def test_save_merged_basic(self):
        """Test basic TSV export functionality"""
        # Mock word data for different difficulties
        mock_word_data = {
            Difficulty.SIMPLE: ["cat", "dog", "run"],
            Difficulty.MEDIUM: ["house", "water", "light"],
            Difficulty.HARD: ["complex", "analysis", "structure"]
        }
        
        def mock_get_words(difficulty):
            return mock_word_data.get(difficulty, [])
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.tsv') as temp_file:
            temp_filename = temp_file.name
        
        try:
            with patch.object(self.generator, '_get_words_for_difficulty', side_effect=mock_get_words):
                self.generator.save_merged(temp_filename)
            
            # Read and verify the file content
            with open(temp_filename, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Check header
            self.assertIn("difficulty\tentry\n", content)
            
            # Check that words from all difficulties are present
            self.assertIn("simple\tcat", content)
            self.assertIn("medium\thouse", content)
            self.assertIn("hard\tcomplex", content)
            
        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_save_merged_sorted_output(self):
        """Test that exported data is sorted by difficulty and word"""
        mock_word_data = {
            Difficulty.MEDIUM: ["zebra", "apple"],
            Difficulty.SIMPLE: ["dog", "cat"]
        }
        
        def mock_get_words(difficulty):
            return mock_word_data.get(difficulty, [])
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.tsv') as temp_file:
            temp_filename = temp_file.name
        
        try:
            with patch.object(self.generator, '_get_words_for_difficulty', side_effect=mock_get_words):
                self.generator.save_merged(temp_filename)
            
            with open(temp_filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            # Skip header and check order
            data_lines = lines[1:]
            
            # Should be sorted by difficulty first (simple before medium), then alphabetically
            expected_order = [
                "simple\tcat\n",
                "simple\tdog\n", 
                "medium\tapple\n",
                "medium\tzebra\n"
            ]
            
            self.assertEqual(data_lines, expected_order)
            
        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_save_merged_special_characters(self):
        """Test export with words containing special characters"""
        mock_word_data = {
            Difficulty.SIMPLE: ["word\twith\ttabs", "word\nwith\nnewlines", "normal_word"]
        }
        
        def mock_get_words(difficulty):
            return mock_word_data.get(difficulty, [])
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.tsv') as temp_file:
            temp_filename = temp_file.name
        
        try:
            with patch.object(self.generator, '_get_words_for_difficulty', side_effect=mock_get_words):
                self.generator.save_merged(temp_filename)
            
            with open(temp_filename, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Check that special characters are escaped
            self.assertIn("simple\tword\\twith\\ttabs", content)
            self.assertIn("simple\tword\\nwith\\nnewlines", content)
            self.assertIn("simple\tnormal_word", content)
            
        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_save_merged_empty_filename(self):
        """Test that empty filename raises ValueError"""
        with self.assertRaises(ValueError) as context:
            self.generator.save_merged("")
        
        self.assertIn("Filename cannot be empty", str(context.exception))
    
    def test_save_merged_whitespace_filename(self):
        """Test that whitespace-only filename raises ValueError"""
        with self.assertRaises(ValueError) as context:
            self.generator.save_merged("   ")
        
        self.assertIn("Filename cannot be empty", str(context.exception))
    
    def test_save_merged_no_words_available(self):
        """Test error when no words are available for export"""
        def mock_get_words(difficulty):
            raise Exception("No words available")
        
        with patch.object(self.generator, '_get_words_for_difficulty', side_effect=mock_get_words):
            with self.assertRaises(RuntimeError) as context:
                self.generator.save_merged("test.tsv")
        
        self.assertIn("No words available to export", str(context.exception))
    
    def test_save_merged_permission_error(self):
        """Test handling of permission errors"""
        mock_word_data = {Difficulty.SIMPLE: ["test"]}
        
        def mock_get_words(difficulty):
            return mock_word_data.get(difficulty, [])
        
        with patch.object(self.generator, '_get_words_for_difficulty', side_effect=mock_get_words):
            with patch("builtins.open", side_effect=PermissionError("Access denied")):
                with self.assertRaises(PermissionError) as context:
                    self.generator.save_merged("test.tsv")
                
                self.assertIn("Permission denied writing to file", str(context.exception))
    
    def test_save_merged_disk_space_error(self):
        """Test handling of disk space errors"""
        mock_word_data = {Difficulty.SIMPLE: ["test"]}
        
        def mock_get_words(difficulty):
            return mock_word_data.get(difficulty, [])
        
        with patch.object(self.generator, '_get_words_for_difficulty', side_effect=mock_get_words):
            with patch("builtins.open", side_effect=OSError("No space left on device")):
                with self.assertRaises(OSError) as context:
                    self.generator.save_merged("test.tsv")
                
                self.assertIn("Insufficient disk space", str(context.exception))
    
    def test_save_merged_creates_directory(self):
        """Test that export creates directory if it doesn't exist"""
        mock_word_data = {Difficulty.SIMPLE: ["test"]}
        
        def mock_get_words(difficulty):
            return mock_word_data.get(difficulty, [])
        
        with tempfile.TemporaryDirectory() as temp_dir:
            nested_path = os.path.join(temp_dir, "subdir", "test.tsv")
            
            with patch.object(self.generator, '_get_words_for_difficulty', side_effect=mock_get_words):
                self.generator.save_merged(nested_path)
            
            # Directory should be created and file should exist
            self.assertTrue(os.path.exists(nested_path))
            
            # Verify content
            with open(nested_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.assertIn("difficulty\tentry\n", content)
                self.assertIn("simple\ttest", content)
    
    def test_save_merged_partial_difficulty_failure(self):
        """Test export when some difficulties fail to load"""
        def mock_get_words(difficulty):
            if difficulty == Difficulty.SIMPLE:
                return ["simple_word"]
            elif difficulty == Difficulty.MEDIUM:
                raise Exception("Medium difficulty failed")
            else:
                return ["other_word"]
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.tsv') as temp_file:
            temp_filename = temp_file.name
        
        try:
            with patch.object(self.generator, '_get_words_for_difficulty', side_effect=mock_get_words):
                self.generator.save_merged(temp_filename)
            
            with open(temp_filename, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Should contain words from successful difficulties
            self.assertIn("simple\tsimple_word", content)
            self.assertIn("other_word", content)
            # Should not contain medium difficulty words
            self.assertNotIn("medium\t", content)
            
        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_save_merged_unicode_words(self):
        """Test export with Unicode words"""
        mock_word_data = {
            Difficulty.SIMPLE: ["café", "naïve", "résumé", "漢字"]
        }
        
        def mock_get_words(difficulty):
            return mock_word_data.get(difficulty, [])
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.tsv') as temp_file:
            temp_filename = temp_file.name
        
        try:
            with patch.object(self.generator, '_get_words_for_difficulty', side_effect=mock_get_words):
                self.generator.save_merged(temp_filename)
            
            with open(temp_filename, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Check that Unicode words are preserved
            self.assertIn("simple\tcafé", content)
            self.assertIn("simple\tnaïve", content)
            self.assertIn("simple\trésumé", content)
            self.assertIn("simple\t漢字", content)
            
        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_save_merged_large_dataset(self):
        """Test export with a large number of words"""
        # Create a large dataset
        large_word_list = [f"word_{i}" for i in range(1000)]
        mock_word_data = {Difficulty.MEDIUM: large_word_list}
        
        def mock_get_words(difficulty):
            return mock_word_data.get(difficulty, [])
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.tsv') as temp_file:
            temp_filename = temp_file.name
        
        try:
            with patch.object(self.generator, '_get_words_for_difficulty', side_effect=mock_get_words):
                self.generator.save_merged(temp_filename)
            
            with open(temp_filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            # Should have header + 1000 data lines
            self.assertEqual(len(lines), 1001)
            
            # Check first and last entries
            self.assertEqual(lines[1].strip(), "medium\tword_0")
            self.assertEqual(lines[-1].strip(), "medium\tword_999")
            
        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)


if __name__ == '__main__':
    unittest.main()