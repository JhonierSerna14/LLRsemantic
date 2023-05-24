from Models.Production import Production


class Grammar:
    def __init__(self):
        self._productions = [Production()]
        self._terminals = []
        self._nonTerminals = []
        self._initial = ""

    @property
    def initial(self):
        return self._initial

    @initial.setter
    def initial(self, value):
        self._initial = value

    @property
    def nonTerminals(self):
        return self._nonTerminals

    @nonTerminals.setter
    def nonTerminals(self, value):
        self._nonTerminals = value

    @property
    def terminals(self):
        return self._terminals

    @terminals.setter
    def terminals(self, value):
        self._terminals = value

    @property
    def productions(self):
        return self._productions

    @productions.setter
    def productions(self, value):
        self._productions = value

    def print_info(self, indent=""):
        print(f"{indent}Productions:")
        for production in self._productions:
            print(f"{indent}  Left: {production.left}")
            print(f"{indent}  Right: {production.right}")
        print(f"{indent}Initial: {self._initial}")
        print(f"{indent}Terminals: {self._terminals}")
        print(f"{indent}Non-terminals: {self._nonTerminals}")
