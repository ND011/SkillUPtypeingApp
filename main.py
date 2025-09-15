#!/usr/bin/env python3
"""
SPEED - Advanced Keyboard Speed Training Application
Combining the best features from both Fest versions with enhancements
"""

import sys
import logging
import os
from PyQt6.QtWidgets import QApplication, QMessageBox, QSplashScreen
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPixmap, QFont
from ui.main_window import MainWindow
from game.database_manager import DatabaseManager
from ui.theme_manager import ThemeManager


def setup_logging():
    """Set up comprehensive logging for the application"""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(log_dir, 'speed_app.log')),
            logging.StreamHandler()
        ]
    )


def create_splash_screen(app):
    """Create a splash screen for application startup"""
    # Create a simple splash screen
    splash_pix = QPixmap(400, 300)
    splash_pix.fill(Qt.GlobalColor.darkBlue)
    
    splash = QSplashScreen(splash_pix, Qt.WindowType.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    
    # Add text to splash screen
    splash.showMessage("Loading SPEED...", Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter, Qt.GlobalColor.white)
    splash.show()
    
    app.processEvents()
    return splash


def initialize_application():
    """Initialize application components"""
    try:
        # Initialize database
        db_manager = DatabaseManager()
        if not db_manager.initialize():
            logging.warning("Database initialization failed, using fallback mode")
        
        # Initialize theme manager
        theme_manager = ThemeManager()
        theme_manager.load_default_theme()
        
        return True
    except Exception as e:
        logging.error(f"Application initialization failed: {e}")
        return False


class SpeedApplication:
    """Main SPEED application class"""
    
    def __init__(self):
        self.app = None
        self.main_window = None
        self.splash = None
        
    def setup_application(self):
        """Set up the QApplication with proper configuration"""
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("SPEED - Keyboard Speed Training")
        self.app.setApplicationVersion("3.0")
        self.app.setOrganizationName("SPEED Training")
        
        # Set application font
        font = QFont("Segoe UI", 10)
        self.app.setFont(font)
        
        return True
    
    def show_splash(self):
        """Show splash screen during startup"""
        self.splash = create_splash_screen(self.app)
        QTimer.singleShot(2000, self.splash.close)  # Close after 2 seconds
        
    def create_main_window(self):
        """Create and configure the main application window"""
        try:
            self.main_window = MainWindow()
            
            # Connect application-level signals
            self.app.aboutToQuit.connect(self.cleanup)
            
            return True
        except Exception as e:
            logging.error(f"Failed to create main window: {e}")
            return False
    
    def show_main_window(self):
        """Show the main application window"""
        if self.main_window:
            self.main_window.show()
            if self.splash:
                self.splash.finish(self.main_window)
    
    def cleanup(self):
        """Clean up resources before application exit"""
        logging.info("Cleaning up application resources...")
        try:
            if self.main_window:
                self.main_window.cleanup()
        except Exception as e:
            logging.error(f"Error during cleanup: {e}")
    
    def run(self):
        """Main application run loop"""
        try:
            if not self.setup_application():
                return 1
            
            self.show_splash()
            
            if not initialize_application():
                QMessageBox.critical(None, "Initialization Error", 
                                   "Failed to initialize application components.")
                return 1
            
            if not self.create_main_window():
                QMessageBox.critical(None, "Startup Error", 
                                   "Failed to create main window.")
                return 1
            
            self.show_main_window()
            
            logging.info("SPEED application started successfully")
            return self.app.exec()
            
        except Exception as e:
            logging.error(f"Critical error in application: {e}")
            try:
                QMessageBox.critical(None, "Critical Error", 
                                   f"A critical error occurred: {str(e)}")
            except:
                pass
            return 1


def main():
    """Application entry point"""
    setup_logging()
    logging.info("Starting SPEED - Keyboard Speed Training Application")
    
    try:
        app = SpeedApplication()
        return app.run()
    except Exception as e:
        logging.error(f"Failed to start application: {e}")
        return 1
    finally:
        logging.info("SPEED application shutdown complete")


if __name__ == "__main__":
    sys.exit(main())