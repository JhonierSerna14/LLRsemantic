"""LLR model module for LLR semantic analyzer.

This module defines the LLR class that represents the complete LR parsing automaton.
It contains the start node of the automaton and the original grammar used to
construct the parser.

Author: LLRsemantic Team
"""
from Models.Node import Node
from Models.Grammar import Grammar


class LLR:
    """Represents the complete LR parsing automaton.
    
    The LLR class encapsulates the entire parsing automaton including:
    - The start node/state of the automaton
    - The original grammar from which the automaton was constructed
    
    This serves as the main entry point for LR parsing operations.
    
    Attributes:
        _start (Node): Initial state/node of the LR automaton
        _grammar (Grammar): Original grammar used to build the automaton
    """
    def __init__(self):
        """Initialize a new LLR automaton instance.
        
        Creates an empty LR automaton with a new start node and empty grammar.
        The automaton must be constructed by setting the grammar and building
        the state transitions.
        """
        self._start = Node()
        self._grammar = Grammar()

    @property
    def start(self) -> Node:
        """Get the start node of the LR automaton.
        
        Returns:
            Node: Initial state/node of the automaton
        """
        return self._start

    @start.setter
    def start(self, value: Node) -> None:
        """Set the start node of the LR automaton.
        
        Args:
            value (Node): Node to set as the initial state of the automaton
        """
        self._start = value

    @property
    def grammar(self) -> Grammar:
        """Get the grammar associated with this LR automaton.
        
        Returns:
            Grammar: Original grammar used to construct the automaton
        """
        return self._grammar

    @grammar.setter
    def grammar(self, value: Grammar) -> None:
        """Set the grammar for this LR automaton.
        
        Args:
            value (Grammar): Grammar to use for constructing the automaton
        """
        self._grammar = value
