"""
Functional typing interface for SPEED application
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QTextEdit, QPushButton, QGroupBox, QComboBox, 
                            QSpinBox, QProgressBar, QFrame)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QTextCharFormat, QTextCursor
from game.speed_engine import GameMode, DifficultyLevel
import time


class TypingInterface(QWidget):
    """Functional typing practice interface"""
    
    session_started = pyqtSignal()
    session_ended = pyqtSignal(object)  # Emits score record
    
    def __init__(self, speed_engine):
        super().__init__()
        self.speed_engine = speed_engine
        self.current_session = None
        self.start_time = None
        self.setup_ui()
        self.setup_connections()
        
        # Update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_display)
        self.update_timer.start(100)  # Update every 100ms
    
    def setup_ui(self):
        """Set up the typing interface"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Session controls
        controls_group = self.create_session_controls()
        layout.addWidget(controls_group)
        
        # Performance stats
        stats_group = self.create_performance_stats()
        layout.addWidget(stats_group)
        
        # Typing area
        typing_group = self.create_typing_area()
        layout.addWidget(typing_group)
        
        self.setLayout(layout)
    
    def create_session_controls(self):
        """Create session control panel"""
        group = QGroupBox("Session Settings")
        layout = QHBoxLayout()
        
        # Mode selection
        mode_layout = QVBoxLayout()
        mode_label = QLabel("Mode:")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            "Timed Challenge", "Accuracy Focus", 
            "Speed Burst", "Endurance"
        ])
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.mode_combo)
        
        # Difficulty selection
        difficulty_layout = QVBoxLayout()
        difficulty_label = QLabel("Difficulty:")
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Beginner", "Intermediate", "Advanced", "Expert"])
        difficulty_layout.addWidget(difficulty_label)
        difficulty_layout.addWidget(self.difficulty_combo)
        
        # Time-based selection
        time_layout = QVBoxLayout()
        time_label = QLabel("Time Selection:")
        self.time_combo = QComboBox()
        self.time_combo.addItems(["1 min (70 words)", "2 min (140 words)", "3 min (210 words)", 
                                 "5 min (350 words)", "7 min (490 words)", "10 min (700 words)"])
        self.time_combo.setCurrentIndex(0)  # Default to 1 minute
        time_layout.addWidget(time_label)
        time_layout.addWidget(self.time_combo)
        
        # Control buttons
        button_layout = QVBoxLayout()
        self.start_button = QPushButton("Start Session")
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #107c10;
                color: white;
                padding: 10px 20px;
                font-size: 12pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0e6e0e;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.start_button.clicked.connect(self.start_session_clicked)
        
        self.stop_button = QPushButton("Stop Session")
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #d13438;
                color: white;
                padding: 10px 20px;
                font-size: 12pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b92b2f;
            }
        """)
        self.stop_button.clicked.connect(self.stop_session_clicked)
        self.stop_button.setEnabled(False)
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        
        # Assemble layout
        layout.addLayout(mode_layout)
        layout.addLayout(difficulty_layout)
        layout.addLayout(time_layout)
        layout.addStretch()
        layout.addLayout(button_layout)
        
        group.setLayout(layout)
        return group
    
    def create_performance_stats(self):
        """Create performance statistics display"""
        group = QGroupBox("Live Performance")
        layout = QHBoxLayout()
        
        # Timer display
        timer_layout = QVBoxLayout()
        timer_label = QLabel("Time Remaining")
        timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_display = QLabel("00:00")
        timer_font = QFont()
        timer_font.setPointSize(18)
        timer_font.setBold(True)
        self.timer_display.setFont(timer_font)
        self.timer_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_display.setStyleSheet("color: #d13438; padding: 10px;")
        timer_layout.addWidget(timer_label)
        timer_layout.addWidget(self.timer_display)
        
        # WPM display
        wpm_layout = QVBoxLayout()
        wpm_label = QLabel("Words Per Minute")
        wpm_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.wpm_display = QLabel("0.0")
        wpm_font = QFont()
        wpm_font.setPointSize(18)
        wpm_font.setBold(True)
        self.wpm_display.setFont(wpm_font)
        self.wmp_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.wmp_display.setStyleSheet("color: #0078d4; padding: 10px;")
        wmp_layout.addWidget(wmp_label)
        wmp_layout.addWidget(self.wmp_display)
        
        # Accuracy display
        accuracy_layout = QVBoxLayout()
        accuracy_label = QLabel("Accuracy")
        accuracy_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.accuracy_display = QLabel("0.0%")
        accuracy_font = QFont()
        accuracy_font.setPointSize(18)
        accuracy_font.setBold(True)
        self.accuracy_display.setFont(accuracy_font)
        self.accuracy_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.accuracy_display.setStyleSheet("color: #107c10; padding: 10px;")
        accuracy_layout.addWidget(accuracy_label)
        accuracy_layout.addWidget(self.accuracy_display)
        
        # Progress bar
        progress_layout = QVBoxLayout()
        progress_label = QLabel("Progress")
        progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        progress_layout.addWidget(progress_label)
        progress_layout.addWidget(self.progress_bar)
        
        layout.addLayout(timer_layout)
        layout.addLayout(wmp_layout)
        layout.addLayout(accuracy_layout)
        layout.addLayout(progress_layout)
        
        group.setLayout(layout)
        return group