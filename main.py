import json
from tkinter import Tk

from Controller.GrammarController import GrammarController
from Controller.LLRController import LLRController
from View.Interface import Interface

llrController = LLRController()


def openJson():
    grammarController = GrammarController()
    with open('archivo.json') as f:
        data = json.load(f)
    g = grammarController.createGrammar(data)
    llrController.LLR.grammar = g
    llrController.startNode()


def initializeWindow():
    root = Tk()
    root.wm_title("Formal language structure project")
    # The parameter of wn_geometry is for the window to be centered.
    root.wm_geometry(str(1200) + "x" + str(600) + "+" +
                     str(root.winfo_screenwidth() // 2 - 1200 // 2) + "+" +
                     str(root.winfo_screenheight() // 2 - 600 // 2))
    root.resizable(False, False)
    app = Interface(root)
    app.mainloop()


if __name__ == '__main__':
    openJson()
    # initializeWindow()
