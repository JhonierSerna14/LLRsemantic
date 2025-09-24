"""Main entry point for the LLR Semantic Analyzer application.

This module provides the main application entry point for the LLR (Left-to-Right
Rightmost) semantic analyzer. It initializes the GUI application and provides
utility functions for JSON grammar processing.

The application allows users to:
- Load context-free grammars from JSON files
- Construct LR parsing automata
- Visualize the automaton graphically
- Analyze grammar properties

Author: LLRsemantic Team
Version: 1.0
"""
import json
from tkinter import Tk

from Controller.GrammarController import GrammarController
from Controller.LLRController import LLRController
from View.Interface import Interface

# Global LLR controller instance for grammar processing operations
llrController = LLRController()


def openJson() -> None:
    """Load and process a grammar from a JSON file.
    
    Reads grammar data from 'archivo.json', creates a Grammar object,
    constructs the LR automaton, and extracts edge information.
    This function is currently unused but available for testing purposes.
    
    Note:
        This function is hardcoded to read from 'archivo.json'.
        Consider making the filename configurable for better flexibility.
    """
    # Initialize grammar controller
    grammarController = GrammarController()
    
    # Load grammar data from JSON file
    with open('archivo.json') as f:
        data = json.load(f)
    
    # Create grammar object and configure LLR controller
    g = grammarController.createGrammar(data)
    llrController.LLR.grammar = g
    
    # Build the LR automaton
    llrController.startNode()
    
    # Extract edge information (for debugging/analysis)
    a = llrController.obtainEdges()


def initializeWindow() -> None:
    """Initialize and start the main GUI application window.
    
    Creates a centered Tkinter window with fixed dimensions and starts
    the main application interface. The window is configured with:
    - Title: "Formal language structure project"
    - Size: 1200x600 pixels
    - Position: Centered on screen
    - Non-resizable
    """
    # Create main Tkinter root window
    root = Tk()
    root.wm_title("Formal language structure project")
    
    # Calculate center position for window placement
    window_width = 1200
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    x_position = screen_width // 2 - window_width // 2
    y_position = screen_height // 2 - window_height // 2
    
    # Set window geometry (size and position)
    root.wm_geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    # Make window non-resizable
    root.resizable(False, False)
    
    # Create and start the main application interface
    app = Interface(root)
    app.mainloop()


if __name__ == '__main__':
    """Main execution block.
    
    Entry point for the application. Currently starts the GUI interface.
    The openJson() function call is commented out but can be used for
    direct grammar processing without the GUI.
    
    Usage:
        python main.py
    """
    # Optional: Uncomment to process grammar directly from JSON
    # openJson()
    
    # Start the main GUI application
    initializeWindow()
