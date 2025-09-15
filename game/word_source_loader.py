"""
Word source loading system for the Advanced Word Generator
"""

import os
import logging
from typing import List, Dict, Optional
from models.difficulty import Difficulty, WordEntry


class WordSourceLoader:
    """Handles loading and caching of word files with phrase support"""
    
    def __init__(self):
        self._word_cache: Dict[Difficulty, List[str]] = {}
        self._file_mappings = {
            Difficulty.SIMPLE: 'simple_words_large.txt',
            Difficulty.MEDIUM: 'medium_unique_words.txt',
            Difficulty.HARD: 'hard_words_expanded.txt',
            Difficulty.EXTRA_HARD: 'extra_hard_words_extended.txt'
        }
        self.logger = logging.getLogger(__name__)
    
    def load_file(self, filepath: str, allow_phrases: bool = False) -> List[str]:
        """
        Load words from a file with encoding detection and phrase support
        
        Args:
            filepath: Path to the word file
            allow_phrases: Whether to preserve multi-word entries
            
        Returns:
            List of words/phrases from the file
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            PermissionError: If the file can't be read
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Word file not found: {filepath}")
        
        words = []
        encodings_to_try = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
        
        for encoding in encodings_to_try:
            try:
                with open(filepath, 'r', encoding=encoding) as file:
                    for line_num, line in enumerate(file, 1):
                        line = line.strip()
                        if not line or line.startswith('#'):  # Skip empty lines and comments
                            continue
                        
                        if allow_phrases:
                            # Keep lines as-is, including phrases
                            words.append(line)
                        else:
                            # Split multi-word entries if phrases not allowed
                            if ' ' in line:
                                words.extend(word.strip() for word in line.split() if word.strip())
                            else:
                                words.append(line)
                
                self.logger.info(f"Loaded {len(words)} entries from {filepath} using {encoding} encoding")
                return words
                
            except UnicodeDecodeError:
                continue
            except PermissionError:
                raise PermissionError(f"Permission denied reading file: {filepath}")
            except Exception as e:
                self.logger.error(f"Error reading file {filepath} with {encoding}: {e}")
                continue
        
        raise ValueError(f"Could not decode file {filepath} with any supported encoding")
    
    def get_words_for_difficulty(self, difficulty: Difficulty) -> List[str]:
        """
        Get words for a specific difficulty level, loading from cache or file
        
        Args:
            difficulty: The difficulty level to get words for
            
        Returns:
            List of words for the difficulty level
            
        Raises:
            FileNotFoundError: If the difficulty file doesn't exist
        """
        if difficulty in self._word_cache:
            return self._word_cache[difficulty].copy()
        
        if difficulty not in self._file_mappings:
            raise ValueError(f"No file mapping found for difficulty: {difficulty}")
        
        filename = self._file_mappings[difficulty]
        
        # Try to load from current directory first, then from SPEED directory
        possible_paths = [
            filename,
            os.path.join('SPEED', filename),
            os.path.join('..', filename)
        ]
        
        for filepath in possible_paths:
            try:
                words = self.load_file(filepath, allow_phrases=True)
                self._word_cache[difficulty] = words
                return words.copy()
            except FileNotFoundError:
                continue
        
        # If no file found, create a fallback with basic words
        self.logger.warning(f"No word file found for {difficulty}, using fallback words")
        fallback_words = self._get_fallback_words(difficulty)
        self._word_cache[difficulty] = fallback_words
        return fallback_words.copy()
    
    def _get_fallback_words(self, difficulty: Difficulty) -> List[str]:
        """Generate fallback words when files are not available"""
        base_words = [
            "the", "and", "for", "are", "but", "not", "you", "all", "can", "had",
            "her", "was", "one", "our", "out", "day", "get", "has", "him", "his",
            "how", "man", "new", "now", "old", "see", "two", "way", "who", "boy"
        ]
        
        medium_words = [
            "about", "after", "again", "before", "being", "below", "could", "every",
            "first", "found", "great", "group", "hand", "head", "help", "here"
        ]
        
        hard_words = [
            "ability", "absence", "academy", "account", "achieve", "acquire", "address",
            "advance", "against", "already", "another", "anxiety", "anybody", "anymore",
            "anywhere", "approve", "arrange", "article", "attempt", "attract", "average"
        ]
        
        extra_hard_words = [
            "absolutely", "accelerate", "accessible", "accomplish", "accordance", "accumulate",
            "achievement", "acknowledge", "additional", "administration", "advantage", "adventure",
            "advertising", "afternoon", "aggressive", "algorithm", "alternative", "ambassador",
            "anniversary", "announcement", "application", "appointment", "appreciate", "appropriate"
        ]
        
        if difficulty == Difficulty.SIMPLE:
            return base_words
        elif difficulty == Difficulty.MEDIUM:
            return base_words + medium_words
        elif difficulty == Difficulty.HARD:
            return base_words + medium_words + hard_words
        else:  # EXTRA_HARD
            return base_words + medium_words + hard_words + extra_hard_words
    
    def reload_sources(self) -> None:
        """Clear cache and reload all word sources"""
        self._word_cache.clear()
        self.logger.info("Word source cache cleared")
    
    def get_available_difficulties(self) -> List[Difficulty]:
        """Get list of difficulties that have word sources available"""
        available = []
        for difficulty in Difficulty:
            try:
                words = self.get_words_for_difficulty(difficulty)
                if words:
                    available.append(difficulty)
            except Exception:
                continue
        return available
    
    def get_word_count_for_difficulty(self, difficulty: Difficulty) -> int:
        """Get the number of words available for a difficulty level"""
        try:
            words = self.get_words_for_difficulty(difficulty)
            return len(words)
        except Exception:
            return 0