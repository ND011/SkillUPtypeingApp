"""
User profile dialog for SPEED application
"""

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

class UserProfileDialog(QDialog):
    """User profile management dialog"""
    
    def __init__(self, user_profile, parent=None):
        super().__init__(parent)
        self.user_profile = user_profile
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user profile dialog"""
        self.setWindowTitle("User Profile")
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        
        label = QLabel("User Profile Dialog - Coming Soon!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        
        # OK button
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)
        
        self.setLayout(layout)
    
    def get_user_profile(self):
        """Get the updated user profile"""
        return self.user_profile