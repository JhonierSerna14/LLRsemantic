"""User interface module for LLR semantic analyzer.

This module provides the graphical user interface for the LLR semantic analyzer
using Tkinter. It allows users to load grammar files and visualize the resulting
LR parsing automaton with interactive graphics.

Author: LLRsemantic Team
"""
import json
import random
import tkinter
import traceback
from tkinter import messagebox, filedialog

from Controller.GrammarController import GrammarController
from Controller.LLRController import LLRController


def _obtainPossibleStatePositions() -> list[tuple[int, int]]:
    """Get predefined positions for drawing automaton states.
    
    Returns a list of coordinate tuples where states can be positioned
    on the canvas to avoid overlapping and provide good visual distribution.
    
    Returns:
        list[tuple[int, int]]: List of (x, y) coordinate tuples for state positioning
    """
    return [(50, 50), (200, 100), (350, 50), (500, 100), (650, 50), (800, 100), (950, 50), (1100, 100),
            (100, 200), (250, 250), (400, 200), (550, 250), (700, 200), (850, 250), (1000, 200), (1150, 250),
            (50, 350), (200, 400), (350, 350), (500, 400), (650, 350), (800, 400), (950, 350), (1100, 400),
            (100, 500), (250, 550), (400, 500), (550, 550), (700, 500), (850, 550), (1000, 500), (1150, 550)]


def _obtainStateSize() -> int:
    """Get the radius size for drawing state circles.
    
    Returns:
        int: Radius in pixels for state circle visualization
    """
    return 40


def _calculateMiddlePoint(position1: tuple[int, int], position2: tuple[int, int]) -> tuple[int, int]:
    """Calculate the midpoint between two coordinate positions.
    
    Used for positioning transition labels on edges between states.
    
    Args:
        position1 (tuple[int, int]): First position coordinates (x, y)
        position2 (tuple[int, int]): Second position coordinates (x, y)
    
    Returns:
        tuple[int, int]: Midpoint coordinates (x, y)
    """
    xPosition = (position1[0] + position2[0]) // 2
    yPosition = (position1[1] + position2[1]) // 2
    return (xPosition, yPosition)


class Interface(tkinter.Frame):
    """Main graphical user interface for the LLR semantic analyzer.
    
    Provides a Tkinter-based GUI that allows users to:
    - Load grammar definition files (JSON format)
    - Visualize the constructed LR parsing automaton
    - Navigate through the automaton structure graphically
    
    The interface displays states as colored circles (green for acceptance states,
    pink for regular states) connected by labeled edges representing transitions.
    
    Attributes:
        _root (tkinter.Tk): Main window root widget
        _llrController (LLRController): Controller for LR automaton operations
        _grammarController (GrammarController): Controller for grammar operations
        canvas (tkinter.Canvas): Drawing canvas for automaton visualization
        img_background (tkinter.PhotoImage): Background image for the canvas
    """

    def __init__(self, root: tkinter.Tk):
        """Initialize the main interface window.
        
        Sets up the GUI components including canvas, controllers, menu system,
        and window properties. Creates a centered window with fixed dimensions.
        
        Args:
            root (tkinter.Tk): The main Tkinter root window
        """
        super().__init__(root)
        self._root = root
        self.pack(expand=True, fill="both")
        
        # Initialize controllers for grammar and LR automaton operations
        self._llrController = LLRController()
        self._grammarController = GrammarController()
        
        # Create GUI components and menu system
        self.__createWidgets()
        self.__createMenu()

    def __createWidgets(self) -> None:
        """Create and configure the main GUI widgets.
        
        Sets up the canvas component with background image for displaying
        the automaton visualization. The canvas fills the entire window.
        """
        # Create main drawing canvas
        self.canvas = tkinter.Canvas(self, width=1200, height=600)
        
        # Load and set background image
        self.img_background = tkinter.PhotoImage(file="./Assets/background.png")
        self.canvas.create_image(0, 0, image=self.img_background, anchor="nw")
        
        # Pack canvas to fill available space
        self.canvas.pack(fill="both", expand=True)

    def __createMenu(self) -> None:
        """Create and configure the application menu bar.
        
        Sets up the File menu with options to open grammar files and close
        the application. Assigns appropriate command callbacks to menu items.
        """
        # Create main menu bar
        nav = tkinter.Menu(self._root)

        # Create File menu with open and close options
        fileOption = tkinter.Menu(nav, tearoff=False)
        fileOption.add_command(label="Open", command=self.__open)
        fileOption.add_separator()
        fileOption.add_command(label="Close", command=self._root.destroy)

        # Add File menu to menu bar and configure root window
        nav.add_cascade(label="File", menu=fileOption)
        self._root.config(menu=nav)

    def __open(self) -> None:
        """Handle file opening and grammar processing.
        
        Opens a file dialog for JSON grammar selection, processes the grammar
        to create an LR automaton, and triggers the visualization. Handles
        errors gracefully with user feedback.
        
        The process includes:
        1. File selection dialog
        2. JSON grammar parsing
        3. LR automaton construction
        4. State naming and visualization
        """
        try:
            # Open file dialog to select grammar JSON file
            file_path = filedialog.askopenfilename(
                initialdir="C:/Users/hp/PycharmProjects/LLRsemantic",
                title="Select a file",
                filetypes=(("JSON files", ".json"), ("all files", "*.*"))
            )
            
            # Load and parse grammar data from selected file
            with open(file_path, 'r', encoding='utf-8') as f:
                grammarData = json.load(f)
            
            # Create grammar and construct LR automaton
            self._llrController.LLR.grammar = self._grammarController.createGrammar(grammarData)
            self._llrController.startNode()  # Build automaton states
            self._llrController.putNameOfStates()  # Assign state names
            
            # Optional: Print automaton structure for debugging
            self._llrController.LLR.start.traverse_dfs()
            
            # Refresh canvas and draw the automaton
            self.canvas.destroy()
            self.__createWidgets()
            self.__drawAutomata()
            
        except Exception:
            # Handle any errors during file processing
            errorMessage = traceback.format_exc()
            messagebox.showerror(
                title='Error', 
                message=f'File could not be opened\n{errorMessage}'
            )

    def __drawAutomata(self) -> None:
        """Render the LR automaton graphically on the canvas.
        
        Creates a visual representation of the automaton with:
        - States as colored circles (green for acceptance, pink for regular)
        - Transitions as labeled arrows between states
        - State names and production indices displayed
        
        Automatically handles layout by randomly assigning positions from
        predefined coordinates. Shows warning for overly large automata.
        """
        # Check if automaton is too large for effective visualization
        if self._llrController.obtainNumberOfStates() > 32:
            messagebox.showwarning(
                title='Warning', 
                message='Automata very large to draw'
            )
            return
        
        # Get automaton components for drawing
        llrStates = self._llrController.obtainStates()
        llrEdges = self._llrController.obtainEdges()
        possiblePositions = _obtainPossibleStatePositions()
        stateSize = _obtainStateSize()
        statePositions: dict[str, tuple[int, int]] = {}

        # Draw all states as circles with appropriate colors and labels
        for state in llrStates:
            # Select random position for this state
            randomPosition = random.choice(possiblePositions)
            
            # Determine state color based on acceptance status
            allowed = state.allowed is not None
            color = "green" if allowed else "pink"
            
            # Draw state circle
            self.canvas.create_oval(
                randomPosition[0] - stateSize, randomPosition[1] - stateSize,
                randomPosition[0] + stateSize, randomPosition[1] + stateSize, 
                outline="black", fill=color, width=2.5
            )
            
            # Add state name label
            self.canvas.create_text(
                randomPosition[0], randomPosition[1], 
                text=state.name, font=("Verdana", 25)
            )
            
            # Add production index for acceptance states
            if allowed:
                self.canvas.create_text(
                    randomPosition[0] - stateSize, randomPosition[1] - stateSize,
                    text=state.allowed, font=("Verdana", 25)
                )
            
            # Store position for edge drawing and remove from available positions
            statePositions[state.name] = randomPosition
            possiblePositions.remove(randomPosition)

        # Draw all transitions as labeled arrows
        for edge in llrEdges:
            originPosition = statePositions[edge.origin.name]
            destinationPosition = statePositions[edge.destination.name]
            
            if edge.origin.name != edge.destination.name:
                # Draw straight arrow for different states
                self.canvas.create_line(
                    originPosition[0], originPosition[1], 
                    destinationPosition[0], destinationPosition[1], 
                    arrow=tkinter.LAST, width=1.75, fill="white"
                )
                
                # Add transition label at midpoint
                middlePoint = _calculateMiddlePoint(originPosition, destinationPosition)
                self.canvas.create_text(
                    middlePoint[0], middlePoint[1], 
                    text=edge.transition, font=("Times New Roman", 20), 
                    fill="#fbfbfb"
                )
            else:
                # Draw self-loop arc for same state transitions
                self.canvas.create_arc(
                    originPosition[0] - 25, originPosition[1] - 40, 
                    originPosition[0] + 25, originPosition[1] - 70, 
                    start=0, extent=180, style=tkinter.ARC, 
                    width=1.5, outline="white"
                )
