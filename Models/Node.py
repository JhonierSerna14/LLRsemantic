from Models.Grammar import Grammar


class Node:
    def __init__(self):
        from Models.Edge import Edge
        self._name = ""
        self._grammar = Grammar()
        self._edge = [Edge()]
        self._acepted = ""
        self._edge.pop()
        self._grammar.productions.pop()

    @property
    def acepted(self):
        return self._acepted

    @acepted.setter
    def acepted(self, value):
        self._acepted = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def grammar(self):
        return self._grammar

    @grammar.setter
    def grammar(self, value):
        self._grammar = value

    @property
    def edge(self):
        return self._edge

    @edge.setter
    def edge(self, value):
        self._edge = value
