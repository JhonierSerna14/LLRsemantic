class Production:

    def __init__(self):
        self._left = ""
        self._right = []
        self._pointIndex = 0

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, value):
        self._right = value

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value):
        self._left = value

    @property
    def pointIndex(self):
        return self._pointIndex

    @pointIndex.setter
    def pointIndex(self, value):
        self._pointIndex = value
