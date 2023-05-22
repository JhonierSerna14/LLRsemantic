from Models.Node import Node


class Edge:
    def __init__(self):
        self._origin = None
        self._destination = None
        self._transition = ""

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = value

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, value):
        self._destination = value

    @property
    def transition(self):
        return self._transition

    @transition.setter
    def transition(self, value):
        self._transition = value
