import json
import tkinter
from tkinter import messagebox, filedialog

from Controller.GrammarController import GrammarController
from Controller.LLRController import LLRController


def __obtainPossibleStatePositions() -> list[tuple]:
    """Returns the possible positions where a state can be drawn"""
    return [(50, 50), (200, 100), (350, 50), (500, 100), (650, 50), (800, 100), (950, 50), (1100, 100),
            (100, 200), (250, 250), (400, 200), (550, 250), (700, 200), (850, 250), (1000, 200), (1150, 250),
            (50, 350), (200, 400), (350, 350), (500, 400), (650, 350), (800, 400), (950, 350), (1100, 400),
            (100, 500), (250, 550), (400, 500), (550, 550), (700, 500), (850, 550), (1000, 500), (1150, 550)]


def __obtainStateSize() -> int:
    """Returns the size of the states"""
    return 40


class Interface(tkinter.Frame):

    def __init__(self, root: tkinter.Tk):
        super().__init__(root)
        self._root = root
        self.pack(expand=True, fill="both")
        self._llrController = LLRController()
        self._grammarController = GrammarController()
        self.__createWidgets()
        self.__createMenu()

    def __createWidgets(self):
        """Here all the elements of the window are created"""
        self.canvas = tkinter.Canvas(self, width=600, height=400)
        self.img_background = tkinter.PhotoImage(file="./Assets/background.png")
        self.canvas.create_image(0, 0, image=self.img_background, anchor="nw")
        self.canvas.pack(fill="both", expand=True)

    def __createMenu(self):
        """Here you assign the menu commands to the window"""
        nav = tkinter.Menu(self._root)

        fileOption = tkinter.Menu(nav, tearoff=False)
        fileOption.add_command(label="Open", command=self.__open)
        fileOption.add_separator()
        fileOption.add_command(label="Close", command=self._root.destroy)

        nav.add_cascade(label="File", menu=fileOption)
        self._root.config(menu=nav)

    def __open(self):
        """The user is asked for a json file containing a grammar"""
        try:
            with open(filedialog.askopenfilename(initialdir="C:/Users/hp/PycharmProjects/LLRsemantic",
                                                 title="Select a file",
                                                 filetypes=(("JSON files", ".json"), ("all files", "*.*"))),
                      'r', encoding='utf-8') as f:
                grammarData = json.load(f)
            self._llrController.LLR.grammar = self._grammarController.createGrammar(grammarData)
            self._llrController.startNode()
            self.canvas.destroy()
            self.__createWidgets()
            self.__drawAutomata()

        except Exception:
            messagebox.showerror(title='Error', message=f'File could not be opened\n{Exception}')

    def __drawAutomata(self):
        """Takes the automata and draw it in the root window"""
