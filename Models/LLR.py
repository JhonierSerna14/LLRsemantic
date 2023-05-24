from Models.Node import Node
from Models.Grammar import Grammar


class LLR:
    def __init__(self):
        self._start = Node()
        self._grammar = Grammar()

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = value

    @property
    def grammar(self):
        return self._grammar

    @grammar.setter
    def grammar(self, value):
        self._grammar = value
