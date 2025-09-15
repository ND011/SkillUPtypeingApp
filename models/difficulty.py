"""
Difficulty levels and data models for the Advanced Word Generator
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Any, Optional


class Difficulty(Enum):
    """Enumeration of difficulty levels for word generation"""
    SIMPLE = "simple"
    MEDIUM = "medium"
    HARD = "hard"
    EXTRA_HARD = "extra_hard"


@dataclass
class WordEntry:
    """Represents a word entry with metadata"""
    text: str
    difficulty: Difficulty
    source_file: str
    is_phrase: bool = False
    
    def __post_init__(self):
        """Validate word entry after initialization"""
        if not self.text or not self.text.strip():
            raise ValueError("Word text cannot be empty")
        if not isinstance(self.difficulty, Difficulty):
            raise ValueError("Difficulty must be a Difficulty enum value")
        if not self.source_file:
            raise ValueError("Source file cannot be empty")


@dataclass
class GenerationRequest:
    """Request parameters for word generation"""
    difficulty: Optional[Difficulty] = None
    count: Optional[int] = None
    duration_seconds: Optional[int] = None
    target_wpm: Optional[int] = None
    lines: Optional[int] = None
    max_line_chars: Optional[int] = None
    weights: Optional[Dict[Difficulty, float]] = None
    total_count: Optional[int] = None
    
    def __post_init__(self):
        """Validate generation request parameters"""
        if self.count is not None and self.count <= 0:
            raise ValueError("Count must be positive")
        if self.duration_seconds is not None and self.duration_seconds <= 0:
            raise ValueError("Duration must be positive")
        if self.target_wpm is not None and self.target_wpm <= 0:
            raise ValueError("Target WPM must be positive")
        if self.lines is not None and self.lines <= 0:
            raise ValueError("Lines must be positive")
        if self.max_line_chars is not None and self.max_line_chars <= 0:
            raise ValueError("Max line chars must be positive")
        if self.total_count is not None and self.total_count <= 0:
            raise ValueError("Total count must be positive")


@dataclass
class GenerationResult:
    """Result of word generation with metadata"""
    words: List[str]
    metadata: Dict[str, Any]
    generation_time: float
    seed_used: Optional[int] = None
    
    def __post_init__(self):
        """Validate generation result"""
        if not isinstance(self.words, list):
            raise ValueError("Words must be a list")
        if not isinstance(self.metadata, dict):
            raise ValueError("Metadata must be a dictionary")
        if self.generation_time < 0:
            raise ValueError("Generation time cannot be negative")