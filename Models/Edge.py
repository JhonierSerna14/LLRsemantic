"""Edge model module for LLR semantic analyzer.

This module defines the Edge class that represents transitions between states
in the LR parsing automaton. Each edge connects two nodes and is labeled
with a symbol that triggers the transition.

Author: LLRsemantic Team
"""
from Models.Node import Node


class Edge:
    """Represents a transition edge between two nodes in the LR automaton.
    
    An edge defines a transition from one state to another based on a specific
    symbol (terminal or non-terminal). This forms the basis of the LR parsing
    automaton's state machine.
    
    Attributes:
        _origin (Node|None): Source node of the transition
        _destination (Node|None): Target node of the transition
        _transition (str): Symbol that triggers this transition
    """
    def __init__(self):
        """Initialize a new Edge instance.
        
        Creates an empty edge with no origin, destination, or transition symbol.
        These properties should be set after instantiation to define the transition.
        """
        self._origin = None
        self._destination = None
        self._transition = ""

    @property
    def origin(self) -> Node | None:
        """Get the origin node of this edge.
        
        Returns:
            Node | None: Source node of the transition, or None if not set
        """
        return self._origin

    @origin.setter
    def origin(self, value: Node | None) -> None:
        """Set the origin node of this edge.
        
        Args:
            value (Node | None): Source node to set for this transition
        """
        self._origin = value

    @property
    def destination(self) -> Node | None:
        """Get the destination node of this edge.
        
        Returns:
            Node | None: Target node of the transition, or None if not set
        """
        return self._destination

    @destination.setter
    def destination(self, value: Node | None) -> None:
        """Set the destination node of this edge.
        
        Args:
            value (Node | None): Target node to set for this transition
        """
        self._destination = value

    @property
    def transition(self) -> str:
        """Get the transition symbol for this edge.
        
        The transition symbol is the terminal or non-terminal that triggers
        the movement from the origin to the destination node.
        
        Returns:
            str: Symbol that triggers this transition
        """
        return self._transition

    @transition.setter
    def transition(self, value: str) -> None:
        """Set the transition symbol for this edge.
        
        Args:
            value (str): Symbol that should trigger this transition
        """
        self._transition = value


