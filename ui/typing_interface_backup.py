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
        timer_layout out()
        timer_label = QLabel("Time")
        timer_label.setAlignment(Qt.Alignment
        timer_label.setStyleSh: 2px;")
        :00")
        timer_font = QFo
        timer_font.setPointSize(14)
        timer_font.setBold(True)
        self.timer_display.setFont(tier_font)
        self.timer_display.setAlignter)
        self.timer_display.setStyleSheet("color: 
        timer_layout.addWidget(timer_label)
        tidisplay)
        
        # WPM display
        
        wpm_label = QLabel("WP
        wpm_label.setAlignment(Qt.Alignme
        wpm_label.setStyleSheet("font-size: 9pt;x;")
        self.wpm_display = QLabel("0.0")
        wpm_font = QFont()
        wpm_font.setPointSize(14)
        wpm_font.setBold(True)
        
        self.wpm_display.setAler)
        self.wpm_display.setStyleSh;")
        wmp_layout.addWidget(wpm_label)
        wpm_layout.addWidget(self.wmpy)
        
        # Accuracy display
        accuracy_layout = QVBoxLayout()
        accuracy_label = QLabel("Accuracy")
        accuracy_label.setAlignment(Qt.Alignmer)
        )
%")
        )
        accuracy_font.set4)
        accuracy_font.setBold(True)
        self.accuracy_display.setFont(accuracy_font)
        self.accuracy_display.setAlignment()
        self.accuracy_dis;")
        accuracy_layout.addWidget(accuracy_label)
        accuracy_layout.addWi
        
        # Progress bar
        progress_layout = QVBoxLay
        progr)
        progress_label.setAligner)
        progress_label.setStyleSheet("fontpx;")
        self.
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.e)
        self
        self.progress_bar.setStyleSheet("""
        sBar {
                border: 1px solid #d1d1d1;
                border-radius: 3px;
                text-aligr;
                font-size: 9pt;
                font-weight: bold;
            }
            QProgressBar::chunk 
                background-color: 078d4;
             ;
            }
        """)
        progrl)
        prog
        
        # Add stats to bottom row
        t)
        stats_layout.addLayout(wmp_layout)
        stats_layout.addLayout(accuracy_layout)
        e space
        
        # Add both rows to main layout
        main_layout.addLayout(controls_layout)
        main_layout.addLayout(stats_lyout)
        
        group.setLayout(main_layout)
        rn group
    
    def create_sessiols(self):_contronretua moress bar# Give progr)  layout, 2rogress_ayout(paddLayout.stats_lr_layouyout(timeyout.addLastats_lar)gress_barot(self.p.addWidge_layoutressrogress_labedWidget(ps_layout.ades2pxs: diu   border-ra#0{n: cente   QProgres 20)ht(eigaximumHar.setMogress_b.prTruble(siVi_bar.setTextprogressr()ogressBa = QPrgress_barpro-bottom: 2 marginolor: #666;ize: 9pt; c-signCent.AllignmentFlagent(Qt.Amgress"bel("Pro QLalabel =ss_eout()y)acy_displaaccurget(self.ddding: 4px; pa107c10or: #Sheet("colyleplay.setStenterlignCnmentFlag.AQt.Alige(1PointSizont(t = QFy_fonaccuracl("0.0QLabedisplay = ccuracy_.a  self       2px;"m:n-bottomargior: #666; olt; c: 9pize"font-sheet(l.setStyleSaberacy_laccugnCente.AlintFlag_displang: 4px; paddi0078d4r: #coloet("eentg.AlignCignmentFla(Qt.Almentign(wpm_font)ontsetFisplay.f.wmp_dselottom: 2pmargin-b66; r: #6colo r)teenlag.AlignCntFM")yout()t = QVBoxLam_layouwper_elf.tim(sgetyout.addWidmer_lapx;")ding: 4; pad13438#dg.AlignCeignmentFlaQt.Alnment(m)nt(Label("00 Qdisplay =imer_self.targin-bottom#666; mt; color: nt-size: 9peet("fonCenter)Aliglag.F= QVBoxLay
        """Create session control panel"""
        group = QGroupBox("Session Settings")
        layout = QHBoxLayout()
        
        # Mode selection
        mode_layout = QVBoxLayout()
        mode_label = QLabel("Mode:")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            "Timed Challenge", "Accuracy Focus", 
            "Speed Burst", "Endurance"
        ])
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.mode_combo)
        
        # Difficulty selection
        difficulty_layout = QVBoxLayout()
        difficulty_label = QLabel("Difficulty:")
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Beginner", "Intermediate", "Advanced", "Expert"])
        difficulty_layout.addWidget(difficulty_label)
        difficulty_layout.addWidget(self.difficulty_combo)
        
        # Time-based selection
        time_layout = QVBoxLayout()
        time_label = QLabel("Time Selection:")
        self.time_combo = QComboBox()
        self.time_combo.addItems(["1 min (70 words)", "2 min (140 words)", "3 min (210 words)", 
                                 "5 min (350 words)", "7 min (490 words)", "10 min (700 words)"])
        self.time_combo.setCurrentIndex(0)  # Default to 1 minute
        time_layout.addWidget(time_label)
        time_layout.addWidget(self.time_combo)
        

        
        # Control buttons
        button_layout = QVBoxLayout()
        self.start_button = QPushButton("Start Session")
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #107c10;
                color: white;
                padding: 10px 20px;
                font-size: 12pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0e6e0e;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.start_button.clicked.connect(self.start_session_clicked)
        
        self.stop_button = QPushButton("Stop Session")
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #d13438;
                color: white;
                padding: 10px 20px;
                font-size: 12pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b92b2f;
            }
        """)
        self.stop_button.clicked.connect(self.stop_session_clicked)
        self.stop_button.setEnabled(False)
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        
        # Assemble layout
        layout.addLayout(mode_layout)
        layout.addLayout(difficulty_layout)
        layout.addLayout(time_layout)
        layout.addStretch()
        layout.addLayout(button_layout)
        
        group.setLayout(layout)
        return group
    
    def create_performance_stats(self):
        """Create performance statistics display"""
        group = QGroupBox("Live Performance")
        layout = QHBoxLayout()
        
        # Timer display
        timer_layout = QVBoxLayout()
        timer_label = QLabel("Time Remaining")
        timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_display = QLabel("00:00")
        timer_font = QFont()
        timer_font.setPointSize(18)
        timer_font.setBold(True)
        self.timer_display.setFont(timer_font)
        self.timer_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_display.setStyleSheet("color: #d13438; padding: 10px;")
        timer_layout.addWidget(timer_label)
        timer_layout.addWidget(self.timer_display)
        
        # WPM display
        wpm_layout = QVBoxLayout()
        wpm_label = QLabel("Words Per Minute")
        wpm_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.wpm_display = QLabel("0.0")
        wpm_font = QFont()
        wpm_font.setPointSize(18)
        wpm_font.setBold(True)
        self.wpm_display.setFont(wpm_font)
        self.wpm_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.wpm_display.setStyleSheet("color: #0078d4; padding: 10px;")
        wpm_layout.addWidget(wpm_label)
        wpm_layout.addWidget(self.wpm_display)
        
        # Accuracy display
        accuracy_layout = QVBoxLayout()
        accuracy_label = QLabel("Accuracy")
        accuracy_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.accuracy_display = QLabel("0.0%")
        accuracy_font = QFont()
        accuracy_font.setPointSize(18)
        accuracy_font.setBold(True)
        self.accuracy_display.setFont(accuracy_font)
        self.accuracy_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.accuracy_display.setStyleSheet("color: #107c10; padding: 10px;")
        accuracy_layout.addWidget(accuracy_label)
        accuracy_layout.addWidget(self.accuracy_display)
        
        # Progress bar
        progress_layout = QVBoxLayout()
        progress_label = QLabel("Progress")
        progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        progress_layout.addWidget(progress_label)
        progress_layout.addWidget(self.progress_bar)
        
        layout.addLayout(timer_layout)
        layout.addLayout(wpm_layout)
        layout.addLayout(accuracy_layout)
        layout.addLayout(progress_layout)
        
        group.setLayout(layout)
        return group
    
    def create_typing_area(self):
        """Create the main typing area with auto-scroll"""
        group = QGroupBox("Typing Practice")
        layout = QVBoxLayout()
        
        # Target text display (scrollable)
        self.target_text_display = QTextEdit()
        self.target_text_display.setReadOnly(True)
        self.target_text_display.setMinimumHeight(150)
        self.target_text_display.setMaximumHeight(200)
        self.target_text_display.setPlainText("Click 'Start Session' to begin typing practice...")
        self.target_text_display.setStyleSheet("""
            QTextEdit {
                background-color: #ffffff;
                border: 2px solid #d1d1d1;
                border-radius: 4px;
                padding: 15px;
                font-size: 16pt;
                font-family: 'Courier New', monospace;
                line-height: 1.5;
                color: #000000;
            }
            QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #c0c0c0;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a0a0a0;
            }
        """)
        
        # Typing input area
        self.typing_input = QTextEdit()
        self.typing_input.setMaximumHeight(100)
        self.typing_input.setPlaceholderText("Type here when the session starts...")
        self.typing_input.setStyleSheet("""
            font-size: 14pt;
            font-family: 'Courier New', monospace;
            border: 2px solid #0078d4;
            border-radius: 4px;
            padding: 10px;
            color: #000000;
            background-color: #ffffff;
        """)
        self.typing_input.setEnabled(False)
        self.typing_input.textChanged.connect(self.on_text_changed)
        
        layout.addWidget(self.target_text_display)
        layout.addWidget(self.typing_input)
        
        group.setLayout(layout)
        return group
    
    def setup_connections(self):
        """Set up signal connections"""
        # Connect to speed engine callbacks
        self.speed_engine.register_update_callback(self.on_performance_update)
        self.speed_engine.register_session_end_callback(self.on_session_end)
    
    def start_session_clicked(self):
        """Handle start session button click"""
        # Get selected parameters
        mode_map = {
            "Timed Challenge": GameMode.TIMED_CHALLENGE,
            "Accuracy Focus": GameMode.ACCURACY_FOCUS,
            "Speed Burst": GameMode.SPEED_BURST,
            "Endurance": GameMode.ENDURANCE
        }
        
        difficulty_map = {
            "Beginner": DifficultyLevel.BEGINNER,
            "Intermediate": DifficultyLevel.INTERMEDIATE,
            "Advanced": DifficultyLevel.ADVANCED,
            "Expert": DifficultyLevel.EXPERT
        }
        
        mode = mode_map[self.mode_combo.currentText()]
        difficulty = difficulty_map[self.difficulty_combo.currentText()]
        
        # Get time selection (extract minutes from combo text)
        time_text = self.time_combo.currentText()
        minutes = int(time_text.split()[0])  # Extract number from "X min (Y words)"
        
        # Always use time-based generation (no more custom duration)
        duration = minutes * 60  # Convert minutes to seconds for session
        
        # Start session with time-based generation (name will be asked at the end)
        self.start_session("Anonymous", mode, difficulty, duration, minutes)
    
    def start_session(self, username, mode, difficulty, duration, time_minutes):
        """Start a typing session"""
        # Always use time-based generation
        success = self.speed_engine.start_time_based_session(username, mode, difficulty, time_minutes)
        
        if success:
            self.current_session = self.speed_engine.get_current_session()
            self.start_time = time.time()
            
            # Update UI
            self.target_text_display.setPlainText(self.current_session.target_text)
            self.typing_input.setEnabled(True)
            self.typing_input.clear()
            self.typing_input.setFocus()
            
            # Update buttons
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            
            # Disable controls during session
            self.mode_combo.setEnabled(False)
            self.difficulty_combo.setEnabled(False)
            self.time_combo.setEnabled(False)
            
            self.session_started.emit()
    
    def stop_session_clicked(self):
        """Handle stop session button click"""
        self.stop_session()
    
    def stop_session(self):
        """Stop the current session"""
        if self.speed_engine.is_session_active():
            # Just end the session - the callback will handle the UI updates
            self.speed_engine.end_session()
    
    def on_text_changed(self):
        """Handle typing input changes"""
        if self.speed_engine.is_session_active():
            typed_text = self.typing_input.toPlainText()
            self.speed_engine.update_typed_text(typed_text)
            
            # Update visual feedback
            self.update_text_highlighting(typed_text)
    
    def update_text_highlighting(self, typed_text):
        """Update text highlighting for visual feedback with auto-scroll"""
        if not self.current_session:
            return
        
        target_text = self.current_session.target_text
        typed_length = len(typed_text)
        
        # Create HTML with highlighting
        html_text = ""
        current_position = 0
        
        for i, char in enumerate(target_text):
            if i < typed_length:
                if typed_text[i] == char:
                    # Correct character - green background
                    html_text += f'<span style="background-color: #90EE90; color: #000000;">{self._escape_html(char)}</span>'
                else:
                    # Incorrect character - red background
                    html_text += f'<span style="background-color: #FFB6C1; color: #000000;">{self._escape_html(char)}</span>'
                current_position = i + 1
            elif i == typed_length:
                # Current typing position - blue cursor
                html_text += f'<span style="background-color: #0078d4; color: white;">{self._escape_html(char)}</span>'
            else:
                # Not yet typed - default
                html_text += self._escape_html(char)
        
        # Update the display with HTML
        self.target_text_display.setHtml(html_text)
        
        # Auto-scroll to keep current position visible
        self._auto_scroll_to_position(current_position)
    
    def _escape_html(self, char):
        """Escape HTML special characters"""
        if char == '<':
            return '&lt;'
        elif char == '>':
            return '&gt;'
        elif char == '&':
            return '&amp;'
        elif char == '"':
            return '&quot;'
        elif char == "'":
            return '&#x27;'
        elif char == '\n':
            return '<br>'
        elif char == ' ':
            return '&nbsp;'
        elif char == '\t':
            return '&nbsp;&nbsp;&nbsp;&nbsp;'
        else:
            return char
    
    def _auto_scroll_to_position(self, position):
        """Auto-scroll to keep the current typing position visible"""
        if not self.current_session:
            return
        
        # Get the text cursor and move it to the current position
        cursor = self.target_text_display.textCursor()
        cursor.setPosition(position)
        
        # Ensure the cursor position is visible
        self.target_text_display.setTextCursor(cursor)
        self.target_text_display.ensureCursorVisible()
        
        # Additional scroll adjustment to keep some context visible
        scrollbar = self.target_text_display.verticalScrollBar()
        if scrollbar:
            # Get current scroll position
            current_scroll = scrollbar.value()
            max_scroll = scrollbar.maximum()
            
            # Calculate progress through the text
            if self.current_session.target_text:
                progress_ratio = position / len(self.current_session.target_text)
                
                # Scroll to show current position with some context
                target_scroll = int(max_scroll * progress_ratio)
                
                # Smooth scroll adjustment - don't jump too far at once
                scroll_diff = target_scroll - current_scroll
                if abs(scroll_diff) > 50:  # Only adjust if significant difference
                    new_scroll = current_scroll + (scroll_diff // 3)  # Gradual adjustment
                    scrollbar.setValue(new_scroll)
    
    def on_performance_update(self, wpm, accuracy, progress):
        """Handle performance updates from speed engine"""
        self.wpm_display.setText(f"{wpm:.1f}")
        self.accuracy_display.setText(f"{accuracy:.1f}%")
        self.progress_bar.setValue(int(progress))
    
    def on_session_end(self, score_record):
        """Handle session end"""
        # Reset UI
        self.typing_input.setEnabled(False)
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
        # Re-enable controls
        self.mode_combo.setEnabled(True)
        self.difficulty_combo.setEnabled(True)
        self.time_combo.setEnabled(True)
        
        # Reset displays
        self.timer_display.setText("00:00")
        self.target_text_display.setPlainText("Session completed! Click 'Start Session' to practice again.")
        
        # Show results and ask for user name to save record
        if score_record:
            result_text = f"Session Results:\nWPM: {score_record.wpm:.1f}\nAccuracy: {score_record.accuracy:.1f}%"
            self.target_text_display.setPlainText(result_text)
            
            # Always ask for user name to save the record
            self.ask_user_name_and_save(score_record)
            
            # Always show statistics and leaderboard after session
            self.show_session_statistics(score_record)
            self.show_leaderboard()
        
        self.current_session = None
        self.session_ended.emit(score_record)
    
    def ask_user_name_and_save(self, score_record):
        """Ask for user name and save the record"""
        from PyQt6.QtWidgets import QInputDialog, QMessageBox
        
        # Ask for user name
        user_name, ok = QInputDialog.getText(
            self, 
            "Save Your Score", 
            f"Session Complete!\n"
            f"WPM: {score_record.wpm:.1f}\n"
            f"Accuracy: {score_record.accuracy:.1f}%\n\n"
            f"Enter your name to save this score:",
            text=""
        )
        
        if ok and user_name.strip():
            # Update the score record with the new name
            score_record.user_name = user_name.strip()
            
            # Save the updated score
            self.speed_engine.db_manager.save_score(score_record)
            
            # Show confirmation
            if score_record.accuracy >= 100.0:
                QMessageBox.information(
                    self,
                    "Perfect Score Saved!",
                    f"Congratulations {user_name}!\n"
                    f"Your perfect score has been saved to the leaderboard.\n"
                    f"WPM: {score_record.wpm:.1f} | Accuracy: 100%"
                )
            else:
                QMessageBox.information(
                    self,
                    "Score Saved!",
                    f"Great job {user_name}!\n"
                    f"Your score has been saved to the leaderboard.\n"
                    f"WPM: {score_record.wpm:.1f} | Accuracy: {score_record.accuracy:.1f}%"
                )
        else:
            # User cancelled or didn't enter name
            QMessageBox.information(
                self,
                "Score Not Saved",
                f"Your score was not saved.\n"
                f"WPM: {score_record.wpm:.1f} | Accuracy: {score_record.accuracy:.1f}%"
            )
    
    def show_session_statistics(self, score_record):
        """Show session statistics automatically"""
        try:
            from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
            
            # Create statistics dialog
            stats_dialog = QDialog(self)
            stats_dialog.setWindowTitle("Session Statistics")
            stats_dialog.setModal(True)
            stats_dialog.resize(400, 300)
            
            layout = QVBoxLayout()
            
            # Session results
            layout.addWidget(QLabel(f"<h2>Session Complete!</h2>"))
            layout.addWidget(QLabel(f"<b>Words Per Minute:</b> {score_record.wpm:.1f}"))
            layout.addWidget(QLabel(f"<b>Accuracy:</b> {score_record.accuracy:.1f}%"))
            layout.addWidget(QLabel(f"<b>Mode:</b> {score_record.mode.title()}"))
            layout.addWidget(QLabel(f"<b>Difficulty:</b> {score_record.level.title()}"))
            layout.addWidget(QLabel(f"<b>Duration:</b> {score_record.duration} seconds"))
            layout.addWidget(QLabel(f"<b>Total Characters:</b> {score_record.total_characters}"))
            layout.addWidget(QLabel(f"<b>Correct Characters:</b> {score_record.correct_characters}"))
            
            # Performance rating
            if score_record.accuracy >= 100:
                rating = "🏆 PERFECT!"
            elif score_record.accuracy >= 95:
                rating = "🌟 EXCELLENT!"
            elif score_record.accuracy >= 90:
                rating = "👍 GREAT!"
            elif score_record.accuracy >= 80:
                rating = "👌 GOOD"
            else:
                rating = "📈 KEEP PRACTICING"
            
            layout.addWidget(QLabel(f"<h3>{rating}</h3>"))
            
            # Close button
            button_layout = QHBoxLayout()
            close_button = QPushButton("Continue")
            close_button.clicked.connect(stats_dialog.accept)
            button_layout.addWidget(close_button)
            layout.addLayout(button_layout)
            
            stats_dialog.setLayout(layout)
            stats_dialog.exec()
            
        except Exception as e:
            print(f"❌ Error showing statistics: {e}")
            import traceback
            traceback.print_exc()
    
    def show_leaderboard(self):
        """Show leaderboard automatically after session"""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout
        
        # Create leaderboard dialog
        leaderboard_dialog = QDialog(self)
        leaderboard_dialog.setWindowTitle("Leaderboard - Top 10")
        leaderboard_dialog.setModal(True)
        leaderboard_dialog.resize(600, 400)
        
        layout = QVBoxLayout()
        
        # Title
        layout.addWidget(QLabel("<h2>🏆 Top 10 Leaderboard</h2>"))
        
        # Get top 10 scores
        top_scores = self.speed_engine.get_leaderboard(limit=10)
        
        if top_scores:
            # Create table
            table = QTableWidget(len(top_scores), 5)
            table.setHorizontalHeaderLabels(["Rank", "Name", "WPM", "Accuracy", "Mode"])
            
            for i, score in enumerate(top_scores):
                table.setItem(i, 0, QTableWidgetItem(f"#{i+1}"))
                table.setItem(i, 1, QTableWidgetItem(score.user_name))
                table.setItem(i, 2, QTableWidgetItem(f"{score.wpm:.1f}"))
                table.setItem(i, 3, QTableWidgetItem(f"{score.accuracy:.1f}%"))
                table.setItem(i, 4, QTableWidgetItem(score.mode.title()))
            
            # Resize columns to content
            table.resizeColumnsToContents()
            layout.addWidget(table)
        else:
            layout.addWidget(QLabel("No scores recorded yet. Start typing to see your results here!"))
        
        # Close button
        button_layout = QHBoxLayout()
        close_button = QPushButton("Close")
        close_button.clicked.connect(leaderboard_dialog.accept)
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)
        
        leaderboard_dialog.setLayout(layout)
        leaderboard_dialog.exec()
    
    def update_display(self):
        """Update display with current session info"""
        if self.speed_engine.is_session_active():
            # Update timer
            remaining = self.speed_engine.get_time_remaining()
            minutes = int(remaining) // 60
            seconds = int(remaining) % 60
            self.timer_display.setText(f"{minutes:02d}:{seconds:02d}")
        elif self.timer_display.text() != "00:00" and not self.speed_engine.is_session_active():
            self.timer_display.setText("00:00")