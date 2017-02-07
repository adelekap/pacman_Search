class ImprovedState(object):
    def __init__(self, coord):
        self.Coord = coord
        pass

    def __iter__(self):
        return (c for c in self.Coord)

    def __eq__(self, other):
        return self.Coord == other


goal = (1, 1)

initialState = (10, 10)

s = ImprovedState(initialState)

print (10,10) == s

a, b = s

print a
print b
