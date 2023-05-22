from Models.Grammar import Grammar
from Models.Production import Production


class GrammarController:
    def __init__(self):
        self._grammar = Grammar()

    @property
    def grammar(self):
        return self._grammar

    @grammar.setter
    def grammar(self, value):
        self._grammar = value

    def createGrammar(self, data: dict) -> Grammar:
        self._grammar.productions.pop()
        self._grammar.initial = data['initial']
        self._grammar.terminals = data['terminals']
        self._grammar.nonTerminals = data['nonTerminals']
        prod = data['productions']
        for p in prod:
            production = Production()
            production.left = p['left']
            production.right = p['right']
            self._grammar.productions.append(production)
        self.expandGrammar()
        # self._grammar.print_info()
        return self._grammar

    def expandGrammar(self):
        newProduction = Production()
        name = self.add_quote_to_variable(self._grammar.initial)
        newProduction.left = name
        newProduction.right.append(self._grammar.initial)
        self._grammar.productions.insert(0, newProduction)
        self._grammar.initial = name
        self._grammar.nonTerminals.append(name)

    def add_quote_to_variable(self, name):
        new_name = name + "'"
        while self.variable_exists(new_name):
            new_name += "'"
        return new_name

    def variable_exists(self, name):
        for production in self._grammar.productions:
            if production.left == name:
                return True
        return False
