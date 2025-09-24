# LLR Semantic Analyzer

A Python-based LR (Left-to-Right, Rightmost) parsing automaton generator and visualizer for context-free grammars.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Grammar Format](#grammar-format)
- [Examples](#examples)
- [Technical Details](#technical-details)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

## 🔍 Overview

The LLR Semantic Analyzer is an educational tool designed to help students and practitioners understand LR parsing techniques used in compiler construction. The application takes a context-free grammar as input and constructs the corresponding LR parsing automaton, providing both textual analysis and graphical visualization.

### Key Capabilities

- **Grammar Processing**: Parses context-free grammars from JSON format
- **Automaton Construction**: Builds LR(0) parsing automata with state generation
- **Visual Representation**: Interactive graphical display of states and transitions
- **Educational Focus**: Clear visualization aids in understanding parsing theory

## ✨ Features

### Core Functionality

- 🔄 **LR Automaton Generation**: Automatic construction of LR parsing states
- 📊 **Interactive Visualization**: Graphical display of automaton states and transitions  
- 📁 **JSON Grammar Import**: Support for standardized grammar file format
- 🎨 **State Differentiation**: Visual distinction between acceptance and regular states
- 🔍 **Automaton Analysis**: State counting, naming, and traversal capabilities

### User Interface

- 🖥️ **Tkinter GUI**: Clean, intuitive graphical interface
- 📂 **File Dialog Integration**: Easy grammar file selection
- ⚠️ **Error Handling**: Comprehensive error reporting and user feedback
- 🎯 **Centered Layout**: Automatic window positioning and sizing

## 🏗️ Architecture

The application follows a Model-View-Controller (MVC) architectural pattern:

### Models (`Models/`)
- **Grammar**: Represents context-free grammars with productions and symbols
- **Production**: Individual grammar rules with point indices for LR items
- **Node**: States in the LR automaton with associated productions
- **Edge**: Transitions between states labeled with symbols
- **LLR**: Complete automaton representation with start state

### Views (`View/`)
- **Interface**: Main GUI application with canvas-based automaton visualization

### Controllers (`Controller/`)
- **GrammarController**: Manages grammar creation and augmentation
- **LLRController**: Handles automaton construction and state management  
- **NodeController**: Controls individual node creation and closure computation

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Tkinter (usually included with Python)
- Standard Python libraries (json, copy, random, traceback)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/JhonierSerna14/LLRsemantic.git
   cd LLRsemantic
   ```

2. **Verify Python installation**:
   ```bash
   python --version
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

### Requirements

The application uses only Python standard library modules:
- `tkinter` - GUI framework
- `json` - Grammar file parsing
- `copy` - Deep copying for state management
- `random` - State positioning in visualization
- `traceback` - Error reporting

## 🎯 Usage

### Starting the Application

1. **Launch the program**:
   ```bash
   python main.py
   ```

2. **Load a grammar file**:
   - Click `File > Open` in the menu bar
   - Select a JSON grammar file
   - The automaton will be automatically constructed and displayed

### Grammar File Creation

Create grammar files in JSON format following the required structure:

```json
{
  "initial": "S",
  "terminals": ["a", "d"],
  "nonTerminals": ["S", "C"],
  "productions": [
    {
      "left": "S",
      "right": ["C", "C"]
    },
    {
      "left": "C",
      "right": ["a", "C"]
    },
    {
      "left": "C",
      "right": ["d"]
    }
  ]
}
```

### Visualization Features

- **Green circles**: Acceptance states (reduce actions available)
- **Pink circles**: Regular states  
- **White arrows**: Transitions between states
- **Labels**: Transition symbols and state names
- **Numbers**: Production indices for acceptance states

## 📖 Grammar Format

### JSON Structure

| Field | Type | Description |
|-------|------|-------------|
| `initial` | string | Start symbol of the grammar |
| `terminals` | array | List of terminal symbols |
| `nonTerminals` | array | List of non-terminal symbols |  
| `productions` | array | Grammar production rules |

### Production Format

Each production contains:
- `left`: Left-hand side non-terminal
- `right`: Array of right-hand side symbols

### Validation Rules

- Start symbol must be in non-terminals list
- Production left sides must be non-terminals
- Right side symbols must be declared in terminals or non-terminals
- At least one production must exist for the start symbol

## 📚 Examples

### Example 1: Simple Expression Grammar

```json
{
  "initial": "S",
  "terminals": ["id", "*", "="],
  "nonTerminals": ["S", "L", "R"],
  "productions": [
    {
      "left": "S",
      "right": ["L", "=", "R"]
    },
    {
      "left": "S", 
      "right": ["R"]
    },
    {
      "left": "L",
      "right": ["*", "R"]
    },
    {
      "left": "L",
      "right": ["id"]
    },
    {
      "left": "R",
      "right": ["L"]
    }
  ]
}
```

### Example 2: Arithmetic Expressions

```json
{
  "initial": "E",
  "terminals": ["+", "*", "(", ")", "id"],
  "nonTerminals": ["E", "T", "F"],
  "productions": [
    {
      "left": "E",
      "right": ["E", "+", "T"]
    },
    {
      "left": "E",
      "right": ["T"]
    },
    {
      "left": "T", 
      "right": ["T", "*", "F"]
    },
    {
      "left": "T",
      "right": ["F"]
    },
    {
      "left": "F",
      "right": ["(", "E", ")"]
    },
    {
      "left": "F",
      "right": ["id"]
    }
  ]
}
```

## 🔬 Technical Details

### LR Automaton Construction

The application implements the standard LR(0) automaton construction algorithm:

1. **Grammar Augmentation**: Adds new start production `S' → S`
2. **Closure Computation**: For each state, computes the closure of LR items
3. **Transition Function**: Creates GOTO transitions for symbols
4. **State Generation**: Builds complete set of LR states
5. **Conflict Detection**: Identifies reduce/reduce or shift/reduce conflicts

### State Representation

Each state contains:
- **LR Items**: Productions with point positions indicating parsing progress
- **Transitions**: Labeled edges to successor states  
- **Acceptance Info**: Production numbers for reduce actions

### Algorithms Used

- **Depth-First Search**: State traversal and analysis
- **Set Operations**: Closure computation and duplicate detection
- **Graph Algorithms**: Automaton construction and visualization layout

### Performance Considerations

- **State Limit**: Warns when automaton exceeds 32 states for visualization
- **Memory Management**: Uses efficient copying strategies for large grammars
- **UI Responsiveness**: Handles large automata gracefully with user feedback

## 📁 Project Structure

```
LLRsemantic/
├── Assets/                 # Visual resources
│   └── background.png     # Canvas background image
├── Controller/            # Business logic controllers
│   ├── GrammarController.py    # Grammar processing
│   ├── LLRController.py        # Automaton management
│   └── NodeController.py       # State creation and closure
├── Models/                # Data models
│   ├── Edge.py               # State transitions
│   ├── Grammar.py            # Grammar representation
│   ├── LLR.py               # Complete automaton
│   ├── Node.py              # Individual states
│   └── Production.py         # Grammar rules
├── View/                  # User interface
│   └── Interface.py          # Main GUI application
├── archivo.json           # Sample grammar file
├── archivo2.json          # Additional sample
├── main.py               # Application entry point
├── requirements.txt      # Dependencies (empty - uses stdlib)
└── README.md            # This documentation
```

⚡ Desarrollado con Python y ❤️

🌟 ¡Dale una estrella si te gusta el proyecto! ⭐
