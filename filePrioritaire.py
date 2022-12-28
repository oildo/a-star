class FilePrioritaire:
    def __init__(self):
        self.donnees = []

    def enfiler(self, valeur):
        self.donnees.append(valeur)
    
    def defiler(self):
        indice = 0
        heuristiquePlusBas = None
        for i in range(len(self.donnees)):
            if heuristiquePlusBas == None:
                heuristiquePlusBas = self.donnees[i].getHeuristique()
                indice = i
            else:
                heuristique = self.donnees[i].getHeuristique()
                if heuristiquePlusBas >heuristique:
                    heuristiquePlusBas = heuristique
                    indice = i
        return self.donnees.pop(indice)
    
    def estVide():
        return (len(self.donnees) == 0)
