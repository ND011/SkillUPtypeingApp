"""
Settings dialog for SPEED application
"""

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

class SettingsDialog(QDialog):
    """Settings configuration dialog"""
    
    def __init__(self, user_profile, theme_manager, parent=None):
        super().__init__(parent)
        self.user_profile = user_profile
        self.theme_manager = theme_manager
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the settings dialog"""
        self.setWindowTitle("Settings")
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        
        label = QLabel("Settings Dialog - Coming Soon!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        
        # OK button
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)
        
        self.setLayout(layout)