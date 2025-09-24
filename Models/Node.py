"""Node model module for LLR semantic analyzer.

This module defines the Node class that represents a state in the LR automaton.
Each node contains a grammar with production rules, edges to other nodes,
and acceptance information for parsing.

Author: LLRsemantic Team
"""
from Models.Grammar import Grammar


class Node:
    """Represents a state node in the LR parsing automaton.
    
    Each node in the automaton contains:
    - A grammar with production rules relevant to this state
    - Edges connecting to other states based on symbol transitions
    - Name identifier for the state
    - Allowed production index for acceptance states
    
    Attributes:
        _name (str): Identifier name for the node/state
        _grammar (Grammar): Grammar containing productions for this state
        _edge (list[Edge]): List of transitions to other nodes
        _allowed (int|None): Production index if this is an acceptance state
    """
    def __init__(self):
        """Initialize a new Node instance.
        
        Creates a new state node with empty grammar, no edges, and no name.
        The initial empty production and edge are removed during initialization
        to provide clean starting containers.
        """
        from Models.Edge import Edge  # Import here to avoid circular dependency
        self._name = ""
        self._grammar = Grammar()
        self._edge = [Edge()]
        self._allowed = None
        # Remove the initial empty edge and production
        self._edge.pop()
        self._grammar.productions.pop()

    @property
    def allowed(self) -> int | None:
        """Get the production index for acceptance states.
        
        Returns:
            int | None: Index of the accepted production, or None if not an acceptance state
        """
        return self._allowed

    @allowed.setter
    def allowed(self, value: int | None) -> None:
        """Set the production index for acceptance states.
        
        Args:
            value (int | None): Production index to set, or None for non-acceptance states
        """
        self._allowed = value

    @property
    def name(self) -> str:
        """Get the name identifier of the node.
        
        Returns:
            str: Name/identifier of this node
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set the name identifier of the node.
        
        Args:
            value (str): Name/identifier to assign to this node
        """
        self._name = value

    @property
    def grammar(self) -> Grammar:
        """Get the grammar associated with this node.
        
        Returns:
            Grammar: Grammar object containing productions for this state
        """
        return self._grammar

    @grammar.setter
    def grammar(self, value: Grammar) -> None:
        """Set the grammar associated with this node.
        
        Args:
            value (Grammar): Grammar object to associate with this state
        """
        self._grammar = value

    @property
    def edge(self) -> list:
        """Get the list of edges from this node.
        
        Returns:
            list[Edge]: List of transition edges to other nodes
        """
        return self._edge

    @edge.setter
    def edge(self, value: list) -> None:
        """Set the list of edges from this node.
        
        Args:
            value (list[Edge]): List of transition edges to set
        """
        self._edge = value

    def traverse_dfs(self) -> None:
        """Perform depth-first traversal of the automaton starting from this node.
        
        Visits each reachable node exactly once and prints their grammar information.
        Uses a visited set to prevent infinite loops in cyclic graphs.
        """
        visited = set()
        self._dfs_helper(visited)

    def _dfs_helper(self, visited: set) -> None:
        """Recursive helper method for depth-first traversal.
        
        Args:
            visited (set): Set of already visited nodes to prevent cycles
        """
        visited.add(self)
        self.print_grammar()

        for edge in self._edge:
            destination_node = edge.destination
            if destination_node not in visited:
                destination_node._dfs_helper(visited)

    def print_grammar(self, indent: str = "") -> None:
        """Print detailed information about this node and its grammar.
        
        Displays node name, associated grammar productions, and outgoing edges
        with optional indentation for hierarchical output.
        
        Args:
            indent (str): String to use for indentation (default: "")
        """
        print(f"{indent}Node: {self._name}")
        self._grammar.print_info(indent + "  ")
        print(f"{indent}Edges:")
        for edge in self._edge:
            print(f"{indent}  Origin: {edge.origin.name}")
            print(f"{indent}  Destination: {edge.destination.name}")
            print(f"{indent}  Transition: {edge.transition}")
        print(f"{indent}-------------------")