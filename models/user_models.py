"""
User-related data models for SPEED application
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum


class UserLevel(Enum):
    """User skill levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class Theme(Enum):
    """Available themes"""
    DEFAULT = "default"
    DARK = "dark"
    HIGH_CONTRAST = "high_contrast"
    BLUE = "blue"
    GREEN = "green"


@dataclass
class UserProfile:
    """Complete user profile with preferences and statistics"""
    username: str
    display_name: str
    skill_level: UserLevel
    theme: Theme = Theme.DEFAULT
    created_date: datetime = field(default_factory=datetime.now)
    last_active: datetime = field(default_factory=datetime.now)
    
    # Preferences
    sound_enabled: bool = True
    auto_advance: bool = True
    show_wpm_live: bool = True
    show_accuracy_live: bool = True
    preferred_session_duration: int = 60  # seconds
    
    # Statistics (calculated from database)
    total_sessions: int = 0
    total_time_practiced: int = 0  # seconds
    average_wpm: float = 0.0
    best_wpm: float = 0.0
    average_accuracy: float = 0.0
    best_accuracy: float = 0.0
    improvement_rate: float = 0.0  # percentage
    
    # Achievements
    achievements: List[str] = field(default_factory=list)
    current_streak: int = 0  # consecutive days practiced
    longest_streak: int = 0
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for storage"""
        return {
            'username': self.username,
            'display_name': self.display_name,
            'skill_level': self.skill_level.value,
            'theme': self.theme.value,
            'created_date': self.created_date.isoformat(),
            'last_active': self.last_active.isoformat(),
            'sound_enabled': self.sound_enabled,
            'auto_advance': self.auto_advance,
            'show_wpm_live': self.show_wpm_live,
            'show_accuracy_live': self.show_accuracy_live,
            'preferred_session_duration': self.preferred_session_duration,
            'total_sessions': self.total_sessions,
            'total_time_practiced': self.total_time_practiced,
            'average_wpm': self.average_wpm,
            'best_wpm': self.best_wpm,
            'average_accuracy': self.average_accuracy,
            'best_accuracy': self.best_accuracy,
            'improvement_rate': self.improvement_rate,
            'achievements': self.achievements,
            'current_streak': self.current_streak,
            'longest_streak': self.longest_streak
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'UserProfile':
        """Create from dictionary"""
        return cls(
            username=data['username'],
            display_name=data['display_name'],
            skill_level=UserLevel(data['skill_level']),
            theme=Theme(data.get('theme', 'default')),
            created_date=datetime.fromisoformat(data['created_date']),
            last_active=datetime.fromisoformat(data['last_active']),
            sound_enabled=data.get('sound_enabled', True),
            auto_advance=data.get('auto_advance', True),
            show_wpm_live=data.get('show_wpm_live', True),
            show_accuracy_live=data.get('show_accuracy_live', True),
            preferred_session_duration=data.get('preferred_session_duration', 60),
            total_sessions=data.get('total_sessions', 0),
            total_time_practiced=data.get('total_time_practiced', 0),
            average_wpm=data.get('average_wpm', 0.0),
            best_wpm=data.get('best_wpm', 0.0),
            average_accuracy=data.get('average_accuracy', 0.0),
            best_accuracy=data.get('best_accuracy', 0.0),
            improvement_rate=data.get('improvement_rate', 0.0),
            achievements=data.get('achievements', []),
            current_streak=data.get('current_streak', 0),
            longest_streak=data.get('longest_streak', 0)
        )


@dataclass
class DailyGoal:
    """Daily practice goals for users"""
    user_name: str
    date: datetime
    target_wpm: float
    target_accuracy: float
    target_sessions: int
    target_time: int  # minutes
    
    # Progress tracking
    achieved_wpm: float = 0.0
    achieved_accuracy: float = 0.0
    completed_sessions: int = 0
    completed_time: int = 0  # minutes
    
    @property
    def is_completed(self) -> bool:
        """Check if all goals are met"""
        return (self.achieved_wpm >= self.target_wpm and
                self.achieved_accuracy >= self.target_accuracy and
                self.completed_sessions >= self.target_sessions and
                self.completed_time >= self.target_time)
    
    @property
    def completion_percentage(self) -> float:
        """Get overall completion percentage"""
        wpm_progress = min(100, (self.achieved_wpm / max(1, self.target_wpm)) * 100)
        accuracy_progress = min(100, (self.achieved_accuracy / max(1, self.target_accuracy)) * 100)
        session_progress = min(100, (self.completed_sessions / max(1, self.target_sessions)) * 100)
        time_progress = min(100, (self.completed_time / max(1, self.target_time)) * 100)
        
        return (wpm_progress + accuracy_progress + session_progress + time_progress) / 4


@dataclass
class Achievement:
    """User achievement definition"""
    id: str
    name: str
    description: str
    icon: str
    category: str  # speed, accuracy, consistency, milestone, etc.
    requirement: Dict  # Flexible requirement definition
    points: int = 10
    is_hidden: bool = False  # Hidden until unlocked
    
    def check_requirement(self, user_stats: Dict) -> bool:
        """Check if user meets achievement requirement"""
        # This would contain logic to check various achievement types
        # For now, return False as placeholder
        return False


# Predefined achievements
ACHIEVEMENTS = [
    Achievement(
        id="first_session",
        name="Getting Started",
        description="Complete your first typing session",
        icon="🎯",
        category="milestone",
        requirement={"sessions": 1},
        points=5
    ),
    Achievement(
        id="speed_demon_50",
        name="Speed Demon",
        description="Achieve 50 WPM in a session",
        icon="⚡",
        category="speed",
        requirement={"wpm": 50},
        points=15
    ),
    Achievement(
        id="accuracy_master_95",
        name="Accuracy Master",
        description="Achieve 95% accuracy in a session",
        icon="🎯",
        category="accuracy",
        requirement={"accuracy": 95},
        points=15
    ),
    Achievement(
        id="consistent_performer",
        name="Consistent Performer",
        description="Maintain 90%+ consistency score",
        icon="📊",
        category="consistency",
        requirement={"consistency": 90},
        points=20
    ),
    Achievement(
        id="daily_practice_7",
        name="Week Warrior",
        description="Practice for 7 consecutive days",
        icon="🔥",
        category="streak",
        requirement={"streak": 7},
        points=25
    ),
    Achievement(
        id="speed_demon_100",
        name="Century Club",
        description="Achieve 100 WPM in a session",
        icon="💯",
        category="speed",
        requirement={"wpm": 100},
        points=50
    ),
    Achievement(
        id="perfectionist",
        name="Perfectionist",
        description="Achieve 100% accuracy in a session",
        icon="✨",
        category="accuracy",
        requirement={"accuracy": 100},
        points=30
    ),
    Achievement(
        id="marathon_runner",
        name="Marathon Runner",
        description="Complete a 10-minute endurance session",
        icon="🏃",
        category="endurance",
        requirement={"duration": 600},
        points=20
    ),
    Achievement(
        id="improvement_champion",
        name="Improvement Champion",
        description="Improve WPM by 20+ points from first session",
        icon="📈",
        category="improvement",
        requirement={"improvement": 20},
        points=35
    ),
    Achievement(
        id="night_owl",
        name="Night Owl",
        description="Complete a session after 10 PM",
        icon="🦉",
        category="fun",
        requirement={"time_after": "22:00"},
        points=10
    )
]