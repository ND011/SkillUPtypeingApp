"""
Functional leaderboard widget for SPEED application
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QTableWidget, QTableWidgetItem, QGroupBox, 
                            QPushButton, QComboBox, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class LeaderboardWidget(QWidget):
    """Functional leaderboard display widget"""
    
    def __init__(self, speed_engine):
        super().__init__()
        self.speed_engine = speed_engine
        self.setup_ui()
        self.refresh_data()
    
    def setup_ui(self):
        """Set up the leaderboard interface"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header with controls
        header = self.create_header()
        layout.addWidget(header)
        
        # Leaderboard table
        leaderboard_group = self.create_leaderboard_table()
        layout.addWidget(leaderboard_group)
        
        # Refresh button
        refresh_button = QPushButton("Refresh Leaderboard")
        refresh_button.clicked.connect(self.refresh_data)
        layout.addWidget(refresh_button)
        
        self.setLayout(layout)
    
    def create_header(self):
        """Create leaderboard header with filter controls"""
        header_frame = QFrame()
        layout = QHBoxLayout()
        
        # Title
        title_label = QLabel("Leaderboard")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #0078d4;")
        
        # Mode filter
        mode_layout = QVBoxLayout()
        mode_label = QLabel("Filter by Mode:")
        self.mode_filter = QComboBox()
        self.mode_filter.addItems([
            "All Modes", "Practice", "Timed Challenge", "Accuracy Focus", 
            "Speed Burst", "Endurance"
        ])
        self.mode_filter.currentTextChanged.connect(self.refresh_data)
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.mode_filter)
        
        layout.addWidget(title_label)
        layout.addStretch()
        layout.addLayout(mode_layout)
        
        header_frame.setLayout(layout)
        return header_frame
    
    def create_leaderboard_table(self):
        """Create leaderboard table"""
        group = QGroupBox("Top Performers")
        layout = QVBoxLayout()
        
        # Create table
        self.leaderboard_table = QTableWidget()
        self.leaderboard_table.setColumnCount(6)
        self.leaderboard_table.setHorizontalHeaderLabels([
            "Rank", "User", "WPM", "Accuracy", "Mode", "Level"
        ])
        
        # Set table properties
        self.leaderboard_table.setAlternatingRowColors(True)
        self.leaderboard_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.leaderboard_table.horizontalHeader().setStretchLastSection(True)
        
        layout.addWidget(self.leaderboard_table)
        group.setLayout(layout)
        return group
    
    def refresh_data(self):
        """Refresh leaderboard data"""
        # Get filter mode
        selected_mode = self.mode_filter.currentText()
        mode_filter = None if selected_mode == "All Modes" else selected_mode.lower().replace(" ", "_")
        
        # Get leaderboard data
        leaderboard_data = self.speed_engine.db_manager.get_leaderboard(mode_filter, 50)
        
        # Update table
        self.leaderboard_table.setRowCount(len(leaderboard_data))
        
        for row, score in enumerate(leaderboard_data):
            # Rank
            rank_item = QTableWidgetItem(str(row + 1))
            rank_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if row == 0:
                rank_item.setBackground(Qt.GlobalColor.yellow)  # Gold
            elif row == 1:
                rank_item.setBackground(Qt.GlobalColor.lightGray)  # Silver
            elif row == 2:
                rank_item.setBackground(Qt.GlobalColor.darkYellow)  # Bronze
            self.leaderboard_table.setItem(row, 0, rank_item)
            
            # User
            user_item = QTableWidgetItem(score.user_name)
            self.leaderboard_table.setItem(row, 1, user_item)
            
            # WPM
            wpm_item = QTableWidgetItem(f"{score.wpm:.1f}")
            wpm_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.leaderboard_table.setItem(row, 2, wpm_item)
            
            # Accuracy
            accuracy_item = QTableWidgetItem(f"{score.accuracy:.1f}%")
            accuracy_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.leaderboard_table.setItem(row, 3, accuracy_item)
            
            # Mode
            mode_item = QTableWidgetItem(score.mode.replace("_", " ").title())
            self.leaderboard_table.setItem(row, 4, mode_item)
            
            # Level
            level_item = QTableWidgetItem(score.level.title())
            self.leaderboard_table.setItem(row, 5, level_item)

        
        # Resize columns to content
        self.leaderboard_table.resizeColumnsToContents()
        
        # Show message if no data
        if len(leaderboard_data) == 0:
            self.leaderboard_table.setRowCount(1)
            no_data_item = QTableWidgetItem("No scores available yet. Complete some typing sessions to see rankings!")
            no_data_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.leaderboard_table.setItem(0, 0, no_data_item)
            self.leaderboard_table.setSpan(0, 0, 1, 6)  # Span across all columns