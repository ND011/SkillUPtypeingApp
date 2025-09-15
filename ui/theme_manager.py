"""
Theme manager for SPEED application
Handles different visual themes and styling
"""

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication
from typing import Dict
from models.user_models import Theme


class ThemeManager(QObject):
    """Manages application themes and styling"""
    
    theme_changed = pyqtSignal(str)  # Emitted when theme changes
    
    def __init__(self):
        super().__init__()
        self.current_theme = Theme.DEFAULT
        self.themes = self._initialize_themes()
    
    def _initialize_themes(self) -> Dict[Theme, Dict[str, str]]:
        """Initialize all available themes"""
        return {
            Theme.DEFAULT: {
                'name': 'Default',
                'background': '#ffffff',
                'text': '#000000',
                'primary': '#0078d4',
                'secondary': '#107c10',
                'accent': '#ff8c00',
                'error': '#d13438',
                'success': '#107c10',
                'warning': '#ff8c00',
                'border': '#d1d1d1',
                'hover': '#f3f2f1',
                'disabled': '#cccccc',
                'style': self._get_default_style()
            },
            Theme.DARK: {
                'name': 'Dark',
                'background': '#1e1e1e',
                'text': '#ffffff',
                'primary': '#0078d4',
                'secondary': '#00cc6a',
                'accent': '#ffa500',
                'error': '#ff6b6b',
                'success': '#00cc6a',
                'warning': '#ffa500',
                'border': '#404040',
                'hover': '#2d2d2d',
                'disabled': '#666666',
                'style': self._get_dark_style()
            },
            Theme.HIGH_CONTRAST: {
                'name': 'High Contrast',
                'background': '#000000',
                'text': '#ffffff',
                'primary': '#ffff00',
                'secondary': '#00ff00',
                'accent': '#ff00ff',
                'error': '#ff0000',
                'success': '#00ff00',
                'warning': '#ffff00',
                'border': '#ffffff',
                'hover': '#333333',
                'disabled': '#808080',
                'style': self._get_high_contrast_style()
            },
            Theme.BLUE: {
                'name': 'Ocean Blue',
                'background': '#f0f8ff',
                'text': '#003366',
                'primary': '#0066cc',
                'secondary': '#0099ff',
                'accent': '#3399ff',
                'error': '#cc3300',
                'success': '#009966',
                'warning': '#ff9900',
                'border': '#b3d9ff',
                'hover': '#e6f3ff',
                'disabled': '#cccccc',
                'style': self._get_blue_style()
            },
            Theme.GREEN: {
                'name': 'Forest Green',
                'background': '#f0fff0',
                'text': '#003300',
                'primary': '#006600',
                'secondary': '#009900',
                'accent': '#33cc33',
                'error': '#cc3300',
                'success': '#009900',
                'warning': '#ff9900',
                'border': '#b3ffb3',
                'hover': '#e6ffe6',
                'disabled': '#cccccc',
                'style': self._get_green_style()
            }
        }
    
    def set_theme(self, theme: Theme):
        """Set the current theme"""
        if theme in self.themes:
            self.current_theme = theme
            self._apply_theme()
            self.theme_changed.emit(theme.value)
    
    def get_current_theme(self) -> Theme:
        """Get the current theme"""
        return self.current_theme
    
    def get_theme_colors(self, theme: Theme = None) -> Dict[str, str]:
        """Get color palette for a theme"""
        if theme is None:
            theme = self.current_theme
        return self.themes.get(theme, self.themes[Theme.DEFAULT])
    
    def get_available_themes(self) -> Dict[Theme, str]:
        """Get list of available themes with their display names"""
        return {theme: colors['name'] for theme, colors in self.themes.items()}
    
    def load_default_theme(self):
        """Load the default theme"""
        self.set_theme(Theme.DEFAULT)
    
    def toggle_dark_light(self):
        """Toggle between dark and light themes"""
        if self.current_theme == Theme.DARK:
            self.set_theme(Theme.DEFAULT)
        else:
            self.set_theme(Theme.DARK)
    
    def is_dark_theme(self) -> bool:
        """Check if current theme is dark"""
        return self.current_theme in [Theme.DARK, Theme.HIGH_CONTRAST]
    
    def _apply_theme(self):
        """Apply the current theme to the application"""
        app = QApplication.instance()
        if app:
            theme_data = self.themes[self.current_theme]
            app.setStyleSheet(theme_data['style'])
    
    def _get_default_style(self) -> str:
        """Get default theme stylesheet"""
        return """
        QApplication {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 10pt;
            background-color: #ffffff;
            color: #000000;
        }
        
        QMainWindow {
            background-color: #ffffff;
            color: #000000;
        }
        
        QPushButton {
            background-color: #0078d4;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            min-width: 80px;
        }
        
        QPushButton:hover {
            background-color: #106ebe;
        }
        
        QPushButton:pressed {
            background-color: #005a9e;
        }
        
        QPushButton:disabled {
            background-color: #cccccc;
            color: #666666;
        }
        
        QTextEdit {
            background-color: #ffffff;
            color: #000000;
            border: 2px solid #d1d1d1;
            border-radius: 4px;
            padding: 10px;
            font-family: 'Courier New', monospace;
            font-size: 14pt;
        }
        
        QTextEdit:focus {
            border-color: #0078d4;
        }
        
        QLabel {
            color: #000000;
        }
        
        QGroupBox {
            font-weight: bold;
            font-size: 12pt;
            color: #323130;
            border: 2px solid #d1d1d1;
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        
        QProgressBar {
            border: 2px solid #d1d1d1;
            border-radius: 5px;
            text-align: center;
            font-weight: bold;
        }
        
        QProgressBar::chunk {
            background-color: #0078d4;
            border-radius: 3px;
        }
        
        QComboBox {
            border: 2px solid #d1d1d1;
            border-radius: 4px;
            padding: 5px;
            min-width: 100px;
        }
        
        QComboBox:focus {
            border-color: #0078d4;
        }
        
        QSpinBox {
            border: 2px solid #d1d1d1;
            border-radius: 4px;
            padding: 5px;
        }
        
        QSpinBox:focus {
            border-color: #0078d4;
        }
        """
    
    def _get_dark_style(self) -> str:
        """Get enhanced dark theme stylesheet"""
        return """
        QApplication {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 10pt;
            background-color: #1e1e1e;
            color: #ffffff;
        }
        
        QMainWindow {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        
        QWidget {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        
        QPushButton {
            background-color: #0078d4;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            min-width: 80px;
        }
        
        QPushButton:hover {
            background-color: #106ebe;
        }
        
        QPushButton:pressed {
            background-color: #005a9e;
        }
        
        QPushButton:disabled {
            background-color: #666666;
            color: #999999;
        }
        
        QTextEdit {
            background-color: #2d2d2d;
            color: #ffffff;
            border: 2px solid #404040;
            border-radius: 4px;
            padding: 10px;
            font-family: 'Courier New', monospace;
            font-size: 14pt;
            selection-background-color: #0078d4;
        }
        
        QTextEdit:focus {
            border-color: #0078d4;
        }
        
        QLabel {
            color: #ffffff;
            background-color: transparent;
        }
        
        QGroupBox {
            font-weight: bold;
            font-size: 12pt;
            color: #ffffff;
            border: 2px solid #404040;
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
            background-color: #1e1e1e;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
            background-color: #1e1e1e;
        }
        
        QProgressBar {
            border: 2px solid #404040;
            border-radius: 5px;
            text-align: center;
            font-weight: bold;
            color: #ffffff;
            background-color: #2d2d2d;
        }
        
        QProgressBar::chunk {
            background-color: #0078d4;
            border-radius: 3px;
        }
        
        QComboBox {
            background-color: #2d2d2d;
            border: 2px solid #404040;
            border-radius: 4px;
            padding: 5px;
            min-width: 100px;
            color: #ffffff;
        }
        
        QComboBox:focus {
            border-color: #0078d4;
        }
        
        QComboBox::drop-down {
            background-color: #404040;
            border: none;
        }
        
        QComboBox::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid #ffffff;
        }
        
        QComboBox QAbstractItemView {
            background-color: #2d2d2d;
            color: #ffffff;
            selection-background-color: #0078d4;
            border: 1px solid #404040;
        }
        
        QSpinBox {
            background-color: #2d2d2d;
            border: 2px solid #404040;
            border-radius: 4px;
            padding: 5px;
            color: #ffffff;
        }
        
        QSpinBox:focus {
            border-color: #0078d4;
        }
        
        QSpinBox::up-button, QSpinBox::down-button {
            background-color: #404040;
            border: none;
        }
        
        QSpinBox::up-arrow, QSpinBox::down-arrow {
            width: 10px;
            height: 10px;
        }
        
        QTableWidget {
            background-color: #2d2d2d;
            color: #ffffff;
            gridline-color: #404040;
            selection-background-color: #0078d4;
            alternate-background-color: #252525;
        }
        
        QTableWidget::item {
            padding: 5px;
            border: none;
        }
        
        QTableWidget::item:selected {
            background-color: #0078d4;
        }
        
        QHeaderView::section {
            background-color: #404040;
            color: #ffffff;
            padding: 5px;
            border: 1px solid #2d2d2d;
            font-weight: bold;
        }
        
        QTabWidget::pane {
            border: 1px solid #404040;
            background-color: #1e1e1e;
        }
        
        QTabBar::tab {
            background-color: #2d2d2d;
            color: #ffffff;
            padding: 8px 16px;
            margin-right: 2px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
        
        QTabBar::tab:selected {
            background-color: #0078d4;
        }
        
        QTabBar::tab:hover {
            background-color: #404040;
        }
        
        QMenuBar {
            background-color: #2d2d2d;
            color: #ffffff;
            border-bottom: 1px solid #404040;
        }
        
        QMenuBar::item {
            background-color: transparent;
            padding: 4px 8px;
        }
        
        QMenuBar::item:selected {
            background-color: #0078d4;
        }
        
        QMenu {
            background-color: #2d2d2d;
            color: #ffffff;
            border: 1px solid #404040;
        }
        
        QMenu::item {
            padding: 5px 20px;
        }
        
        QMenu::item:selected {
            background-color: #0078d4;
        }
        
        QStatusBar {
            background-color: #2d2d2d;
            color: #ffffff;
            border-top: 1px solid #404040;
        }
        
        QFrame {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        """
    
    def _get_high_contrast_style(self) -> str:
        """Get high contrast theme stylesheet"""
        return """
        QApplication {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 12pt;
            background-color: #000000;
            color: #ffffff;
        }
        
        QMainWindow {
            background-color: #000000;
            color: #ffffff;
        }
        
        QPushButton {
            background-color: #ffff00;
            color: #000000;
            border: 2px solid #ffffff;
            padding: 10px 20px;
            border-radius: 4px;
            font-weight: bold;
            min-width: 100px;
        }
        
        QPushButton:hover {
            background-color: #ffffff;
            color: #000000;
        }
        
        QPushButton:pressed {
            background-color: #cccccc;
            color: #000000;
        }
        
        QPushButton:disabled {
            background-color: #808080;
            color: #000000;
        }
        
        QTextEdit {
            background-color: #000000;
            color: #ffffff;
            border: 3px solid #ffffff;
            border-radius: 4px;
            padding: 15px;
            font-family: 'Courier New', monospace;
            font-size: 16pt;
        }
        
        QTextEdit:focus {
            border-color: #ffff00;
        }
        
        QLabel {
            color: #ffffff;
            font-size: 12pt;
        }
        
        QGroupBox {
            font-weight: bold;
            font-size: 14pt;
            color: #ffffff;
            border: 3px solid #ffffff;
            border-radius: 5px;
            margin-top: 15px;
            padding-top: 15px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 15px;
            padding: 0 10px 0 10px;
        }
        """
    
    def _get_blue_style(self) -> str:
        """Get blue theme stylesheet"""
        return self._get_default_style().replace('#ffffff', '#f0f8ff').replace('#000000', '#003366').replace('#0078d4', '#0066cc')
    
    def _get_green_style(self) -> str:
        """Get green theme stylesheet"""
        return self._get_default_style().replace('#ffffff', '#f0fff0').replace('#000000', '#003300').replace('#0078d4', '#006600')