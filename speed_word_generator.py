"""
Advanced Word Generator for SPEED typing application
"""

import random
import time
import logging
from typing import List, Dict, Optional
from models.difficulty import Difficulty, GenerationResult
from game.word_source_loader import WordSourceLoader


class WordGenerator:
    """
    Advanced word generator with multiple generation strategies
    """
    
    def __init__(self, seed: Optional[int] = None):
        """
        Initialize the word generator
        
        Args:
            seed: Optional seed for reproducible random generation
        """
        self.seed = seed
        self._random = random.Random(seed)
        
        self.word_loader = WordSourceLoader()
        self.logger = logging.getLogger(__name__)
        self._sources_loaded = False
        self._allow_phrases = False
        self._generated_words_history = []  # Track generated words with metadata
        
        # Configuration
        self.config = {
            'session_buffer_percentage': 10,
            'default_paragraph_lines': 6,
            'default_line_chars': 200,
            'cache_word_sources': True,
            'export_format': 'tsv'
        }
        
        # Time-based generation settings
        self.time_options = [1, 2, 3, 5, 7, 10]  # Available minute options
        self.word_counts = [70, 140, 210, 350, 490, 700]  # Specific word counts for each time option
    
    def load_default_sources(self, allow_phrases: bool = False) -> None:
        """
        Load default word sources for all difficulty levels
        
        Args:
            allow_phrases: Whether to preserve multi-word entries as complete units
        """
        self._allow_phrases = allow_phrases
        
        try:
            # Pre-load all difficulty levels to verify availability
            loaded_difficulties = []
            for difficulty in Difficulty:
                try:
                    words = self.word_loader.get_words_for_difficulty(difficulty)
                    if words:
                        loaded_difficulties.append(difficulty)
                        self.logger.info(f"Loaded {len(words)} words for {difficulty.value}")
                except Exception as e:
                    self.logger.warning(f"Could not load words for {difficulty.value}: {e}")
            
            if not loaded_difficulties:
                raise RuntimeError("No word sources could be loaded")
            
            self._sources_loaded = True
            self.logger.info(f"Successfully loaded word sources for {len(loaded_difficulties)} difficulty levels")
            
        except Exception as e:
            self.logger.error(f"Failed to load default sources: {e}")
            raise RuntimeError(f"Failed to load word sources: {e}")
    
    def _ensure_sources_loaded(self) -> None:
        """Ensure word sources are loaded before generation"""
        if not self._sources_loaded:
            self.load_default_sources(self._allow_phrases)
    
    def _get_words_for_difficulty(self, difficulty: Difficulty) -> List[str]:
        """Get words for a specific difficulty level"""
        self._ensure_sources_loaded()
        return self.word_loader.get_words_for_difficulty(difficulty)
    
    def _create_generation_result(self, words: List[str], metadata: Dict) -> GenerationResult:
        """Create a GenerationResult with timing and metadata"""
        return GenerationResult(
            words=words,
            metadata=metadata,
            generation_time=time.time(),
            seed_used=self.seed
        )
    
    def get_available_difficulties(self) -> List[Difficulty]:
        """Get list of available difficulty levels"""
        self._ensure_sources_loaded()
        return self.word_loader.get_available_difficulties()
    
    def get_word_count_for_difficulty(self, difficulty: Difficulty) -> int:
        """Get the number of words available for a difficulty level"""
        self._ensure_sources_loaded()
        return self.word_loader.get_word_count_for_difficulty(difficulty)
    
    def reload_sources(self) -> None:
        """Reload all word sources"""
        self.word_loader.reload_sources()
        self._sources_loaded = False
        self.logger.info("Word sources reloaded")
    
    def generate_words(self, difficulty: Difficulty, count: int) -> List[str]:
        """
        Generate a specific number of words for a given difficulty level
        
        Args:
            difficulty: The difficulty level for word generation
            count: The exact number of words to generate
            
        Returns:
            List of generated words
            
        Raises:
            ValueError: If count is not positive
            RuntimeError: If word sources are not available
        """
        if count <= 0:
            raise ValueError("Count must be positive")
        
        start_time = time.time()
        
        # Get available words for the difficulty
        available_words = self._get_words_for_difficulty(difficulty)
        
        if not available_words:
            raise RuntimeError(f"No words available for difficulty: {difficulty.value}")
        
        # If we need more words than available, we'll cycle through them
        if count <= len(available_words):
            # Simple case: we have enough unique words
            selected_words = self._random.sample(available_words, count)
        else:
            # Need to repeat words - use random selection with replacement
            selected_words = []
            remaining_count = count
            
            while remaining_count > 0:
                # Take up to the full word list or remaining count, whichever is smaller
                batch_size = min(remaining_count, len(available_words))
                
                if batch_size == len(available_words):
                    # Take all words and shuffle them
                    batch = available_words.copy()
                    self._random.shuffle(batch)
                else:
                    # Take a random sample
                    batch = self._random.sample(available_words, batch_size)
                
                selected_words.extend(batch)
                remaining_count -= batch_size
            
            # Final shuffle to mix any repeated words
            self._random.shuffle(selected_words)
        
        generation_time = time.time() - start_time
        
        self.logger.info(f"Generated {len(selected_words)} words for {difficulty.value} in {generation_time:.3f}s")
        
        return selected_words
    
    def generate_for_session(self, difficulty: Difficulty, duration_seconds: int, target_wpm: int) -> List[str]:
        """
        Generate words for a typing session based on duration and target WPM
        
        Args:
            difficulty: The difficulty level for word generation
            duration_seconds: Session duration in seconds
            target_wpm: Target words per minute
            
        Returns:
            List of generated words with buffer
            
        Raises:
            ValueError: If duration or target_wpm are not positive
        """
        if duration_seconds <= 0:
            raise ValueError("Duration must be positive")
        if target_wpm <= 0:
            raise ValueError("Target WPM must be positive")
        
        # Calculate base word count needed
        duration_minutes = duration_seconds / 60.0
        base_word_count = int(duration_minutes * target_wpm)
        
        # Add buffer percentage (default 10%)
        buffer_percentage = self.config['session_buffer_percentage']
        buffer_multiplier = 1.0 + (buffer_percentage / 100.0)
        total_word_count = int(base_word_count * buffer_multiplier)
        
        # Ensure minimum word count
        total_word_count = max(total_word_count, 10)
        
        self.logger.info(f"Session calculation: {duration_seconds}s at {target_wpm} WPM = {base_word_count} base words + {buffer_percentage}% buffer = {total_word_count} total words")
        
        # Use the fixed count generation method
        return self.generate_words(difficulty, total_word_count)
    
    def generate_for_time_selection(self, difficulty: Difficulty, minutes: int) -> List[str]:
        """
        Generate words based on time selection with specific word counts: 70, 140, 210, 350, 490, 700
        
        Args:
            difficulty: The difficulty level for word generation
            minutes: Selected time in minutes (must be in [1, 2, 3, 5, 7, 10])
            
        Returns:
            List of generated words
            
        Raises:
            ValueError: If minutes is not in the allowed time options
        """
        if minutes not in self.time_options:
            raise ValueError(f"Minutes must be one of {self.time_options}, got {minutes}")
        
        start_time = time.time()
        
        # Get word count from the predefined mapping
        word_count = self.calculate_word_count_for_time(minutes)
        
        self.logger.info(f"Time-based generation: {minutes} minutes -> {word_count} words")
        
        # Generate the words using the fixed count method
        words = self.generate_words(difficulty, word_count)
        
        generation_time = time.time() - start_time
        self.logger.info(f"Generated {len(words)} words for {minutes}-minute selection in {generation_time:.3f}s")
        
        return words
    
    def get_available_time_options(self) -> List[int]:
        """
        Get the available time options in minutes
        
        Returns:
            List of available time options in minutes
        """
        return self.time_options.copy()
    
    def calculate_word_count_for_time(self, minutes: int) -> int:
        """
        Calculate how many words will be generated for a given time selection
        
        Args:
            minutes: Time selection in minutes
            
        Returns:
            Number of words that will be generated
            
        Raises:
            ValueError: If minutes is not in the allowed time options
        """
        if minutes not in self.time_options:
            raise ValueError(f"Minutes must be one of {self.time_options}, got {minutes}")
        
        # Map minutes to specific word counts
        time_to_words = dict(zip(self.time_options, self.word_counts))
        return time_to_words[minutes]
    
    def generate_paragraph(self, difficulty: Difficulty, lines: int, max_line_chars: int) -> List[str]:
        """
        Generate words formatted into paragraph lines with character limits
        
        Args:
            difficulty: The difficulty level for word generation
            lines: Number of lines to generate
            max_line_chars: Maximum characters per line
            
        Returns:
            List of strings, each representing a line of the paragraph
            
        Raises:
            ValueError: If lines or max_line_chars are not positive
        """
        if lines <= 0:
            raise ValueError("Lines must be positive")
        if max_line_chars <= 0:
            raise ValueError("Max line chars must be positive")
        
        start_time = time.time()
        
        # Estimate words needed - assume average word length of 5 chars + 1 space
        avg_word_length = 6
        estimated_words_per_line = max(1, max_line_chars // avg_word_length)
        total_estimated_words = lines * estimated_words_per_line
        
        # Generate more words than estimated to ensure we have enough
        buffer_words = int(total_estimated_words * 1.5)
        available_words = self.generate_words(difficulty, buffer_words)
        
        # Format words into lines
        formatted_lines = []
        word_index = 0
        
        for line_num in range(lines):
            current_line = ""
            line_word_count = 0
            
            while word_index < len(available_words):
                word = available_words[word_index]
                
                # Check if adding this word would exceed the character limit
                if current_line:
                    test_line = current_line + " " + word
                else:
                    test_line = word
                
                if len(test_line) <= max_line_chars:
                    current_line = test_line
                    word_index += 1
                    line_word_count += 1
                else:
                    # Word would exceed limit, break to next line
                    break
            
            # If we couldn't fit any words on this line, force at least one
            if not current_line and word_index < len(available_words):
                current_line = available_words[word_index]
                word_index += 1
                line_word_count = 1
            
            # If we run out of words, generate more
            if not current_line and word_index >= len(available_words):
                additional_words = self.generate_words(difficulty, estimated_words_per_line * 2)
                available_words.extend(additional_words)
                continue
            
            formatted_lines.append(current_line)
            
            # If we've used all words and still need more lines, generate more
            if word_index >= len(available_words) and line_num < lines - 1:
                additional_words = self.generate_words(difficulty, estimated_words_per_line * (lines - line_num))
                available_words.extend(additional_words)
        
        generation_time = time.time() - start_time
        
        self.logger.info(f"Generated {len(formatted_lines)} paragraph lines for {difficulty.value} in {generation_time:.3f}s")
        
        return formatted_lines
    
    def generate_mixed(self, weights: Dict[Difficulty, float], total_count: int) -> List[str]:
        """
        Generate words with mixed difficulty levels according to specified weights
        
        Args:
            weights: Dictionary mapping difficulty levels to their weights (0.0 to 1.0)
            total_count: Total number of words to generate
            
        Returns:
            List of generated words from mixed difficulties
            
        Raises:
            ValueError: If total_count is not positive or weights are invalid
        """
        if total_count <= 0:
            raise ValueError("Total count must be positive")
        if not weights:
            raise ValueError("Weights dictionary cannot be empty")
        
        # Validate weights
        for difficulty, weight in weights.items():
            if not isinstance(difficulty, Difficulty):
                raise ValueError(f"Invalid difficulty in weights: {difficulty}")
            if weight < 0:
                raise ValueError(f"Weight cannot be negative for {difficulty}")
        
        start_time = time.time()
        
        # Normalize weights to sum to 1.0
        total_weight = sum(weights.values())
        if total_weight == 0:
            raise ValueError("Total weight cannot be zero")
        
        normalized_weights = {diff: weight / total_weight for diff, weight in weights.items()}
        
        # Calculate word counts for each difficulty
        difficulty_counts = {}
        allocated_count = 0
        
        # Allocate words proportionally
        for difficulty, weight in normalized_weights.items():
            count = int(total_count * weight)
            difficulty_counts[difficulty] = count
            allocated_count += count
        
        # Distribute any remaining words due to rounding
        remaining = total_count - allocated_count
        if remaining > 0:
            # Add remaining words to difficulties with highest fractional parts
            fractional_parts = []
            for difficulty, weight in normalized_weights.items():
                exact_count = total_count * weight
                fractional_part = exact_count - int(exact_count)
                fractional_parts.append((fractional_part, difficulty))
            
            # Sort by fractional part (descending) and add remaining words
            fractional_parts.sort(reverse=True)
            for i in range(remaining):
                if i < len(fractional_parts):
                    difficulty = fractional_parts[i][1]
                    difficulty_counts[difficulty] += 1
        
        # Generate words for each difficulty
        all_words = []
        for difficulty, count in difficulty_counts.items():
            if count > 0:
                try:
                    words = self.generate_words(difficulty, count)
                    all_words.extend(words)
                    self.logger.info(f"Generated {len(words)} words for {difficulty.value}")
                except Exception as e:
                    self.logger.warning(f"Could not generate words for {difficulty.value}: {e}")
                    # If a difficulty fails, try to compensate with other difficulties
                    if difficulty_counts:
                        # Add the failed count to the first available difficulty
                        first_available = next(iter(difficulty_counts.keys()))
                        if first_available != difficulty:
                            try:
                                compensation_words = self.generate_words(first_available, count)
                                all_words.extend(compensation_words)
                                self.logger.info(f"Compensated with {len(compensation_words)} words from {first_available.value}")
                            except Exception:
                                self.logger.error(f"Could not compensate for failed difficulty {difficulty.value}")
        
        # Shuffle the mixed words to distribute difficulties evenly
        self._random.shuffle(all_words)
        
        generation_time = time.time() - start_time
        
        self.logger.info(f"Generated {len(all_words)} mixed difficulty words in {generation_time:.3f}s")
        
        return all_words
    
    def save_merged(self, filename: str) -> None:
        """
        Save all generated words to a TSV file with difficulty levels
        
        Args:
            filename: Path to the output file
            
        Raises:
            ValueError: If filename is empty
            PermissionError: If file cannot be written
            OSError: If disk space or other I/O issues occur
        """
        if not filename or not filename.strip():
            raise ValueError("Filename cannot be empty")
        
        # Collect all words from different sources with their difficulties
        merged_data = []
        
        # Add words from all difficulty levels
        for difficulty in Difficulty:
            try:
                words = self._get_words_for_difficulty(difficulty)
                for word in words:
                    merged_data.append((difficulty.value, word.strip()))
            except Exception as e:
                self.logger.warning(f"Could not load words for {difficulty.value} during export: {e}")
                continue
        
        if not merged_data:
            raise RuntimeError("No words available to export")
        
        # Sort by difficulty and then by word for consistent output
        difficulty_order = {d.value: i for i, d in enumerate(Difficulty)}
        merged_data.sort(key=lambda x: (difficulty_order.get(x[0], 999), x[1].lower()))
        
        try:
            # Check if we can write to the directory
            import os
            directory = os.path.dirname(os.path.abspath(filename))
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            
            # Write TSV file
            with open(filename, 'w', encoding='utf-8', newline='') as file:
                # Write header
                file.write("difficulty\tentry\n")
                
                # Write data
                for difficulty, word in merged_data:
                    # Escape tabs and newlines in the word
                    escaped_word = word.replace('\t', '\\t').replace('\n', '\\n').replace('\r', '\\r')
                    file.write(f"{difficulty}\t{escaped_word}\n")
            
            self.logger.info(f"Exported {len(merged_data)} words to {filename}")
            
        except PermissionError:
            raise PermissionError(f"Permission denied writing to file: {filename}")
        except OSError as e:
            error_msg = str(e).lower()
            if "no space left on device" in error_msg or "disk full" in error_msg or "insufficient disk space" in error_msg:
                raise OSError(f"Insufficient disk space to write file: {filename}")
            else:
                raise OSError(f"Error writing file {filename}: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error writing file {filename}: {e}")