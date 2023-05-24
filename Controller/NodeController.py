import copy
from Models.Node import Node
from Models.Edge import Edge
from Models.Grammar import Grammar
from Models.Production import Production


class NodeController:
    def __init__(self, visited):
        self._Node = Node()
        self._OriginalGrammar: Grammar
        self._Grammar = Grammar()
        self._Visited: [Production] = visited
        self._Grammar.productions.pop()

    @property
    def Node(self) -> Node:
        return self._Node

    @Node.setter
    def Node(self, value):
        self._Node = value

    @property
    def OriginalGrammar(self) -> Grammar:
        return self._OriginalGrammar

    @OriginalGrammar.setter
    def OriginalGrammar(self, value):
        self._OriginalGrammar = value

    def newNode(self, productions: [Production]):
        for p in productions:
            p.pointIndex = p.pointIndex + 1
        if self.verifyExistence(copy.deepcopy(productions)):
            for v in productions:
                self._Visited.append(v)
            self.createNode(productions)
            self.depth()

    def createNode(self, productions: [Production]) -> Node:
        for p in productions:
            if p.pointIndex < len(p.right):
                if (p.right[p.pointIndex] in self.OriginalGrammar.nonTerminals) and not (self.exists(p)):
                    self._Node.grammar.productions.append(p)
                    self.createNode(self.findProduction(p.right[p.pointIndex]))
                elif not self.exists(p):
                    self._Node.grammar.productions.append(p)
            elif not self.exists(p):
                self._Node.grammar.productions.append(p)
                self._Node.acepted = "TRUE"

    def depth(self):
        transitions = self.findTransitions()
        for tr in transitions:
            productionsToTransition = []
            for p in self._Node.grammar.productions:
                if p.pointIndex < len(p.right) and p.right[p.pointIndex] == tr:
                    productionsToTransition.append(p)
            if self.verifyExistence(copy.deepcopy(productionsToTransition)):
                node = NodeController(self._Visited)
                node._OriginalGrammar = copy.deepcopy(self._OriginalGrammar)
                node.newNode(copy.deepcopy(productionsToTransition))
                edge = Edge()
                edge.origin = self._Node
                edge.destination = node._Node
                edge.transition = tr
                self._Node.edge.append(edge)
                # print("Nodo de origen:")
                # for o in edge.origin.grammar.productions:
                #     print(o.left, "->", o.right, ":", o.pointIndex)
                # print("Transicion con: ", edge.transition)
                # print("Nodo de destino:")
                # for o in edge.destination.grammar.productions:
                #     print(o.left, "->", o.right, ":", o.pointIndex)

                # node._Node.edge.append(edge)

    def verifyExistence(self, productions: [Production]) -> bool:
        for p in productions:
            p.pointIndex = p.pointIndex + 1
        comprobando = 0
        for j in productions:
            for i in self._Visited:
                if (i.left == j.left and i.right == j.right and i.pointIndex == j.pointIndex):
                    comprobando = comprobando + 1
        if comprobando < len(productions):
            return True
        return False

    def findTransitions(self):
        trans = []
        for p in self._Node.grammar.productions:
            if p.pointIndex < len(p.right) and p.right[p.pointIndex] not in trans:
                trans.append(p.right[p.pointIndex])
        return trans

    def findProduction(self, name: str) -> [Production]:
        result = []
        for p in self.OriginalGrammar.productions:
            if p.left == name:
                result.append(p)
        return result

    def exists(self, production: Production) -> bool:
        for p in self._Node.grammar.productions:
            if p == production:
                return True
        return False
