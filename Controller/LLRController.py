import copy
from Models.LLR import LLR
from Controller.NodeController import NodeController


class LLRController:
    def __init__(self):
        self._LLR = LLR()

    @property
    def LLR(self):
        return self._LLR

    @LLR.setter
    def LLR(self, value):
        self._LLR = value

    def startNode(self):
        start = NodeController()
        start.Node.name = self._LLR.cont
        start.OriginalGrammar = copy.deepcopy(self._LLR.grammar)
        self._LLR.grammar.productions[0].pointIndex = -1
        start.Visited = []
        start.newNode(copy.deepcopy([self._LLR.grammar.productions[0]]))
        self._LLR.start = start.Node
        self._LLR.start.traverse_dfs()
