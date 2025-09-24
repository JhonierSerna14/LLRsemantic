"""Grammar controller module for LLR semantic analyzer.

This module provides the GrammarController class that handles grammar creation,
expansion, and manipulation operations. It processes JSON grammar definitions
and prepares them for LR parsing by adding augmented start productions.

Author: LLRsemantic Team
"""
from Models.Grammar import Grammar
from Models.Production import Production


class GrammarController:
    """Controller class for grammar operations and transformations.
    
    Handles the creation of Grammar objects from JSON data and performs
    necessary transformations such as grammar augmentation for LR parsing.
    Grammar augmentation involves adding a new start symbol to eliminate
    ambiguity in the parsing process.
    
    Attributes:
        _grammar (Grammar): The grammar instance being managed
    """
    def __init__(self):
        """Initialize a new GrammarController instance.
        
        Creates a controller with an empty grammar that can be populated
        through the createGrammar method.
        """
        self._grammar = Grammar()

    @property
    def grammar(self) -> Grammar:
        """Get the current grammar instance.
        
        Returns:
            Grammar: The grammar object being managed by this controller
        """
        return self._grammar

    @grammar.setter
    def grammar(self, value: Grammar) -> None:
        """Set the current grammar instance.
        
        Args:
            value (Grammar): Grammar object to manage
        """
        self._grammar = value

    def createGrammar(self, data: dict) -> Grammar:
        """Create a Grammar object from JSON dictionary data.
        
        Parses the provided dictionary to extract grammar components and
        creates a complete Grammar object. Also performs grammar augmentation
        by adding a new start symbol.
        
        Args:
            data (dict): Dictionary containing grammar data with keys:
                        'initial', 'terminals', 'nonTerminals', 'productions'
        
        Returns:
            Grammar: Fully constructed and augmented grammar object
        """
        # Remove the initial empty production
        self._grammar.productions.pop()
        
        # Set basic grammar properties
        self._grammar.initial = data['initial']
        self._grammar.terminals = data['terminals']
        self._grammar.nonTerminals = data['nonTerminals']
        
        # Process productions from JSON data
        prod = data['productions']
        for p in prod:
            production = Production()
            production.left = p['left']
            production.right = p['right']
            self._grammar.productions.append(production)
        
        # Augment grammar for LR parsing
        self.expandGrammar()
        return self._grammar

    def expandGrammar(self) -> None:
        """Augment the grammar by adding a new start production.
        
        Creates a new start symbol (with apostrophe suffix) and adds a production
        that derives the original start symbol. This augmentation is necessary
        for LR parsing to properly handle the acceptance state.
        """
        newProduction = Production()
        # Generate a unique name for the augmented start symbol
        name = self.add_quote_to_variable(self._grammar.initial)
        newProduction.left = name
        newProduction.right.append(self._grammar.initial)
        
        # Insert at beginning to make it the new start production
        self._grammar.productions.insert(0, newProduction)
        self._grammar.initial = name
        self._grammar.nonTerminals.append(name)

    def add_quote_to_variable(self, name: str) -> str:
        """Generate a unique variable name by adding apostrophe suffixes.
        
        Continuously adds apostrophes to the given name until a unique
        variable name is found that doesn't conflict with existing productions.
        
        Args:
            name (str): Base variable name to modify
        
        Returns:
            str: Unique variable name with apostrophe suffix
        """
        new_name = name + "'"
        while self.variable_exists(new_name):
            new_name += "'"
        return new_name

    def variable_exists(self, name: str) -> bool:
        """Check if a variable name already exists in the grammar productions.
        
        Searches through all production left-hand sides to determine if
        the given variable name is already in use.
        
        Args:
            name (str): Variable name to check for existence
        
        Returns:
            bool: True if variable exists, False otherwise
        """
        for production in self._grammar.productions:
            if production.left == name:
                return True
        return False
