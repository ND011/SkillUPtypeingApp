"""
Functional statistics widget for SPEED application
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QTableWidget, QTableWidgetItem, QGroupBox, 
                            QPushButton, QFrame)
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtGui import QFont


class StatisticsWidget(QWidget):
    """Functional statistics display widget"""
    
    def __init__(self, speed_engine):
        super().__init__()
        self.speed_engine = speed_engine
        self.settings = QSettings("SPEED", "TypingApp")
        
        # Store references to overview stat labels for refreshing
        self.sessions_value_label = None
        self.avg_wpm_value_label = None
        self.best_wpm_value_label = None
        self.avg_acc_value_label = None
        self.time_value_label = None
        self.no_data_label = None
        
        self.setup_ui()
        self.refresh_data()
    
    def setup_ui(self):
        """Set up the statistics interface"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Overview stats
        overview_group = self.create_overview_stats()
        layout.addWidget(overview_group)
        
        # Recent sessions table
        sessions_group = self.create_sessions_table()
        layout.addWidget(sessions_group)
        
        # Refresh button
        refresh_button = QPushButton("Refresh Statistics")
        refresh_button.clicked.connect(self.refresh_data)
        layout.addWidget(refresh_button)
        
        self.setLayout(layout)
    
    def get_current_user_name(self):
        """Get the current user name from settings"""
        return self.settings.value("user/last_name", "Guest")
    
    def create_header(self):
        """Create statistics header"""
        header_frame = QFrame()
        layout = QHBoxLayout()
        
        title_label = QLabel("Performance Statistics")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #0078d4;")
        
        layout.addWidget(title_label)
        layout.addStretch()
        
        header_frame.setLayout(layout)
        return header_frame
    
    def create_overview_stats(self):
        """Create overview statistics display"""
        group = QGroupBox("Session Overview")
        layout = QHBoxLayout()
        
        # Get user statistics
        current_user = self.get_current_user_name()
        user_stats = self.speed_engine.db_manager.get_user_stats(current_user)
        
        if user_stats:
            # Total sessions
            sessions_layout = QVBoxLayout()
            sessions_title = QLabel("Total Sessions")
            sessions_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.sessions_value_label = QLabel(str(user_stats.total_sessions))
            self.sessions_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.sessions_value_label.setStyleSheet("font-size: 18pt; font-weight: bold; color: #0078d4;")
            sessions_layout.addWidget(sessions_title)
            sessions_layout.addWidget(self.sessions_value_label)
            
            # Average WPM
            avg_wpm_layout = QVBoxLayout()
            avg_wpm_title = QLabel("Average WPM")
            avg_wpm_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.avg_wpm_value_label = QLabel(f"{user_stats.average_wpm:.1f}")
            self.avg_wpm_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.avg_wpm_value_label.setStyleSheet("font-size: 18pt; font-weight: bold; color: #107c10;")
            avg_wpm_layout.addWidget(avg_wpm_title)
            avg_wpm_layout.addWidget(self.avg_wpm_value_label)
            
            # Best WPM
            best_wpm_layout = QVBoxLayout()
            best_wpm_title = QLabel("Best WPM")
            best_wpm_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.best_wpm_value_label = QLabel(f"{user_stats.best_wpm:.1f}")
            self.best_wpm_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.best_wpm_value_label.setStyleSheet("font-size: 18pt; font-weight: bold; color: #ff8c00;")
            best_wpm_layout.addWidget(best_wpm_title)
            best_wpm_layout.addWidget(self.best_wpm_value_label)
            
            # Average Accuracy
            avg_acc_layout = QVBoxLayout()
            avg_acc_title = QLabel("Average Accuracy")
            avg_acc_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.avg_acc_value_label = QLabel(f"{user_stats.average_accuracy:.1f}%")
            self.avg_acc_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.avg_acc_value_label.setStyleSheet("font-size: 18pt; font-weight: bold; color: #d13438;")
            avg_acc_layout.addWidget(avg_acc_title)
            avg_acc_layout.addWidget(self.avg_acc_value_label)
            
            # Total practice time
            time_layout = QVBoxLayout()
            time_title = QLabel("Total Practice Time")
            time_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            total_minutes = user_stats.total_time_practiced // 60
            self.time_value_label = QLabel(f"{total_minutes} min")
            self.time_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.time_value_label.setStyleSheet("font-size: 18pt; font-weight: bold; color: #605e5c;")
            time_layout.addWidget(time_title)
            time_layout.addWidget(self.time_value_label)
            
            layout.addLayout(sessions_layout)
            layout.addLayout(avg_wpm_layout)
            layout.addLayout(best_wpm_layout)
            layout.addLayout(avg_acc_layout)
            layout.addLayout(time_layout)
        else:
            # No data available
            self.no_data_label = QLabel("No statistics available yet.\nComplete some typing sessions to see your progress!")
            self.no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.no_data_label.setStyleSheet("font-size: 14pt; color: #605e5c; padding: 20px;")
            layout.addWidget(self.no_data_label)
        
        group.setLayout(layout)
        return group
    
    def create_sessions_table(self):
        """Create recent sessions table"""
        group = QGroupBox("Recent Sessions")
        layout = QVBoxLayout()
        
        # Create table
        self.sessions_table = QTableWidget()
        self.sessions_table.setColumnCount(6)
        self.sessions_table.setHorizontalHeaderLabels([
            "Date", "Mode", "Level", "WPM", "Accuracy", "Duration"
        ])
        
        # Set table properties
        self.sessions_table.setAlternatingRowColors(True)
        self.sessions_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.sessions_table.horizontalHeader().setStretchLastSection(True)
        
        layout.addWidget(self.sessions_table)
        group.setLayout(layout)
        return group
    
    def refresh_data(self):
        """Refresh statistics data"""
        current_user = self.get_current_user_name()
        
        # Refresh overview statistics
        user_stats = self.speed_engine.db_manager.get_user_stats(current_user)
        if user_stats and self.sessions_value_label:
            # Update overview stat labels
            self.sessions_value_label.setText(str(user_stats.total_sessions))
            self.avg_wpm_value_label.setText(f"{user_stats.average_wpm:.1f}")
            self.best_wpm_value_label.setText(f"{user_stats.best_wpm:.1f}")
            self.avg_acc_value_label.setText(f"{user_stats.average_accuracy:.1f}%")
            total_minutes = user_stats.total_time_practiced // 60
            self.time_value_label.setText(f"{total_minutes} min")
        
        # Get recent scores
        recent_scores = self.speed_engine.db_manager.get_user_scores(current_user, 20)
        
        # Update table
        self.sessions_table.setRowCount(len(recent_scores))
        
        for row, score in enumerate(recent_scores):
            # Date
            date_item = QTableWidgetItem(score.date.strftime("%Y-%m-%d %H:%M"))
            self.sessions_table.setItem(row, 0, date_item)
            
            # Mode
            mode_item = QTableWidgetItem(score.mode.title())
            self.sessions_table.setItem(row, 1, mode_item)
            
            # Level
            level_item = QTableWidgetItem(score.level.title())
            self.sessions_table.setItem(row, 2, level_item)
            
            # WPM
            wpm_item = QTableWidgetItem(f"{score.wpm:.1f}")
            self.sessions_table.setItem(row, 3, wpm_item)
            
            # Accuracy
            accuracy_item = QTableWidgetItem(f"{score.accuracy:.1f}%")
            self.sessions_table.setItem(row, 4, accuracy_item)
            
            # Duration
            duration_item = QTableWidgetItem(f"{score.duration}s")
            self.sessions_table.setItem(row, 5, duration_item)
        
        # Resize columns to content
        self.sessions_table.resizeColumnsToContents()
        
        # Note: In a more sophisticated implementation, we'd update the existing widgets
        # instead of recreating the entire UI