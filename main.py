from Controller.GrammarController import GrammarController
from Controller.NodeController import NodeController
from Controller.LLRController import LLRController
from Models.Production import Production
import json

llrController = LLRController()


def openJson():
    grammarController = GrammarController()
    with open('archivo.json') as f:
        data = json.load(f)
    g = grammarController.createGrammar(data)
    llrController.LLR.grammar = g
    llrController.startNode()


if __name__ == '__main__':
    openJson()
