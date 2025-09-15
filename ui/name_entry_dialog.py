"""
Name entry dialog for SPEED application
Allows users to enter their name before starting typing sessions
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QFrame)
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtGui import QFont


class NameEntryDialog(QDialog):
    """Dialog for entering user name before starting typing sessions"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings("SPEED", "TypingApp")
        self.entered_name = ""
        self.setup_ui()
        self.load_last_name()
    
    def setup_ui(self):
        """Set up the dialog user interface"""
        self.setWindowTitle("Enter Your Name")
        self.setModal(True)
        self.setFixedSize(350, 200)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("Enter Your Name")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #0078d4; margin-bottom: 10px;")
        layout.addWidget(title_label)
        
        # Instruction
        instruction_label = QLabel("Please enter your name to track your typing progress:")
        instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instruction_label.setStyleSheet("color: #605e5c; margin-bottom: 10px;")
        layout.addWidget(instruction_label)
        
        # Name input
        input_layout = QHBoxLayout()
        name_label = QLabel("Name:")
        name_label.setMinimumWidth(50)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name here...")
        self.name_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                font-size: 12pt;
                border: 2px solid #d1d1d1;
                border-radius: 4px;
            }
            QLineEdit:focus {
                border-color: #0078d4;
            }
        """)
        self.name_input.returnPressed.connect(self.accept_name)
        
        input_layout.addWidget(name_label)
        input_layout.addWidget(self.name_input)
        layout.addLayout(input_layout)
        
        # Error message area
        self.error_label = QLabel("")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setStyleSheet("color: #d13438; font-weight: bold;")
        self.error_label.setMinimumHeight(20)
        layout.addWidget(self.error_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #f3f2f1;
                border: 1px solid #d1d1d1;
                padding: 8px 20px;
                font-size: 11pt;
                border-radius: 4px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #e1dfdd;
            }
        """)
        self.cancel_button.clicked.connect(self.reject)
        
        self.ok_button = QPushButton("OK")
        self.ok_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 8px 20px;
                font-size: 11pt;
                border-radius: 4px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
        """)
        self.ok_button.clicked.connect(self.accept_name)
        self.ok_button.setDefault(True)
        
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.ok_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Focus on name input
        self.name_input.setFocus()
    
    def load_last_name(self):
        """Load the last entered name from settings"""
        last_name = self.settings.value("user/last_name", "")
        if last_name:
            self.name_input.setText(last_name)
            self.name_input.selectAll()  # Select all text for easy replacement
    
    def validate_name(self, name: str) -> tuple[bool, str]:
        """Validate the entered name"""
        # Trim whitespace
        name = name.strip()
        
        # Check if empty
        if not name:
            return False, "Please enter your name"
        
        # Check length
        if len(name) > 50:
            return False, "Name must be 50 characters or less"
        
        # Name is valid
        return True, ""
    
    def accept_name(self):
        """Handle OK button click or Enter key press"""
        name = self.name_input.text()
        is_valid, error_message = self.validate_name(name)
        
        if is_valid:
            # Clear any previous error
            self.error_label.setText("")
            
            # Store the validated name
            self.entered_name = name.strip()
            
            # Save to settings for next time
            self.settings.setValue("user/last_name", self.entered_name)
            
            # Accept the dialog
            self.accept()
        else:
            # Show error message
            self.error_label.setText(error_message)
            self.name_input.setFocus()
            self.name_input.selectAll()
    
    def get_name(self) -> str:
        """Get the entered and validated name"""
        return self.entered_name
    
    def keyPressEvent(self, event):
        """Handle key press events"""
        if event.key() == Qt.Key.Key_Escape:
            self.reject()
        else:
            super().keyPressEvent(event)