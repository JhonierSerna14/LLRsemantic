"""Production model module for LLR semantic analyzer.

This module defines the Production class that represents a grammar production rule
with a left-hand side (non-terminal), right-hand side (sequence of symbols),
and a point index for LR parsing.

Author: LLRsemantic Team
"""


class Production:
    """Represents a production rule in a formal grammar.
    
    A production rule defines how a non-terminal symbol can be expanded
    into a sequence of terminal and/or non-terminal symbols. The point index
    is used in LR parsing to track the position within the production.
    
    Attributes:
        _left (str): Left-hand side symbol (non-terminal)
        _right (list[str]): Right-hand side sequence of symbols
        _pointIndex (int): Current position in the production for LR parsing
    """
    def __init__(self):
        """Initialize a new Production instance.
        
        Creates an empty production with no left or right-hand side symbols
        and point index set to 0.
        """
        self._left = ""
        self._right = []
        self._pointIndex = 0

    @property
    def right(self) -> list[str]:
        """Get the right-hand side of the production.
        
        Returns:
            list[str]: Sequence of symbols on the right-hand side
        """
        return self._right

    @right.setter
    def right(self, value: list[str]) -> None:
        """Set the right-hand side of the production.
        
        Args:
            value (list[str]): Sequence of symbols to set on the right-hand side
        """
        self._right = value

    @property
    def left(self) -> str:
        """Get the left-hand side of the production.
        
        Returns:
            str: Non-terminal symbol on the left-hand side
        """
        return self._left

    @left.setter
    def left(self, value: str) -> None:
        """Set the left-hand side of the production.
        
        Args:
            value (str): Non-terminal symbol to set on the left-hand side
        """
        self._left = value

    @property
    def pointIndex(self) -> int:
        """Get the current point index for LR parsing.
        
        The point index indicates the current position within the production
        during LR parsing, marking how much of the right-hand side has been processed.
        
        Returns:
            int: Current position in the production
        """
        return self._pointIndex

    @pointIndex.setter
    def pointIndex(self, value: int) -> None:
        """Set the point index for LR parsing.
        
        Args:
            value (int): Position to set within the production
        """
        self._pointIndex = value
