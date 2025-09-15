"""
Enhanced performance calculator with detailed metrics and analysis
"""

import time
import math
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class DetailedPerformance:
    """Detailed performance metrics"""
    wpm: float
    accuracy: float
    net_wpm: float
    total_characters: int
    correct_characters: int
    incorrect_characters: int
    total_words: int
    correct_words: int
    keystroke_speed: float  # keystrokes per second
    consistency_score: float  # 0-100, measures typing consistency
    error_rate: float  # errors per minute
    backspace_count: int
    time_per_word: float  # average seconds per word


class PerformanceCalculator:
    """Enhanced performance calculator with comprehensive metrics"""
    
    def __init__(self):
        self.keystroke_times = []  # Track timing between keystrokes
        self.error_positions = []  # Track where errors occur
        self.backspace_count = 0
        self.last_keystroke_time = None
    
    def reset_session(self):
        """Reset tracking for new session"""
        self.keystroke_times = []
        self.error_positions = []
        self.backspace_count = 0
        self.last_keystroke_time = None
    
    def record_keystroke(self, is_correct: bool, is_backspace: bool = False):
        """Record a keystroke for detailed analysis"""
        current_time = time.time()
        
        if self.last_keystroke_time is not None:
            interval = current_time - self.last_keystroke_time
            self.keystroke_times.append(interval)
        
        if is_backspace:
            self.backspace_count += 1
        elif not is_correct:
            self.error_positions.append(len(self.keystroke_times))
        
        self.last_keystroke_time = current_time
    
    def calculate_wpm(self, typed_text: str, time_elapsed_seconds: float) -> float:
        """Calculate Words Per Minute (standard 5-character word definition)"""
        if time_elapsed_seconds <= 0:
            return 0.0
        
        total_characters = len(typed_text)
        time_minutes = time_elapsed_seconds / 60.0
        wpm = (total_characters / 5.0) / time_minutes
        
        return round(wpm, 1)
    
    def calculate_accuracy(self, typed_text: str, target_text: str) -> float:
        """Calculate typing accuracy percentage"""
        if not typed_text:
            return 0.0
        
        correct_characters = 0
        comparison_length = min(len(typed_text), len(target_text))
        
        for i in range(comparison_length):
            if typed_text[i] == target_text[i]:
                correct_characters += 1
        
        accuracy = (correct_characters / len(typed_text)) * 100.0
        return round(accuracy, 1)
    
    def calculate_net_wpm(self, typed_text: str, target_text: str, time_elapsed_seconds: float) -> float:
        """Calculate Net WPM (accounting for errors)"""
        if time_elapsed_seconds <= 0:
            return 0.0
        
        gross_wpm = self.calculate_wpm(typed_text, time_elapsed_seconds)
        errors = self._count_errors(typed_text, target_text)
        time_minutes = time_elapsed_seconds / 60.0
        
        net_wpm = gross_wpm - (errors / time_minutes)
        return max(0.0, round(net_wpm, 1))
    
    def calculate_consistency_score(self) -> float:
        """Calculate typing consistency based on keystroke timing"""
        if len(self.keystroke_times) < 10:
            return 0.0
        
        # Calculate coefficient of variation (lower is more consistent)
        mean_time = sum(self.keystroke_times) / len(self.keystroke_times)
        variance = sum((t - mean_time) ** 2 for t in self.keystroke_times) / len(self.keystroke_times)
        std_dev = math.sqrt(variance)
        
        if mean_time == 0:
            return 0.0
        
        coefficient_of_variation = std_dev / mean_time
        
        # Convert to 0-100 scale (lower CV = higher consistency score)
        consistency_score = max(0, 100 - (coefficient_of_variation * 100))
        return round(consistency_score, 1)
    
    def calculate_keystroke_speed(self, time_elapsed_seconds: float) -> float:
        """Calculate keystrokes per second"""
        if time_elapsed_seconds <= 0 or not self.keystroke_times:
            return 0.0
        
        total_keystrokes = len(self.keystroke_times)
        return round(total_keystrokes / time_elapsed_seconds, 2)
    
    def calculate_error_rate(self, time_elapsed_seconds: float) -> float:
        """Calculate errors per minute"""
        if time_elapsed_seconds <= 0:
            return 0.0
        
        time_minutes = time_elapsed_seconds / 60.0
        error_count = len(self.error_positions) + self.backspace_count
        
        return round(error_count / time_minutes, 1)
    
    def calculate_real_time_stats(self, typed_text: str, target_text: str, elapsed_time: float) -> Tuple[float, float]:
        """Calculate real-time WPM and accuracy"""
        if elapsed_time < 0.1:
            return 0.0, 0.0
        
        wpm = self.calculate_wpm(typed_text, elapsed_time)
        accuracy = self.calculate_accuracy(typed_text, target_text)
        
        return wpm, accuracy
    
    def calculate_final_result(self, user_name: str, mode: str, typed_text: str, 
                             target_text: str, total_time: float) -> Dict:
        """Calculate comprehensive final performance metrics"""
        
        # Basic metrics
        wpm = self.calculate_wpm(typed_text, total_time)
        accuracy = self.calculate_accuracy(typed_text, target_text)
        net_wpm = self.calculate_net_wpm(typed_text, target_text, total_time)
        
        # Character analysis
        total_characters = len(typed_text)
        correct_characters = self._count_correct_characters(typed_text, target_text)
        incorrect_characters = total_characters - correct_characters
        
        # Word analysis
        typed_words = typed_text.split()
        target_words = target_text.split()
        total_words = len(typed_words)
        correct_words = self._count_correct_words(typed_words, target_words)
        
        # Advanced metrics
        keystroke_speed = self.calculate_keystroke_speed(total_time)
        consistency_score = self.calculate_consistency_score()
        error_rate = self.calculate_error_rate(total_time)
        time_per_word = total_time / max(1, total_words)
        
        return {
            'user_name': user_name,
            'mode': mode,
            'wpm': wpm,
            'accuracy': accuracy,
            'net_wpm': net_wpm,
            'total_characters': total_characters,
            'correct_characters': correct_characters,
            'incorrect_characters': incorrect_characters,
            'total_words': total_words,
            'correct_words': correct_words,
            'keystroke_speed': keystroke_speed,
            'consistency_score': consistency_score,
            'error_rate': error_rate,
            'backspace_count': self.backspace_count,
            'time_per_word': round(time_per_word, 2),
            'total_time': total_time
        }
    
    def get_performance_grade(self, wpm: float, accuracy: float) -> str:
        """Get performance grade based on WPM and accuracy"""
        if wpm >= 80 and accuracy >= 98:
            return "Exceptional"
        elif wpm >= 70 and accuracy >= 95:
            return "Excellent"
        elif wpm >= 60 and accuracy >= 92:
            return "Very Good"
        elif wpm >= 50 and accuracy >= 88:
            return "Good"
        elif wpm >= 40 and accuracy >= 85:
            return "Average"
        elif wpm >= 30 and accuracy >= 80:
            return "Below Average"
        else:
            return "Needs Improvement"
    
    def get_improvement_suggestions(self, performance: Dict) -> List[str]:
        """Get personalized improvement suggestions"""
        suggestions = []
        
        wpm = performance['wpm']
        accuracy = performance['accuracy']
        consistency = performance['consistency_score']
        error_rate = performance['error_rate']
        
        # WPM suggestions
        if wpm < 30:
            suggestions.append("Focus on building basic typing speed with simple exercises")
        elif wpm < 50:
            suggestions.append("Practice common word patterns to increase speed")
        elif wpm < 70:
            suggestions.append("Work on touch typing without looking at keyboard")
        
        # Accuracy suggestions
        if accuracy < 85:
            suggestions.append("Slow down and focus on accuracy before speed")
            suggestions.append("Practice difficult letter combinations")
        elif accuracy < 95:
            suggestions.append("Pay attention to common mistake patterns")
        
        # Consistency suggestions
        if consistency < 70:
            suggestions.append("Work on maintaining steady rhythm while typing")
            suggestions.append("Practice with a metronome to improve consistency")
        
        # Error rate suggestions
        if error_rate > 5:
            suggestions.append("Take breaks to avoid fatigue-related errors")
            suggestions.append("Practice proofreading while typing")
        
        # Backspace usage
        if performance['backspace_count'] > performance['total_characters'] * 0.1:
            suggestions.append("Try to avoid excessive backspacing - focus on accuracy")
        
        return suggestions
    
    def _count_errors(self, typed_text: str, target_text: str) -> int:
        """Count total errors in typed text"""
        errors = 0
        comparison_length = min(len(typed_text), len(target_text))
        
        for i in range(comparison_length):
            if typed_text[i] != target_text[i]:
                errors += 1
        
        # Add errors for extra characters
        if len(typed_text) > len(target_text):
            errors += len(typed_text) - len(target_text)
        
        return errors
    
    def _count_correct_characters(self, typed_text: str, target_text: str) -> int:
        """Count correctly typed characters"""
        correct = 0
        comparison_length = min(len(typed_text), len(target_text))
        
        for i in range(comparison_length):
            if typed_text[i] == target_text[i]:
                correct += 1
        
        return correct
    
    def _count_correct_words(self, typed_words: List[str], target_words: List[str]) -> int:
        """Count correctly typed complete words"""
        correct_words = 0
        comparison_length = min(len(typed_words), len(target_words))
        
        for i in range(comparison_length):
            if typed_words[i] == target_words[i]:
                correct_words += 1
        
        return correct_words