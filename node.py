class Node:
    def __init__(self, x, y, cout, heuristique):
        self.x = x
        self.y = y
        self.cout = cout
        self.heuristique = heuristique

    def getHeuristique(self):
        return self.heuristique
    
    def compareParHeuristique(nDeux):
        if self.heuristique < nDeux.getHeuristique():
            return 1
        elif self.heuristique == nDeuX.getHeuristique():
            return 0
        else:
            return 1

# https://www.geeksforgeeks.org/a-search-algorithm/