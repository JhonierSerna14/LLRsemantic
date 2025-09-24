"""LLR controller module for LLR semantic analyzer.

This module provides the LLRController class that manages the construction
and manipulation of LR parsing automata. It handles the creation of states,
transitions, and provides utilities for analyzing the automaton structure.

Author: LLRsemantic Team
"""
import copy

from Controller.NodeController import NodeController
from Models.Edge import Edge
from Models.LLR import LLR
from Models.Node import Node


class LLRController:
    """Controller class for LR automaton construction and management.
    
    Manages the complete LR parsing automaton including state creation,
    transition building, and various analysis operations. Provides methods
    to construct the automaton from a grammar and extract information
    about states and transitions.
    
    Attributes:
        _LLR (LLR): The LR automaton being managed
        _Visited (list): Track visited productions during construction
    """
    def __init__(self):
        """Initialize a new LLRController instance.
        
        Creates a controller with an empty LR automaton and visited list.
        The automaton will be constructed when startNode() is called.
        """
        self._LLR = LLR()
        self._Visited = []

    @property
    def LLR(self) -> LLR:
        """Get the LR automaton being managed.
        
        Returns:
            LLR: The LR parsing automaton instance
        """
        return self._LLR

    @LLR.setter
    def LLR(self, value: LLR) -> None:
        """Set the LR automaton to manage.
        
        Args:
            value (LLR): LR automaton instance to manage
        """
        self._LLR = value

    def startNode(self) -> None:
        """Initialize the LR automaton by creating the start node.
        
        Constructs the initial state of the LR automaton using the first
        production of the grammar (augmented start production). Sets the
        point index to -1 initially, then creates the start node with
        proper closure computation.
        """
        start = NodeController(self._Visited)
        start.OriginalGrammar = copy.deepcopy(self._LLR.grammar)
        
        # Initialize with the augmented start production
        self._LLR.grammar.productions[0].pointIndex = -1
        start.newNode(copy.deepcopy([self._LLR.grammar.productions[0]]))
        self._LLR.start = start.Node
        # Optional: Uncomment to print automaton structure
        # self._LLR.start.traverse_dfs()

    def obtainNumberOfStates(self) -> int:
        """Calculate the total number of states in the LR automaton.
        
        Performs a traversal of the automaton to count all reachable states.
        Returns 0 if no start state exists.
        
        Returns:
            int: Total number of states in the automaton
        """
        start = self.LLR.start
        if start is None:
            return 0
        return self._countStates(start, 0)

    def _countStates(self, node: Node, count: int) -> int:
        """Recursive helper method to count states in the automaton.
        
        Traverses the automaton depth-first to count all reachable states.
        Only the first edge from each node contributes to the count to
        avoid double-counting shared destination states.
        
        Args:
            node (Node): Current node being processed
            count (int): Running count of states
        
        Returns:
            int: Updated count after processing this node and its children
        """
        if len(node.edge) == 0:
            return count + 1
        
        for index, edge in enumerate(node.edge):
            if index == 0:
                # Only count states from the first edge to avoid duplicates
                count = self._countStates(edge.destination, count + 1)
            else:
                count = self._countStates(edge.destination, count)
        return count

    def putNameOfStates(self) -> None:
        """Assign names to all states in the LR automaton.
        
        Traverses the automaton and assigns sequential names (I0, I1, I2, ...)
        to all states. Does nothing if no start state exists.
        """
        start = self.LLR.start
        if start is None:
            return
        self._nameStates(start, 0)
        # Optional: Uncomment to print named automaton structure
        # start.traverse_dfs()

    def _nameStates(self, node: Node, count: int) -> int:
        """Recursive helper method to assign names to states.
        
        Assigns sequential names to states during depth-first traversal.
        Names follow the pattern 'I0', 'I1', 'I2', etc.
        
        Args:
            node (Node): Current node to name
            count (int): Current naming counter
        
        Returns:
            int: Updated counter after processing this node and its children
        """
        node.name = "I" + str(count)
        
        if len(node.edge) == 0:
            return count + 1
        
        for index, edge in enumerate(node.edge):
            if index == 0:
                count = self._nameStates(edge.destination, count + 1)
            else:
                count = self._nameStates(edge.destination, count)
        return count

    def obtainStates(self) -> list[Node]:
        """Collect all states in the LR automaton into a list.
        
        Performs a traversal of the automaton to gather all reachable states.
        Returns an empty list if no start state exists.
        
        Returns:
            list[Node]: List of all states in the automaton
        """
        start = self.LLR.start
        if start is None:
            return []
        return self._obtainListOfStates(start, [])

    def _obtainListOfStates(self, node: Node, statesList: list[Node]) -> list[Node]:
        """Recursive helper method to collect states into a list.
        
        Traverses the automaton depth-first and collects all reachable states.
        Each node is added to the list when first encountered.
        
        Args:
            node (Node): Current node being processed
            statesList (list[Node]): List to accumulate states
        
        Returns:
            list[Node]: Updated list containing all discovered states
        """
        if len(node.edge) == 0:
            # Leaf node - add to list and return
            statesList.append(node)
            return statesList
        
        for index, edge in enumerate(node.edge):
            if index == 0:
                # Add current node on first edge only to avoid duplicates
                statesList.append(node)
                statesList = self._obtainListOfStates(edge.destination, statesList)
            else:
                statesList = self._obtainListOfStates(edge.destination, statesList)
        return statesList

    def obtainEdges(self) -> list[Edge]:
        """Collect all edges in the LR automaton into a list.
        
        Performs a traversal of the automaton to gather all transitions.
        Returns an empty list if no start state exists.
        
        Returns:
            list[Edge]: List of all edges/transitions in the automaton
        """
        start = self.LLR.start
        if start is None:
            return []
        return self._obtainListOfEdges(start, [])

    def _obtainListOfEdges(self, node: Node, edgesList: list[Edge]) -> list[Edge]:
        """Recursive helper method to collect edges into a list.
        
        Traverses the automaton depth-first and collects all transitions.
        All outgoing edges from each node are added to the collection.
        
        Args:
            node (Node): Current node being processed
            edgesList (list[Edge]): List to accumulate edges
        
        Returns:
            list[Edge]: Updated list containing all discovered edges
        """
        if len(node.edge) == 0:
            # Leaf node - no outgoing edges
            return edgesList
        
        # Add all outgoing edges from current node
        edgesList.extend(node.edge)
        
        # Recursively process destination nodes
        for edge in node.edge:
            edgesList = self._obtainListOfEdges(edge.destination, edgesList)
        
        return edgesList
