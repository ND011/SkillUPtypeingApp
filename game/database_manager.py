"""
Enhanced database manager for SPEED application
Handles user scores, progress tracking, and statistics
"""

import sqlite3
import logging
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class ScoreRecord:
    """Data class for score records"""
    id: Optional[int]
    user_name: str
    wpm: float
    accuracy: float
    level: str
    mode: str
    date: datetime
    duration: int
    total_characters: int
    correct_characters: int


@dataclass
class UserStats:
    """Data class for user statistics"""
    user_name: str
    total_sessions: int
    average_wpm: float
    best_wpm: float
    average_accuracy: float
    best_accuracy: float
    total_time_practiced: int
    improvement_rate: float


class DatabaseManager:
    """Enhanced database manager with comprehensive features"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Use a path relative to the executable/script location
            import sys
            import os
            if getattr(sys, 'frozen', False):
                # Running as executable
                app_dir = os.path.dirname(sys.executable)
            else:
                # Running as script
                app_dir = os.path.dirname(os.path.abspath(__file__))
            self.db_path = os.path.join(app_dir, "speed_data.db")
        else:
            self.db_path = db_path
        self.connection = None
        self.logger = logging.getLogger(__name__)
    
    def initialize(self) -> bool:
        """Initialize database with all required tables"""
        try:
            print(f"🗄️ Database path: {self.db_path}")
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            
            self._create_tables()
            self._create_indexes()
            
            # Check if database has existing records
            cursor = self.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM scores")
            count = cursor.fetchone()[0]
            print(f"📊 Database contains {count} existing records")
            
            self.logger.info("Database initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Database initialization failed: {e}")
            return False
    
    def _create_tables(self):
        """Create all required database tables"""
        cursor = self.connection.cursor()
        
        # Scores table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL,
                wpm REAL NOT NULL,
                accuracy REAL NOT NULL,
                level TEXT NOT NULL,
                mode TEXT NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                duration INTEGER NOT NULL,
                total_characters INTEGER NOT NULL,
                correct_characters INTEGER NOT NULL
            )
        ''')
        
        # User preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                user_name TEXT PRIMARY KEY,
                theme TEXT DEFAULT 'default',
                difficulty_level TEXT DEFAULT 'beginner',
                sound_enabled BOOLEAN DEFAULT 1,
                auto_advance BOOLEAN DEFAULT 1,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Daily goals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL,
                date DATE NOT NULL,
                target_wpm REAL NOT NULL,
                target_accuracy REAL NOT NULL,
                target_sessions INTEGER NOT NULL,
                achieved_wpm REAL DEFAULT 0,
                achieved_accuracy REAL DEFAULT 0,
                completed_sessions INTEGER DEFAULT 0,
                UNIQUE(user_name, date)
            )
        ''')
        
        # Practice sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS practice_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL,
                start_time TIMESTAMP NOT NULL,
                end_time TIMESTAMP,
                total_duration INTEGER,
                rounds_completed INTEGER DEFAULT 0,
                average_wpm REAL DEFAULT 0,
                average_accuracy REAL DEFAULT 0
            )
        ''')
        
        self.connection.commit()
    
    def _create_indexes(self):
        """Create database indexes for better performance"""
        cursor = self.connection.cursor()
        
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_scores_user_date ON scores(user_name, date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_scores_wpm ON scores(wpm)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_user ON practice_sessions(user_name)')
        
        self.connection.commit()
    
    def save_score(self, score: ScoreRecord) -> bool:
        """Save a score record to the database and keep only top 10 records"""
        try:
            cursor = self.connection.cursor()
            
            # Insert the new score
            cursor.execute('''
                INSERT INTO scores (user_name, wpm, accuracy, level, mode, duration, 
                                  total_characters, correct_characters)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (score.user_name, score.wpm, score.accuracy, score.level, 
                  score.mode, score.duration, score.total_characters, score.correct_characters))
            
            # Keep top 50 records based on WPM (primary) and accuracy (secondary)
            cursor.execute('''
                DELETE FROM scores 
                WHERE id NOT IN (
                    SELECT id FROM scores 
                    ORDER BY wpm DESC, accuracy DESC 
                    LIMIT 50
                )
            ''')
            
            self.connection.commit()
            
            # Log how many records remain
            cursor.execute('SELECT COUNT(*) FROM scores')
            count = cursor.fetchone()[0]
            
            self.logger.info(f"Score saved for user {score.user_name}: {score.wpm} WPM, {score.accuracy}% accuracy")
            self.logger.info(f"Database now contains {count} records (max 50)")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save score: {e}")
            return False
    
    def get_user_scores(self, user_name: str, limit: int = 50) -> List[ScoreRecord]:
        """Get recent scores for a user"""
        try:
            if not self.connection:
                self.initialize()
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT * FROM scores 
                WHERE user_name = ? 
                ORDER BY date DESC 
                LIMIT ?
            ''', (user_name, limit))
            
            rows = cursor.fetchall()
            return [self._row_to_score_record(row) for row in rows]
            
        except Exception as e:
            self.logger.error(f"Failed to get user scores: {e}")
            return []
    
    def get_leaderboard(self, mode: str = None, limit: int = 10) -> List[ScoreRecord]:
        """Get top scores for leaderboard"""
        try:
            if not self.connection:
                self.initialize()
            cursor = self.connection.cursor()
            
            if mode:
                cursor.execute('''
                    SELECT * FROM scores 
                    WHERE mode = ? 
                    ORDER BY wpm DESC, accuracy DESC 
                    LIMIT ?
                ''', (mode, limit))
            else:
                cursor.execute('''
                    SELECT * FROM scores 
                    ORDER BY wpm DESC, accuracy DESC 
                    LIMIT ?
                ''', (limit,))
            
            rows = cursor.fetchall()
            print(f"🏆 Retrieved {len(rows)} records from database for leaderboard")
            return [self._row_to_score_record(row) for row in rows]
            
        except Exception as e:
            self.logger.error(f"Failed to get leaderboard: {e}")
            return []
    
    def get_user_stats(self, user_name: str) -> Optional[UserStats]:
        """Get comprehensive statistics for a user"""
        try:
            if not self.connection:
                self.initialize()
            cursor = self.connection.cursor()
            
            # Get basic stats
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_sessions,
                    AVG(wpm) as avg_wpm,
                    MAX(wpm) as best_wpm,
                    AVG(accuracy) as avg_accuracy,
                    MAX(accuracy) as best_accuracy,
                    SUM(duration) as total_time
                FROM scores 
                WHERE user_name = ?
            ''', (user_name,))
            
            row = cursor.fetchone()
            if not row or row['total_sessions'] == 0:
                return None
            
            # Calculate improvement rate (WPM improvement over last 10 sessions vs first 10)
            improvement_rate = self._calculate_improvement_rate(user_name)
            
            return UserStats(
                user_name=user_name,
                total_sessions=row['total_sessions'],
                average_wpm=round(row['avg_wpm'], 1),
                best_wpm=round(row['best_wpm'], 1),
                average_accuracy=round(row['avg_accuracy'], 1),
                best_accuracy=round(row['best_accuracy'], 1),
                total_time_practiced=row['total_time'] or 0,
                improvement_rate=improvement_rate
            )
            
        except Exception as e:
            self.logger.error(f"Failed to get user stats: {e}")
            return None
    
    def _calculate_improvement_rate(self, user_name: str) -> float:
        """Calculate user's improvement rate"""
        try:
            cursor = self.connection.cursor()
            
            # Get first 10 sessions average WPM
            cursor.execute('''
                SELECT AVG(wpm) as early_avg FROM (
                    SELECT wpm FROM scores 
                    WHERE user_name = ? 
                    ORDER BY date ASC 
                    LIMIT 10
                )
            ''', (user_name,))
            early_avg = cursor.fetchone()['early_avg']
            
            # Get last 10 sessions average WPM
            cursor.execute('''
                SELECT AVG(wpm) as recent_avg FROM (
                    SELECT wpm FROM scores 
                    WHERE user_name = ? 
                    ORDER BY date DESC 
                    LIMIT 10
                )
            ''', (user_name,))
            recent_avg = cursor.fetchone()['recent_avg']
            
            if early_avg and recent_avg and early_avg > 0:
                improvement = ((recent_avg - early_avg) / early_avg) * 100
                return round(improvement, 1)
            
            return 0.0
            
        except Exception as e:
            self.logger.error(f"Failed to calculate improvement rate: {e}")
            return 0.0
    
    def get_all_users(self) -> List[str]:
        """Get list of all users"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT DISTINCT user_name FROM scores ORDER BY user_name')
            return [row['user_name'] for row in cursor.fetchall()]
            
        except Exception as e:
            self.logger.error(f"Failed to get users: {e}")
            return []
    
    def _row_to_score_record(self, row) -> ScoreRecord:
        """Convert database row to ScoreRecord object"""
        return ScoreRecord(
            id=row['id'],
            user_name=row['user_name'],
            wpm=row['wpm'],
            accuracy=row['accuracy'],
            level=row['level'],
            mode=row['mode'],
            date=datetime.fromisoformat(row['date']),
            duration=row['duration'],
            total_characters=row['total_characters'],
            correct_characters=row['correct_characters']
        )
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.logger.info("Database connection closed")
    
    def __del__(self):
        """Ensure database connection is closed"""
        self.close()