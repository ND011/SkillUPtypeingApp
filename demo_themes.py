#!/usr/bin/env python3
"""
Demo script to showcase SPEED theme system
"""

import sys
import time
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer
from ui.theme_manager import ThemeManager
from models.user_models import Theme

def demo_themes():
    """Demonstrate theme switching"""
    app = QApplication(sys.argv)
    
    # Create theme manager
    theme_manager = ThemeManager()
    
    # Show info about available themes
    available_themes = theme_manager.get_available_themes()
    theme_list = "\n".join([f"- {name}" for name in available_themes.values()])
    
    QMessageBox.information(None, "SPEED Theme Demo", 
                           f"Available Themes:\n\n{theme_list}\n\n"
                           "This demo will cycle through all themes.\n"
                           "Click OK to start.")
    
    # Create a simple window to show theme changes
    from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
    
    demo_window = QWidget()
    demo_window.setWindowTitle("SPEED Theme Demo")
    demo_window.setFixedSize(400, 300)
    
    layout = QVBoxLayout()
    
    title_label = QLabel("SPEED Theme Demonstration")
    title_label.setStyleSheet("font-size: 18pt; font-weight: bold; padding: 20px;")
    
    current_theme_label = QLabel("Current Theme: Default")
    current_theme_label.setStyleSheet("font-size: 14pt; padding: 10px;")
    
    info_label = QLabel("Watch how the interface changes with different themes!")
    info_label.setStyleSheet("font-size: 12pt; padding: 10px;")
    
    toggle_button = QPushButton("Toggle Dark/Light Theme")
    toggle_button.clicked.connect(theme_manager.toggle_dark_light)
    
    layout.addWidget(title_label)
    layout.addWidget(current_theme_label)
    layout.addWidget(info_label)
    layout.addWidget(toggle_button)
    
    demo_window.setLayout(layout)
    
    # Update theme display
    def update_theme_display():
        current_theme = theme_manager.get_current_theme()
        theme_name = theme_manager.get_theme_colors()['name']
        current_theme_label.setText(f"Current Theme: {theme_name}")
    
    theme_manager.theme_changed.connect(lambda: update_theme_display())
    
    # Auto-cycle through themes
    themes_to_demo = [Theme.DEFAULT, Theme.DARK, Theme.HIGH_CONTRAST, Theme.BLUE, Theme.GREEN]
    current_theme_index = 0
    
    def cycle_theme():
        nonlocal current_theme_index
        if current_theme_index < len(themes_to_demo):
            theme_manager.set_theme(themes_to_demo[current_theme_index])
            current_theme_index += 1
            QTimer.singleShot(3000, cycle_theme)  # Change theme every 3 seconds
    
    # Start theme cycling after 2 seconds
    QTimer.singleShot(2000, cycle_theme)
    
    demo_window.show()
    update_theme_display()
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(demo_themes())