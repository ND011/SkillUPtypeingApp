#!/usr/bin/env python3
"""
Demo script showing auto-scroll with long text content
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from ui.typing_interface import TypingInterface
from game.speed_engine import SpeedEngine

def demo_long_text():
    """Demo the auto-scroll with your long text sample"""
    print("📜 Auto-Scroll Demo with Long Text")
    print("=" * 50)
    
    # Your long text sample
    long_text = """quilt help me two sun sit branch see table star run arm one age ice cat zebra vegetable kite plane yell eye east tea sad well done mail until grow name gut joke quest tip ugly wax low pop dry is look wet laugh loudly off egg write xmas gum idea cry walk I am thirsty sea buy key enjoy it us queen stop food think pink grow two make jeep him pig apple find here book you ask wall walk toe pack sleep lose pull knife set jug lot boy rim yellow cut sometimes village door any youth yep x-ray learn god luck small pen good need ride hit van clean water rock loud knob yes yoga umbrella hot xenops ivy blue rug has zone jump congratulations yet dirty ear fat bad vow river help sing cry way lip yarn show kiss hard easy look good luck war odd man top top road purple meal call vent rest cold xerosis jail know can car ever fifteen apple hand sixteen blue game jam zinc cook law ear seventeen had king city egg swim row never four let zip bright beautiful inch draw clap play iPad call cow move pit eleven son fast street order year chair garden cat xylem read how excuse me tree ten watch quack xiphoid zen silver knee quickly girl home gun ball always zap fish time school else will yield was hot vote zip van love lion unit kind ate ball yolk girl badly slow ant fruit fun raw end quick talk jog zebra into keep lid train teach flower new smile hug sip aim six tie over green moon no unit pot nice to meet you rip go high vase wash clean gold ten pay drink hop dig quip listen difficult ocean cool run early beach car do gray mountain earth hair owl good night happy birthday zing desert why gap take pen yonder open lit area very xylophone yule keep pig yard stop queen rain we good morning fix orange everywhere throw fit nest hum kick quiet shop dog pin red seven island forest net sun gift read take care saw old pull fox up zero in some time letter cut happen j is end of the line and eep goes in next line hard to read"""
    
    # Create QApplication
    app = QApplication(sys.argv)
    
    # Create speed engine
    speed_engine = SpeedEngine()
    
    # Create typing interface
    typing_interface = TypingInterface(speed_engine)
    
    # Create main window
    main_window = QMainWindow()
    main_window.setWindowTitle("SPEED - Long Text Auto-Scroll Demo")
    
    # Create central widget with instructions
    central_widget = QWidget()
    layout = QVBoxLayout()
    
    # Instructions
    instructions = QLabel("""
    🎯 Auto-Scroll Demo Instructions:
    
    1. This demo uses your long text sample ({} characters)
    2. Click 'Start Session' to begin typing practice
    3. As you type, notice how the text automatically scrolls
    4. The current position is highlighted with a blue cursor
    5. Correct typing shows green highlighting
    6. Mistakes show red highlighting
    7. The scroll keeps your typing position visible at all times
    
    ✨ Features demonstrated:
    • Smooth auto-scrolling
    • Visual feedback with color coding
    • Cursor position tracking
    • Automatic text wrapping
    • Scroll bar integration
    """.format(len(long_text)))
    
    instructions.setWordWrap(True)
    instructions.setStyleSheet("""
        background-color: #f0f8ff;
        border: 2px solid #4169e1;
        border-radius: 8px;
        padding: 15px;
        font-size: 11pt;
        margin: 10px;
    """)
    
    layout.addWidget(instructions)
    layout.addWidget(typing_interface)
    
    central_widget.setLayout(layout)
    main_window.setCentralWidget(central_widget)
    main_window.resize(900, 700)
    main_window.show()
    
    print(f"✅ Demo window created with {len(long_text)} character text!")
    print("📝 The auto-scroll will activate when you start typing")
    print("🎨 Watch for the color-coded feedback as you type")
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(demo_long_text())