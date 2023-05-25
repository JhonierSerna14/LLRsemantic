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
        response = self.verifyExistence(copy.deepcopy(productions))
        if response[0]:
            self._Visited.append([productions, self._Node])
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
                self._Node._allowed = self.findAcepted(p)

    def depth(self):
        transitions = self.findTransitions()
        for tr in transitions:
            productionsToTransition = []
            for p in self._Node.grammar.productions:
                if p.pointIndex < len(p.right) and p.right[p.pointIndex] == tr:
                    productionsToTransition.append(p)
            response = self.verifyExistence(copy.deepcopy(productionsToTransition))
            if response[0]:
                node = NodeController(self._Visited)
                node._OriginalGrammar = copy.deepcopy(self._OriginalGrammar)
                node.newNode(copy.deepcopy(productionsToTransition))
                edge = Edge()
                edge.origin = self._Node
                edge.destination = node._Node
                edge.transition = tr
                self._Node.edge.append(edge)
            else:
                edge = Edge()
                edge.origin = self._Node
                edge.destination = response[1]
                edge.transition = tr
                response[1].grammar.print_info()
                #self._Node.edge.append(edge)
    def verifyExistence(self, productions: [Production]) -> (bool, Node):
        for p in productions:
            p.pointIndex = p.pointIndex + 1
        existenceAux = 0
        node = None
        for v in self._Visited:
            node = v[1]
            if (len(v[0]) == len(productions)):
                for i in productions:
                    for j in v[0]:
                        if (i.left == j.left and i.right == j.right and i.pointIndex == j.pointIndex):
                            existenceAux = existenceAux + 1

        if existenceAux < len(productions):
            return (True, node)
        return (False, node)

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

    def findAcepted(self, production: Production) -> str:
        for original in self.OriginalGrammar.productions:
            if (original.left == production.left and original.right == production.right):
                return self.OriginalGrammar.productions.index(original)
