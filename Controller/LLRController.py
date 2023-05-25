import copy

from Controller.NodeController import NodeController
from Models.Edge import Edge
from Models.LLR import LLR
from Models.Node import Node


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
        start.OriginalGrammar = copy.deepcopy(self._LLR.grammar)
        self._LLR.grammar.productions[0].pointIndex = -1
        start.newNode(copy.deepcopy([self._LLR.grammar.productions[0]]))
        self._LLR.start = start.Node
        # start.Node.traverse_dfs()

    def obtainNumberOfStates(self):
        start = self.LLR.start
        if start is None:
            return 0
        return self._countStates(start, 0)

    def _countStates(self, node, count) -> int:
        if len(node.edge) == 0:
            return count + 1
        for index, edge in enumerate(node.edge):
            if index == 0:
                count = self._countStates(edge.destination, count + 1)
            else:
                count = self._countStates(edge.destination, count)
        return count

    def putNameOfStates(self):
        start = self.LLR.start
        if start is None:
            return
        self._nameStates(start, 0)
        #start.traverse_dfs()

    def _nameStates(self, node, count) -> int:
        node.name = "I" + str(count)
        if len(node.edge) == 0:
            node.name = "I" + str(count)
            return count + 1
        for index, edge in enumerate(node.edge):
            if index == 0:
                count = self._nameStates(edge.destination, count + 1)
            else:
                count = self._nameStates(edge.destination, count)
        return count

    def obtainStates(self) -> list[Node]:
        start = self.LLR.start
        if start is None:
            return []
        return self._obtainListOfStates(start, [])

    def _obtainListOfStates(self, node, statesList: list[Node]) -> list[Node]:
        if len(node.edge) == 0:
            statesList.append(node)
            return statesList
        for index, edge in enumerate(node.edge):
            if index == 0:
                statesList.append(node)
                statesList = self._obtainListOfStates(edge.destination, statesList)
            else:
                statesList = self._obtainListOfStates(edge.destination, statesList)
        return statesList

    def obtainEdges(self) -> list[Edge]:
        start = self.LLR.start
        if start is None:
            return []
        return self._obtainListOfEdges(start, [])

    def _obtainListOfEdges(self, node, edgesList) -> list[Edge]:
        if len(node.edge) == 0:
            return edgesList
        edgesList.extend(node.edge)
        for index, edge in enumerate(node.edge):
                edgesList = self._obtainListOfEdges(edge.destination, edgesList)
        return edgesList
