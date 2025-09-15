"""
Enhanced SPEED game engine with multiple modes and difficulty levels
"""

import time
import threading
import random
from typing import Optional, Callable, Dict, List, Tuple
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

from .database_manager import DatabaseManager, ScoreRecord
from .word_manager import WordManager
from .performance_calculator import PerformanceCalculator
from speed_word_generator import WordGenerator
from models.difficulty import Difficulty


class GameMode(Enum):
    """Different game modes available"""
    PRACTICE = "practice"
    TIMED_CHALLENGE = "timed_challenge"
    ACCURACY_FOCUS = "accuracy_focus"
    SPEED_BURST = "speed_burst"
    ENDURANCE = "endurance"


class DifficultyLevel(Enum):
    """Difficulty levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


@dataclass
class GameSession:
    """Enhanced game session data"""
    session_id: str
    user_name: str
    mode: GameMode
    difficulty: DifficultyLevel
    start_time: datetime
    target_text: str
    duration_seconds: int
    is_active: bool = False
    end_time: Optional[datetime] = None
    typed_text: str = ""
    current_wpm: float = 0.0
    current_accuracy: float = 0.0


class SpeedEngine:
    """Enhanced game engine for SPEED application"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.db_manager.initialize()  # Initialize the database
        self.word_manager = WordManager()
        self.performance_calc = PerformanceCalculator()
        
        # Initialize Advanced Word Generator
        self.word_generator = WordGenerator()
        try:
            self.word_generator.load_default_sources(allow_phrases=True)
        except Exception as e:
            print(f"Warning: Could not load advanced word generator: {e}")
            self.word_generator = None
        
        self.current_session: Optional[GameSession] = None
        self.session_timer: Optional[threading.Timer] = None
        self.update_callbacks: List[Callable] = []
        self.session_end_callbacks: List[Callable] = []

        
        self._lock = threading.Lock()
    
    def register_update_callback(self, callback: Callable):
        """Register callback for real-time updates"""
        self.update_callbacks.append(callback)
    
    def register_session_end_callback(self, callback: Callable):
        """Register callback for session end"""
        self.session_end_callbacks.append(callback)
    
    # Removed auto-stop callback registration
    
    def start_session(self, user_name: str, mode: GameMode, 
                     difficulty: DifficultyLevel, duration: int = 60) -> bool:
        """Start a new typing session"""
        with self._lock:
            if self.current_session and self.current_session.is_active:
                return False  # Session already active
            
            # Generate target text based on mode and difficulty
            target_text = self._generate_target_text(mode, difficulty, duration)
            
            # Calculate dynamic duration based on text length
            dynamic_duration = self._calculate_dynamic_duration(target_text, difficulty, mode)
            
            # Create new session
            session_id = f"{user_name}_{int(time.time())}"
            self.current_session = GameSession(
                session_id=session_id,
                user_name=user_name,
                mode=mode,
                difficulty=difficulty,
                start_time=datetime.now(),
                target_text=target_text,
                duration_seconds=dynamic_duration,
                is_active=True
            )
            
            # No automatic timer - sessions only end manually
            self.session_timer = None
            
            return True
    
    def start_time_based_session(self, user_name: str, mode: GameMode, 
                                difficulty: DifficultyLevel, minutes: int) -> bool:
        """Start a new typing session using time-based word generation"""
        with self._lock:
            if self.current_session and self.current_session.is_active:
                return False  # Session already active
            
            # Generate target text using time-based generation
            target_text = self._generate_time_based_text(mode, difficulty, minutes)
            
            # Calculate duration based on minutes selection
            duration_seconds = minutes * 60
            
            # Create new session
            session_id = f"{user_name}_{int(time.time())}"
            self.current_session = GameSession(
                session_id=session_id,
                user_name=user_name,
                mode=mode,
                difficulty=difficulty,
                start_time=datetime.now(),
                target_text=target_text,
                duration_seconds=duration_seconds,
                is_active=True
            )
            
            # No automatic timer - sessions only end manually
            self.session_timer = None
            
            return True
    
    def _calculate_dynamic_duration(self, text: str, difficulty: DifficultyLevel, mode: GameMode) -> int:
        """Calculate dynamic duration based on text length and complexity"""
        # Count words and lines
        words = text.split()
        lines = text.split('\n')
        word_count = len(words)
        line_count = len(lines)
        
        # Base time calculation: estimate based on expected WPM for difficulty
        expected_wpm_map = {
            DifficultyLevel.BEGINNER: 25,
            DifficultyLevel.INTERMEDIATE: 40,
            DifficultyLevel.ADVANCED: 55,
            DifficultyLevel.EXPERT: 70
        }
        
        expected_wpm = expected_wpm_map.get(difficulty, 40)
        
        # Calculate base time needed (words / WPM * 60 seconds)
        base_time = (word_count / expected_wpm) * 60
        
        # Add extra time based on complexity
        complexity_multiplier = 1.0
        
        # Mode-based adjustments
        if mode == GameMode.ACCURACY_FOCUS:
            complexity_multiplier = 1.5  # More time for accuracy
        elif mode == GameMode.SPEED_BURST:
            complexity_multiplier = 0.8  # Less time for speed
        elif mode == GameMode.ENDURANCE:
            complexity_multiplier = 1.2  # Slightly more time for endurance
        elif mode == GameMode.TIMED_CHALLENGE:
            complexity_multiplier = 1.3  # More time for challenge
        
        # Difficulty-based adjustments
        if difficulty == DifficultyLevel.EXPERT:
            complexity_multiplier *= 1.4  # Extra time for symbols and complexity
        elif difficulty == DifficultyLevel.ADVANCED:
            complexity_multiplier *= 1.2  # Some extra time for numbers/symbols
        
        # Line-based adjustment: more lines = more time
        line_bonus = max(0, (line_count - 5) * 5)  # 5 seconds per extra line beyond 5
        
        # Calculate final duration
        final_duration = int(base_time * complexity_multiplier + line_bonus)
        
        # Ensure minimum and maximum bounds
        min_duration = 30  # At least 30 seconds
        max_duration = 600  # At most 10 minutes
        
        return max(min_duration, min(max_duration, final_duration))
    
    def update_typed_text(self, typed_text: str):
        """Update the currently typed text and calculate real-time stats"""
        if not self.current_session or not self.current_session.is_active:
            return
        
        self.current_session.typed_text = typed_text
        
        # Calculate real-time performance
        elapsed_time = (datetime.now() - self.current_session.start_time).total_seconds()
        
        if elapsed_time > 0:
            wpm, accuracy = self.performance_calc.calculate_real_time_stats(
                typed_text, self.current_session.target_text, elapsed_time
            )
            
            self.current_session.current_wpm = wpm
            self.current_session.current_accuracy = accuracy
            
            # Notify callbacks
            for callback in self.update_callbacks:
                try:
                    callback(wpm, accuracy, self._get_progress_percentage())
                except Exception as e:
                    print(f"Error in update callback: {e}")
    
    def end_session(self) -> Optional[ScoreRecord]:
        """Manually end the current session"""
        with self._lock:
            if not self.current_session or not self.current_session.is_active:
                return None
            
            score_record = self._finalize_session()
            
            # Notify callbacks for manual session end too
            for callback in self.session_end_callbacks:
                try:
                    callback(score_record)
                except Exception as e:
                    print(f"Error in session end callback: {e}")
            
            return score_record
    
    # Removed auto-stop functionality
    
    def _finalize_session(self) -> Optional[ScoreRecord]:
        """Finalize the current session and save results"""
        if not self.current_session:
            return None
        
        # Cancel timer if still running
        if self.session_timer:
            self.session_timer.cancel()
            self.session_timer = None
        
        # Mark session as ended
        self.current_session.is_active = False
        self.current_session.end_time = datetime.now()
        
        # Calculate final performance
        total_time = (self.current_session.end_time - self.current_session.start_time).total_seconds()
        
        final_result = self.performance_calc.calculate_final_result(
            self.current_session.user_name,
            self.current_session.mode.value,
            self.current_session.typed_text,
            self.current_session.target_text,
            total_time
        )
        
        # Create score record
        score_record = ScoreRecord(
            id=None,
            user_name=self.current_session.user_name,
            wpm=final_result['wpm'],
            accuracy=final_result['accuracy'],
            level=self.current_session.difficulty.value,
            mode=self.current_session.mode.value,
            date=self.current_session.end_time,
            duration=int(total_time),
            total_characters=final_result['total_characters'],
            correct_characters=final_result['correct_characters']
        )
        
        # Don't save to database yet - let the UI ask for name first
        # The UI will save the score after getting the user's name
        
        return score_record
    
    def _generate_target_text(self, mode: GameMode, difficulty: DifficultyLevel, duration: int) -> str:
        """Generate target text based on mode and difficulty using Advanced Word Generator"""
        
        # Map difficulty levels to Advanced Word Generator difficulties
        difficulty_map = {
            DifficultyLevel.BEGINNER: Difficulty.SIMPLE,
            DifficultyLevel.INTERMEDIATE: Difficulty.MEDIUM,
            DifficultyLevel.ADVANCED: Difficulty.HARD,
            DifficultyLevel.EXPERT: Difficulty.EXTRA_HARD
        }
        
        advanced_difficulty = difficulty_map.get(difficulty, Difficulty.MEDIUM)
        
        # Use Advanced Word Generator if available
        if self.word_generator:
            try:
                if mode == GameMode.PRACTICE:
                    # Generate paragraph format for practice
                    lines = self.word_generator.generate_paragraph(advanced_difficulty, lines=6, max_line_chars=200)
                    return '\n'.join(lines)
                
                elif mode == GameMode.TIMED_CHALLENGE:
                    # Generate session-based words for timed challenge
                    target_wpm = self._get_target_wpm_for_difficulty(difficulty)
                    words = self.word_generator.generate_for_session(advanced_difficulty, duration, target_wpm)
                    return ' '.join(words)
                
                elif mode == GameMode.ACCURACY_FOCUS:
                    # Generate mixed difficulty for accuracy focus
                    weights = {
                        advanced_difficulty: 0.7,
                        Difficulty.HARD if advanced_difficulty != Difficulty.HARD else Difficulty.EXTRA_HARD: 0.3
                    }
                    words = self.word_generator.generate_mixed(weights, 100)
                    return ' '.join(words)
                
                elif mode == GameMode.SPEED_BURST:
                    # Generate shorter, focused word set for speed
                    words = self.word_generator.generate_words(advanced_difficulty, 50)
                    return ' '.join(words)
                
                elif mode == GameMode.ENDURANCE:
                    # Generate longer session for endurance
                    target_wpm = self._get_target_wpm_for_difficulty(difficulty)
                    words = self.word_generator.generate_for_session(advanced_difficulty, duration * 2, target_wpm)
                    return ' '.join(words)
                
                else:
                    # Default to practice mode
                    lines = self.word_generator.generate_paragraph(advanced_difficulty, lines=5, max_line_chars=180)
                    return '\n'.join(lines)
                    
            except Exception as e:
                print(f"Advanced Word Generator failed, falling back to legacy: {e}")
        
        # Fallback to legacy word manager
        if mode == GameMode.PRACTICE:
            return self.word_manager.get_practice_text(difficulty, duration)
        elif mode == GameMode.TIMED_CHALLENGE:
            return self.word_manager.get_challenge_text(difficulty, duration)
        elif mode == GameMode.ACCURACY_FOCUS:
            return self.word_manager.get_accuracy_text(difficulty, duration)
        elif mode == GameMode.SPEED_BURST:
            return self.word_manager.get_speed_text(difficulty, duration)
        elif mode == GameMode.ENDURANCE:
            return self.word_manager.get_endurance_text(difficulty, duration)
        else:
            return self.word_manager.get_practice_text(difficulty, duration)
    
    def _get_target_wpm_for_difficulty(self, difficulty: DifficultyLevel) -> int:
        """Get target WPM based on difficulty level"""
        wpm_map = {
            DifficultyLevel.BEGINNER: 25,
            DifficultyLevel.INTERMEDIATE: 40,
            DifficultyLevel.ADVANCED: 55,
            DifficultyLevel.EXPERT: 70
        }
        return wpm_map.get(difficulty, 40)
    
    def _generate_time_based_text(self, mode: GameMode, difficulty: DifficultyLevel, minutes: int) -> str:
        """Generate target text using time-based word generation (minutes * 7 words)"""
        
        # Map difficulty levels to Advanced Word Generator difficulties
        difficulty_map = {
            DifficultyLevel.BEGINNER: Difficulty.SIMPLE,
            DifficultyLevel.INTERMEDIATE: Difficulty.MEDIUM,
            DifficultyLevel.ADVANCED: Difficulty.HARD,
            DifficultyLevel.EXPERT: Difficulty.EXTRA_HARD
        }
        
        advanced_difficulty = difficulty_map.get(difficulty, Difficulty.MEDIUM)
        
        # Use Advanced Word Generator if available
        if self.word_generator:
            try:
                if mode == GameMode.TIMED_CHALLENGE:
                    # Use time-based generation for timed challenge
                    words = self.word_generator.generate_for_time_selection(advanced_difficulty, minutes)
                    return ' '.join(words)
                
                elif mode == GameMode.ACCURACY_FOCUS:
                    # Use time-based generation with mixed difficulty for accuracy
                    base_words = self.word_generator.generate_for_time_selection(advanced_difficulty, minutes)
                    return ' '.join(base_words)
                
                elif mode == GameMode.SPEED_BURST:
                    # Use time-based generation for speed burst
                    words = self.word_generator.generate_for_time_selection(advanced_difficulty, minutes)
                    return ' '.join(words)
                
                elif mode == GameMode.ENDURANCE:
                    # Use time-based generation for endurance
                    words = self.word_generator.generate_for_time_selection(advanced_difficulty, minutes)
                    return ' '.join(words)
                
                else:
                    # Default to time-based generation
                    words = self.word_generator.generate_for_time_selection(advanced_difficulty, minutes)
                    return ' '.join(words)
                    
            except Exception as e:
                print(f"Time-based Word Generator failed, falling back to legacy: {e}")
        
        # Fallback to legacy word manager with estimated duration
        duration = minutes * 60
        if mode == GameMode.TIMED_CHALLENGE:
            return self.word_manager.get_challenge_text(difficulty, duration)
        elif mode == GameMode.ACCURACY_FOCUS:
            return self.word_manager.get_accuracy_text(difficulty, duration)
        elif mode == GameMode.SPEED_BURST:
            return self.word_manager.get_speed_text(difficulty, duration)
        elif mode == GameMode.ENDURANCE:
            return self.word_manager.get_endurance_text(difficulty, duration)
        else:
            return self.word_manager.get_challenge_text(difficulty, duration)
    
    def get_current_session(self) -> Optional[GameSession]:
        """Get the current active session"""
        return self.current_session
    
    def get_time_remaining(self) -> float:
        """Get remaining time in current session"""
        if not self.current_session or not self.current_session.is_active:
            return 0.0
        
        elapsed = (datetime.now() - self.current_session.start_time).total_seconds()
        remaining = self.current_session.duration_seconds - elapsed
        return max(0.0, remaining)
    
    def get_elapsed_time(self) -> float:
        """Get elapsed time in current session"""
        if not self.current_session or not self.current_session.is_active:
            return 0.0
        
        return (datetime.now() - self.current_session.start_time).total_seconds()
    
    def _get_progress_percentage(self) -> float:
        """Get typing progress as percentage"""
        if not self.current_session:
            return 0.0
        
        typed_length = len(self.current_session.typed_text)
        target_length = len(self.current_session.target_text)
        
        if target_length == 0:
            return 0.0
        
        return min(100.0, (typed_length / target_length) * 100)
    
    def is_session_active(self) -> bool:
        """Check if a session is currently active"""
        return self.current_session is not None and self.current_session.is_active
    
    def get_user_best_scores(self, user_name: str, limit: int = 5) -> List[ScoreRecord]:
        """Get user's best scores"""
        return self.db_manager.get_user_scores(user_name, limit)
    
    def get_leaderboard(self, mode: str = None, limit: int = 10) -> List[ScoreRecord]:
        """Get global leaderboard"""
        return self.db_manager.get_leaderboard(mode, limit)
    
    def reset_session(self):
        """Reset/cancel current session"""
        with self._lock:
            if self.session_timer:
                self.session_timer.cancel()
                self.session_timer = None
            
            self.current_session = None
    
    def cleanup(self):
        """Clean up resources"""
        self.reset_session()
        if self.db_manager:
            self.db_manager.close()