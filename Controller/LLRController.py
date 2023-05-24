import copy
from Models.LLR import LLR
from Controller.NodeController import NodeController


class LLRController:
    def __init__(self):
        self._LLR = LLR()
        self._Visited = []

    @property
    def LLR(self):
        return self._LLR

    @LLR.setter
    def LLR(self, value):
        self._LLR = value

    def startNode(self):
        start = NodeController(self._Visited)
        start.Node.name = self._LLR.cont
        start.OriginalGrammar = copy.deepcopy(self._LLR.grammar)
        self._LLR.grammar.productions[0].pointIndex = -1
        start.newNode(copy.deepcopy([self._LLR.grammar.productions[0]]))
        self._LLR.start = start.Node
        self._LLR.start.traverse_dfs()

    def obtainNumberOfStates(self):
        start = self.LLR.start
        if start == None:
            return 0
        return self._countStates(start, 0)

    def _countStates(self, node, count) -> int:
        if len(node.edge) == 0:
            return count + 1
        for edge in node.edge:
            count = self._countStates(edge.destination, count)
        return count