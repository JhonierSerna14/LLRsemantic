"""Node controller module for LLR semantic analyzer.

This module provides the NodeController class that manages individual nodes
in the LR parsing automaton. It handles closure computation, transition
creation, and state management during automaton construction.

Author: LLRsemantic Team
"""
import copy
from Models.Node import Node
from Models.Edge import Edge
from Models.Grammar import Grammar
from Models.Production import Production


class NodeController:
    """Controller class for managing individual nodes in the LR automaton.
    
    Handles the creation and management of individual states in the LR parsing
    automaton. Responsible for computing closures, creating transitions,
    and managing the node construction process. Each controller manages one
    specific node and its associated grammar items.
    
    Attributes:
        _Node (Node): The node being managed by this controller
        _OriginalGrammar (Grammar): Reference to the original complete grammar
        _Grammar (Grammar): Local grammar for this specific node
        _Visited (list[Production]): Track visited productions to avoid cycles
    """
    def __init__(self, visited: list):
        """Initialize a new NodeController instance.
        
        Creates a controller for managing a single node in the LR automaton.
        Initializes with empty node and grammar, removing the default empty production.
        
        Args:
            visited (list): Shared list to track visited productions across controllers
        """
        self._Node = Node()
        self._OriginalGrammar: Grammar  # Will be set by the calling controller
        self._Grammar = Grammar()
        self._Visited: list[Production] = visited
        # Remove the default empty production
        self._Grammar.productions.pop()

    @property
    def Node(self) -> Node:
        """Get the node being managed by this controller.
        
        Returns:
            Node: The LR automaton node instance
        """
        return self._Node

    @Node.setter
    def Node(self, value: Node) -> None:
        """Set the node to be managed by this controller.
        
        Args:
            value (Node): Node instance to manage
        """
        self._Node = value

    @property
    def OriginalGrammar(self) -> Grammar:
        """Get the original complete grammar reference.
        
        Returns:
            Grammar: Reference to the complete original grammar
        """
        return self._OriginalGrammar

    @OriginalGrammar.setter
    def OriginalGrammar(self, value: Grammar) -> None:
        """Set the original complete grammar reference.
        
        Args:
            value (Grammar): Complete original grammar to reference
        """
        self._OriginalGrammar = value

    def newNode(self, productions: list[Production]) -> None:
        """Create a new node with the given productions.
        
        Advances the point index for all productions, checks for existing states,
        and if the state is new, creates the node and computes transitions.
        
        Args:
            productions (list[Production]): List of productions to include in this node
        """
        # Advance point index for all productions
        for p in productions:
            p.pointIndex = p.pointIndex + 1
        
        # Check if this state configuration already exists
        response = self.verifyExistence(copy.deepcopy(productions))
        if response[0]:
            # New state - add to visited and create node
            self._Visited.append([productions, self._Node])
            self.createNode(productions)
            self.depth()  # Create transitions to other states

    def createNode(self, productions: list[Production]) -> Node:
        """Create the node by computing its closure and setting productions.
        
        Processes each production to compute the LR(0) closure, adding new
        productions when the point precedes a non-terminal. Also identifies
        acceptance states.
        
        Args:
            productions (list[Production]): Initial productions for this node
        
        Returns:
            Node: The created node (same as self._Node)
        """
        for p in productions:
            if p.pointIndex < len(p.right):
                # Point is before a symbol
                if (p.right[p.pointIndex] in self.OriginalGrammar.nonTerminals and 
                    not self.exists(p)):
                    # Symbol is non-terminal - add to node and expand
                    self._Node.grammar.productions.append(p)
                    self.createNode(self.findProduction(p.right[p.pointIndex]))
                elif not self.exists(p):
                    # Symbol is terminal - just add to node
                    self._Node.grammar.productions.append(p)
            elif not self.exists(p):
                # Point is at end - this is a reduce item
                self._Node.grammar.productions.append(p)
                self._Node._allowed = self.findAccepted(p)

    def depth(self) -> None:
        """Create transitions from this node to other states.
        
        Computes all possible transitions from this node based on symbols
        following the point in productions. For each transition symbol,
        creates appropriate edges to new or existing states.
        """
        transitions = self.findTransitions()
        
        for tr in transitions:
            # Collect all productions that can transition on this symbol
            productionsToTransition = []
            for p in self._Node.grammar.productions:
                if p.pointIndex < len(p.right) and p.right[p.pointIndex] == tr:
                    productionsToTransition.append(p)
            
            # Check if this transition leads to a new or existing state
            response = self.verifyExistence(copy.deepcopy(productionsToTransition))
            
            if response[0]:
                # New state - create new node controller
                node = NodeController(self._Visited)
                node._OriginalGrammar = copy.deepcopy(self._OriginalGrammar)
                node.newNode(copy.deepcopy(productionsToTransition))
                
                # Create edge to new state
                edge = Edge()
                edge.origin = self._Node
                edge.destination = node._Node
                edge.transition = tr
                self._Node.edge.append(edge)
            else:
                # Existing state - create edge to existing node
                edge = Edge()
                edge.origin = self._Node
                edge.destination = response[1]
                edge.transition = tr
                # Debug print - uncomment if needed
                response[1].grammar.print_info()
                # Commented out to avoid duplicate edges
                # self._Node.edge.append(edge)
                
    def verifyExistence(self, productions: list[Production]) -> tuple[bool, Node]:
        """Check if a state with the given productions already exists.
        
        Compares the given productions with all previously visited states
        to determine if this state configuration has been seen before.
        
        Args:
            productions (list[Production]): Productions to check for existence
        
        Returns:
            tuple[bool, Node]: (True if new state, existing node if found)
        """
        # Advance point indices for comparison
        for p in productions:
            p.pointIndex = p.pointIndex + 1
        
        existenceAux = 0
        node = None
        
        # Check against all visited state configurations
        for v in self._Visited:
            node = v[1]
            if len(v[0]) == len(productions):
                # Same number of productions - check for exact match
                for i in productions:
                    for j in v[0]:
                        if (i.left == j.left and 
                            i.right == j.right and 
                            i.pointIndex == j.pointIndex):
                            existenceAux = existenceAux + 1

        # Return True if this is a new state (not all productions matched)
        if existenceAux < len(productions):
            return (True, node)
        return (False, node)

    def findTransitions(self) -> list[str]:
        """Find all possible transition symbols from this node.
        
        Examines all productions in the node to identify symbols that
        appear immediately after the point position. These symbols
        represent possible transitions to other states.
        
        Returns:
            list[str]: List of unique transition symbols
        """
        trans = []
        for p in self._Node.grammar.productions:
            if (p.pointIndex < len(p.right) and 
                p.right[p.pointIndex] not in trans):
                trans.append(p.right[p.pointIndex])
        return trans

    def findProduction(self, name: str) -> list[Production]:
        """Find all productions with the given left-hand side symbol.
        
        Searches the original grammar for all productions that have
        the specified non-terminal as their left-hand side.
        
        Args:
            name (str): Left-hand side symbol to search for
        
        Returns:
            list[Production]: List of productions with matching left-hand side
        """
        result = []
        for p in self.OriginalGrammar.productions:
            if p.left == name:
                result.append(p)
        return result

    def exists(self, production: Production) -> bool:
        """Check if a production already exists in this node.
        
        Determines whether the given production is already present
        in the current node's grammar to avoid duplicates.
        
        Args:
            production (Production): Production to check for existence
        
        Returns:
            bool: True if production exists in this node, False otherwise
        """
        for p in self._Node.grammar.productions:
            if p == production:
                return True
        return False

    def findAccepted(self, production: Production) -> int | None:
        """Find the index of a production for acceptance determination.
        
        Matches the given production against the original grammar to
        find its index, which is used to identify acceptance states.
        
        Args:
            production (Production): Production to find in original grammar
        
        Returns:
            int | None: Index of production in original grammar, or None if not found
        """
        for original in self.OriginalGrammar.productions:
            if (original.left == production.left and 
                original.right == production.right):
                return self.OriginalGrammar.productions.index(original)
        return None
