"""Grammar model module for LLR semantic analyzer.

This module defines the Grammar class that represents a formal grammar
with productions, terminals, non-terminals, and an initial symbol.

Author: LLRsemantic Team
"""
from Models.Production import Production


class Grammar:
    """Represents a formal grammar for LLR parsing.
    
    A grammar consists of:
    - Productions: Rules that define how non-terminals can be expanded
    - Terminals: Symbols that cannot be further expanded
    - Non-terminals: Symbols that can be expanded using productions
    - Initial symbol: The starting symbol of the grammar
    
    Attributes:
        _productions (list[Production]): List of production rules
        _terminals (list[str]): List of terminal symbols
        _nonTerminals (list[str]): List of non-terminal symbols
        _initial (str): Initial/start symbol of the grammar
    """
    def __init__(self):
        """Initialize a new Grammar instance.
        
        Creates an empty grammar with one empty production that is later removed.
        """
        self._productions = [Production()]
        self._terminals = []
        self._nonTerminals = []
        self._initial = ""

    @property
    def initial(self) -> str:
        """Get the initial symbol of the grammar.
        
        Returns:
            str: The starting symbol of the grammar
        """
        return self._initial

    @initial.setter
    def initial(self, value: str) -> None:
        """Set the initial symbol of the grammar.
        
        Args:
            value (str): The starting symbol to set
        """
        self._initial = value

    @property
    def nonTerminals(self) -> list[str]:
        """Get the list of non-terminal symbols.
        
        Returns:
            list[str]: List of non-terminal symbols
        """
        return self._nonTerminals

    @nonTerminals.setter
    def nonTerminals(self, value: list[str]) -> None:
        """Set the list of non-terminal symbols.
        
        Args:
            value (list[str]): List of non-terminal symbols to set
        """
        self._nonTerminals = value

    @property
    def terminals(self) -> list[str]:
        """Get the list of terminal symbols.
        
        Returns:
            list[str]: List of terminal symbols
        """
        return self._terminals

    @terminals.setter
    def terminals(self, value: list[str]) -> None:
        """Set the list of terminal symbols.
        
        Args:
            value (list[str]): List of terminal symbols to set
        """
        self._terminals = value

    @property
    def productions(self) -> list[Production]:
        """Get the list of production rules.
        
        Returns:
            list[Production]: List of grammar production rules
        """
        return self._productions

    @productions.setter
    def productions(self, value: list[Production]) -> None:
        """Set the list of production rules.
        
        Args:
            value (list[Production]): List of production rules to set
        """
        self._productions = value

    def print_info(self, indent: str = "") -> None:
        """Print formatted information about the grammar.
        
        Displays all productions, initial symbol, terminals, and non-terminals
        with optional indentation for hierarchical output.
        
        Args:
            indent (str): String to use for indentation (default: "")
        """
        print(f"{indent}Productions:")
        for production in self._productions:
            print(f"{indent}  Left: {production.left}")
            print(f"{indent}  Right: {production.right}")
        print(f"{indent}Initial: {self._initial}")
        print(f"{indent}Terminals: {self._terminals}")
        print(f"{indent}Non-terminals: {self._nonTerminals}")
