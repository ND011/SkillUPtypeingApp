"""
Main window for SPEED application
Central hub with all features and modes
"""

import logging
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QTabWidget, QLabel, QPushButton, QFrame, QStatusBar,
                            QMenuBar, QMenu, QMessageBox, QDialog)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QAction, QIcon

from .typing_interface import TypingInterface
from .statistics_widget import StatisticsWidget
from .leaderboard_widget import LeaderboardWidget
from .settings_dialog import SettingsDialog
from .user_profile_dialog import UserProfileDialog
from .name_entry_dialog import NameEntryDialog
from .theme_manager import ThemeManager
from game.speed_engine import SpeedEngine, GameMode, DifficultyLevel
from models.user_models import UserProfile, Theme, UserLevel


class MainWindow(QMainWindow):
    """Main application window with tabbed interface"""
    
    user_changed = pyqtSignal(str)  # Emitted when user changes
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.speed_engine = SpeedEngine()
        self.theme_manager = ThemeManager()
        self.current_user = None
        
        # UI components
        self.typing_interface = None
        self.statistics_widget = None
        self.leaderboard_widget = None
        
        self.setup_ui()
        self.setup_connections()
        self.setup_status_updates()
        
        # Load default user or show profile dialog
        self.initialize_user()
        self.update_theme_button()  # Initialize theme button state
    
    def setup_ui(self):
        """Set up the main user interface"""
        self.setWindowTitle("SPEED - Keyboard Speed Training")
        self.setMinimumSize(1000, 700)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create central widget with tabs
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Create header
        header = self.create_header()
        layout.addWidget(header)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        
        # Create tabs
        self.create_tabs()
        
        layout.addWidget(self.tab_widget)
        central_widget.setLayout(layout)
        
        # Create status bar
        self.create_status_bar()
    
    def create_menu_bar(self):
        """Create the application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('&File')
        
        new_session_action = QAction('&New Session', self)
        new_session_action.setShortcut('Ctrl+N')
        new_session_action.triggered.connect(self.new_session)
        file_menu.addAction(new_session_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('E&xit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # User menu
        user_menu = menubar.addMenu('&User')
        
        profile_action = QAction('&Profile', self)
        profile_action.triggered.connect(self.show_user_profile)
        user_menu.addAction(profile_action)
        
        switch_user_action = QAction('&Switch User', self)
        switch_user_action.triggered.connect(self.switch_user)
        user_menu.addAction(switch_user_action)
        
        # Settings menu
        settings_menu = menubar.addMenu('&Settings')
        
        preferences_action = QAction('&Preferences', self)
        preferences_action.setShortcut('Ctrl+,')
        preferences_action.triggered.connect(self.show_settings)
        settings_menu.addAction(preferences_action)
        
        settings_menu.addSeparator()
        
        # Quick theme toggle
        toggle_theme_action = QAction('Toggle &Dark/Light Theme', self)
        toggle_theme_action.setShortcut('Ctrl+T')
        toggle_theme_action.triggered.connect(self.toggle_theme)
        settings_menu.addAction(toggle_theme_action)
        
        # Theme submenu
        theme_menu = settings_menu.addMenu('&Theme')
        self.create_theme_menu(theme_menu)
        
        # Help menu
        help_menu = menubar.addMenu('&Help')
        
        about_action = QAction('&About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        shortcuts_action = QAction('&Keyboard Shortcuts', self)
        shortcuts_action.setShortcut('F1')
        shortcuts_action.triggered.connect(self.show_shortcuts)
        help_menu.addAction(shortcuts_action)
    
    def create_theme_menu(self, theme_menu):
        """Create theme selection submenu"""
        available_themes = self.theme_manager.get_available_themes()
        
        for theme, name in available_themes.items():
            action = QAction(name, self)
            action.setCheckable(True)
            action.setData(theme)
            action.triggered.connect(lambda checked, t=theme: self.change_theme(t))
            theme_menu.addAction(action)
            
            # Check current theme
            if theme == self.theme_manager.get_current_theme():
                action.setChecked(True)
    
    def create_header(self):
        """Create the application header"""
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        header_frame.setMaximumHeight(80)
        
        layout = QHBoxLayout()
        
        # App title and logo
        title_layout = QVBoxLayout()
        
        title_label = QLabel("SPEED")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #0078d4;")
        
        subtitle_label = QLabel("Keyboard Speed Training")
        subtitle_font = QFont()
        subtitle_font.setPointSize(12)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet("color: #605e5c;")
        
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        
        # User info
        user_layout = QVBoxLayout()
        
        self.user_label = QLabel("Welcome!")
        user_font = QFont()
        user_font.setPointSize(14)
        user_font.setBold(True)
        self.user_label.setFont(user_font)
        
        self.user_stats_label = QLabel("Ready to practice")
        self.user_stats_label.setStyleSheet("color: #605e5c;")
        
        user_layout.addWidget(self.user_label)
        user_layout.addWidget(self.user_stats_label)
        
        # Theme toggle button
        button_layout = QHBoxLayout()
        
        self.theme_toggle_btn = QPushButton("🌙")  # Moon icon for dark mode
        self.theme_toggle_btn.setFixedSize(40, 40)
        self.theme_toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #605e5c;
                padding: 5px;
                font-size: 16pt;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #484644;
            }
        """)
        self.theme_toggle_btn.setToolTip("Toggle Dark/Light Theme")
        self.theme_toggle_btn.clicked.connect(self.toggle_theme)
        
        button_layout.addWidget(self.theme_toggle_btn)
        
        # Assemble header
        layout.addLayout(title_layout)
        layout.addStretch()
        layout.addLayout(user_layout)
        layout.addStretch()
        layout.addLayout(button_layout)
        
        header_frame.setLayout(layout)
        return header_frame
    
    def create_tabs(self):
        """Create all application tabs"""
        # Practice tab
        self.typing_interface = TypingInterface(self.speed_engine)
        self.tab_widget.addTab(self.typing_interface, "Practice")
        
        # Statistics tab
        self.statistics_widget = StatisticsWidget(self.speed_engine)
        self.tab_widget.addTab(self.statistics_widget, "Statistics")
        
        # Leaderboard tab
        self.leaderboard_widget = LeaderboardWidget(self.speed_engine)
        self.tab_widget.addTab(self.leaderboard_widget, "Leaderboard")
    
    def create_status_bar(self):
        """Create the status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Add permanent widgets to status bar
        self.session_status_label = QLabel("Ready")
        self.status_bar.addPermanentWidget(self.session_status_label)
        
        self.status_bar.showMessage("Welcome to SPEED - Select a practice mode to begin")
    
    def setup_connections(self):
        """Set up signal connections"""
        # Theme manager connections
        self.theme_manager.theme_changed.connect(self.on_theme_changed)
        
        # Speed engine connections
        self.speed_engine.register_update_callback(self.on_session_update)
        self.speed_engine.register_session_end_callback(self.on_session_end)
        
        # Tab change connections
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
    
    def setup_status_updates(self):
        """Set up periodic status updates"""
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(1000)  # Update every second
    
    def initialize_user(self):
        """Initialize user profile"""
        # For now, create a default user
        # In a full implementation, this would load from database or show login
        self.current_user = UserProfile(
            username="default_user",
            display_name="Practice User",
            skill_level=UserLevel.BEGINNER
        )
        self.update_user_display()
    
    def update_user_display(self):
        """Update user information in the header"""
        # Set static welcome message
        self.user_label.setText("Welcome to Typing Race")
        
        if self.current_user:
            if self.current_user.total_sessions > 0:
                stats_text = f"Best: {self.current_user.best_wpm:.0f} WPM | Avg: {self.current_user.average_wpm:.0f} WPM"
            else:
                stats_text = "Ready to start your first session"
            
            self.user_stats_label.setText(stats_text)
    
    def start_quick_practice(self):
        """Start a quick practice session"""
        # Show name entry dialog
        name_dialog = NameEntryDialog(self)
        if name_dialog.exec() == QDialog.DialogCode.Accepted:
            user_name = name_dialog.get_name()
            
            # Switch to practice tab and start session
            self.tab_widget.setCurrentIndex(0)
            self.typing_interface.start_session(
                user_name,
                GameMode.PRACTICE,
                DifficultyLevel.BEGINNER,  # Use beginner as default
                60  # 1 minute
            )
    

    def new_session(self):
        """Start a new typing session"""
        self.start_quick_practice()
    
    def show_user_profile(self):
        """Show user profile dialog"""
        dialog = UserProfileDialog(self.current_user, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.current_user = dialog.get_user_profile()
            self.update_user_display()
    
    def switch_user(self):
        """Switch to a different user"""
        # This would show a user selection dialog
        # For now, just show a message
        QMessageBox.information(self, "Switch User", "User switching will be implemented in a future version.")
    
    def show_settings(self):
        """Show settings dialog"""
        dialog = SettingsDialog(self.current_user, self.theme_manager, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Apply any settings changes
            pass
    
    def change_theme(self, theme: Theme):
        """Change the application theme"""
        self.theme_manager.set_theme(theme)
        self.update_theme_button()
        
        # Update theme menu checkmarks
        theme_menu = None
        for menu in self.menuBar().findChildren(QMenu):
            if menu.title() == "&Theme":
                theme_menu = menu
                break
        
        if theme_menu:
            for action in theme_menu.actions():
                action.setChecked(action.data() == theme)
    
    def toggle_theme(self):
        """Toggle between dark and light themes"""
        self.theme_manager.toggle_dark_light()
        self.update_theme_button()
    
    def update_theme_button(self):
        """Update the theme toggle button icon"""
        if self.theme_manager.is_dark_theme():
            self.theme_toggle_btn.setText("☀️")  # Sun icon for light mode
            self.theme_toggle_btn.setToolTip("Switch to Light Theme")
        else:
            self.theme_toggle_btn.setText("🌙")  # Moon icon for dark mode
            self.theme_toggle_btn.setToolTip("Switch to Dark Theme")
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About SPEED", 
                         "SPEED - Keyboard Speed Training\n\n"
                         "Version 3.0\n\n"
                         "An advanced typing practice application with multiple modes, "
                         "detailed statistics, and comprehensive progress tracking.\n\n"
                         "Features:\n"
                         "• Multiple practice modes\n"
                         "• Difficulty levels\n"
                         "• Real-time performance tracking\n"
                         "• Detailed statistics and analysis\n"
                         "• Leaderboards and achievements\n"
                         "• Customizable themes\n\n"
                         "Built with Python and PyQt6")
    
    def show_shortcuts(self):
        """Show keyboard shortcuts dialog"""
        shortcuts_text = """
        Keyboard Shortcuts:
        
        General:
        Ctrl+N - New Session
        Ctrl+T - Toggle Dark/Light Theme
        Ctrl+, - Preferences
        Ctrl+Q - Quit Application
        F1 - Show Shortcuts
        
        During Practice:
        Escape - Stop Session
        Tab - Switch Focus
        
        Theme Toggle:
        Click the 🌙/☀️ button in the header
        Or use Ctrl+T keyboard shortcut
        """
        
        QMessageBox.information(self, "Keyboard Shortcuts", shortcuts_text)
    
    def on_theme_changed(self, theme_name: str):
        """Handle theme change"""
        self.update_theme_button()
        self.status_bar.showMessage(f"Theme changed to {theme_name.replace('_', ' ').title()}", 2000)
    
    def on_session_update(self, wpm: float, accuracy: float, progress: float):
        """Handle session updates from speed engine"""
        self.session_status_label.setText(f"WPM: {wpm:.1f} | Accuracy: {accuracy:.1f}% | Progress: {progress:.1f}%")
    
    def on_session_end(self, score_record):
        """Handle session end"""
        self.session_status_label.setText("Session completed")
        self.status_bar.showMessage(f"Session completed! WPM: {score_record.wpm:.1f}, Accuracy: {score_record.accuracy:.1f}%", 5000)
        
        # Update user stats (in a real app, this would be loaded from database)
        if self.current_user:
            self.current_user.total_sessions += 1
            if score_record.wpm > self.current_user.best_wpm:
                self.current_user.best_wpm = score_record.wpm
            if score_record.accuracy > self.current_user.best_accuracy:
                self.current_user.best_accuracy = score_record.accuracy
            
            self.update_user_display()
        
        # Refresh statistics and leaderboard immediately after session ends
        if self.statistics_widget:
            self.statistics_widget.refresh_data()
        if self.leaderboard_widget:
            self.leaderboard_widget.refresh_data()
    
    def on_tab_changed(self, index: int):
        """Handle tab change"""
        tab_names = ["Practice", "Statistics", "Leaderboard"]
        if 0 <= index < len(tab_names):
            self.status_bar.showMessage(f"Switched to {tab_names[index]} tab")
            
            # Refresh data when switching to statistics or leaderboard
            if index == 1 and self.statistics_widget:
                self.statistics_widget.refresh_data()
            elif index == 2 and self.leaderboard_widget:
                self.leaderboard_widget.refresh_data()
    
    def update_status(self):
        """Update status information periodically"""
        if self.speed_engine.is_session_active():
            remaining = self.speed_engine.get_time_remaining()
            minutes = int(remaining) // 60
            seconds = int(remaining) % 60
            self.session_status_label.setText(f"Time: {minutes:02d}:{seconds:02d}")
        elif not self.speed_engine.is_session_active() and self.session_status_label.text().startswith("Time:"):
            self.session_status_label.setText("Ready")
    
    def cleanup(self):
        """Clean up resources before closing"""
        if self.speed_engine:
            self.speed_engine.cleanup()
        
        if self.status_timer:
            self.status_timer.stop()
    
    def closeEvent(self, event):
        """Handle application close event"""
        self.cleanup()
        event.accept()