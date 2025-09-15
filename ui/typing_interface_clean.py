"""
Functional typing interface for SPEED application
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QTextEdit, QPushButton, QGroupBox, QComboBox, 
                            QSpinBox, QProgressBar, QFrame, QScrollArea)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QTextCharFormat, QTextCursor, QTextDocument
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
        
        # Combined session controls and performance stats
        controls_group = self.create_combined_controls_and_stats()
        layout.addWidget(controls_group)
        
        # Typing area
        typing_group = self.create_typing_area()
        layout.addWidget(typing_group)
        
        self.setLayout(layout)
    
    def create_combined_controls_and_stats(self):
        """Create combined session controls and live performance stats"""
        group = QGroupBox("Session Settings & Live Performance")
        main_layout = QVBoxLayout()
        
        # Top row: Session controls
        controls_layout = QHBoxLayout()
        
        # Mode selection
        mode_layout = QVBoxLayout()
        mode_label = QLabel("Mode:")
        mode_label.setStyleSheet("font-size: 10pt; color: #666;")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            "Timed Challenge", "Accuracy Focus", 
            "Speed Burst", "Endurance"
        ])
        self.mode_combo.setStyleSheet("font-size: 10pt; padding: 4px;")
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.mode_combo)
        
        # Difficulty selection
        difficulty_layout = QVBoxLayout()
        difficulty_label = QLabel("Difficulty:")
        difficulty_label.setStyleSheet("font-size: 10pt; color: #666;")
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Beginner", "Intermediate", "Advanced", "Expert"])
        self.difficulty_combo.setStyleSheet("font-size: 10pt; padding: 4px;")
        difficulty_layout.addWidget(difficulty_label)
        difficulty_layout.addWidget(self.difficulty_combo)
        
        # Time-based selection
        time_layout = QVBoxLayout()
        time_label = QLabel("Duration:")
        time_label.setStyleSheet("font-size: 10pt; color: #666;")
        self.time_combo = QComboBox()
        self.time_combo.addItems(["1 min (70 words)", "2 min (140 words)", "3 min (210 words)", 
                                 "5 min (350 words)", "7 min (490 words)", "10 min (700 words)"])
        self.time_combo.setCurrentIndex(0)  # Default to 1 minute
        self.time_combo.setStyleSheet("font-size: 10pt; padding: 4px;")
        time_layout.addWidget(time_label)
        time_layout.addWidget(self.time_combo)
        
        # Control buttons
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #107c10;
                color: white;
                padding: 8px 16px;
                font-size: 11pt;
                font-weight: bold;
                border-radius: 4px;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: #0e6e0e;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.start_button.clicked.connect(self.start_session_clicked)
        
        self.stop_button = QPushButton("Stop")
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #d13438;
                color: white;
                padding: 8px 16px;
                font-size: 11pt;
                font-weight: bold;
                border-radius: 4px;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: #b92b2f;
            }
        """)
        self.stop_button.clicked.connect(self.stop_session_clicked)
        self.stop_button.setEnabled(False)
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        
        # Add controls to top row
        controls_layout.addLayout(mode_layout)
        controls_layout.addLayout(difficulty_layout)
        controls_layout.addLayout(time_layout)
        controls_layout.addStretch()
        controls_layout.addLayout(button_layout)
        
        # Bottom row: Live performance stats
        stats_layout = QHBoxLayout()
        
        # Timer display
        timer_layout = QVBoxLayout()
        timer_label = QLabel("Time")
        timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timer_label.setStyleSheet("font-size: 9pt; color: #666; margin-bottom: 2px;")
        self.timer_display = QLabel("00:00")
        timer_font = QFont()
        timer_font.setPointSize(14)
        timer_font.setBold(True)
        self.timer_display.setFont(timer_font)
        self.timer_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_display.setStyleSheet("color: #d13438; padding: 4px;")
        timer_layout.addWidget(timer_label)
        timer_layout.addWidget(self.timer_display)
        
        # WPM display
        wpm_layout = QVBoxLayout()
        wpm_label = QLabel("WPM")
        wpm_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        wpm_label.setStyleSheet("font-size: 9pt; color: #666; margin-bottom: 2px;")
        self.wpm_display = QLabel("0.0")
        wpm_font = QFont()
        wpm_font.setPointSize(14)
        wpm_font.setBold(True)
        self.wpm_display.setFont(wpm_font)
        self.wpm_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.wpm_display.setStyleSheet("color: #0078d4; padding: 4px;")
        wpm_layout.addWidget(wpm_label)
        wpm_layout.addWidget(self.wpm_display)
        
        # Accuracy display
        accuracy_layout = QVBoxLayout()
        accuracy_label = QLabel("Accuracy")
        accuracy_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        accuracy_label.setStyleSheet("font-size: 9pt; color: #666; margin-bottom: 2px;")
        self.accuracy_display = QLabel("0.0%")
        accuracy_font = QFont()
        accuracy_font.setPointSize(14)
        accuracy_font.setBold(True)
        self.accuracy_display.setFont(accuracy_font)
        self.accuracy_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.accuracy_display.setStyleSheet("color: #107c10; padding: 4px;")
        accuracy_layout.addWidget(accuracy_label)
        accuracy_layout.addWidget(self.accuracy_display)
        
        # Progress bar
        progress_layout = QVBoxLayout()
        progress_label = QLabel("Progress")
        progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        progress_label.setStyleSheet("font-size: 9pt; color: #666; margin-bottom: 2px;")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setMaximumHeight(20)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #d1d1d1;
                border-radius: 3px;
                text-align: center;
                font-size: 9pt;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #0078d4;
                border-radius: 2px;
            }
        """)
        progress_layout.addWidget(progress_label)
        progress_layout.addWidget(self.progress_bar)
        
        # Add stats to bottom row
        stats_layout.addLayout(timer_layout)
        stats_layout.addLayout(wpm_layout)
        stats_layout.addLayout(accuracy_layout)
        stats_layout.addLayout(progress_layout, 2)  # Give progress bar more space
        
        # Add both rows to main layout
        main_layout.addLayout(controls_layout)
        main_layout.addLayout(stats_layout)
        
        group.setLayout(main_layout)
        return group