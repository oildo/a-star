import pygame
from pygame.locals import *
import networkx as nx
from node import Node
from filePrioritaire import FilePrioritaire
from math import sqrt

def rajouter_noeud(G, noeud):
    """
    Entrée : un Graphe 'grid' et un noeud
    permet de rajouter un noeud dans un Graphe de type 'grid'
    """
    x = noeud[0]
    y = noeud[1]
    if (x - 1, y) in G:
        G.add_edge(noeud, (x-1, y))
    if (x + 1, y) in G:
        G.add_edge(noeud, (x+1, y))
    if (x, y -1) in G:
        G.add_edge(noeud, (x, y -1))
    if (x, y+1) in G:
        G.add_edge(noeud, (x, y+1))


def findLowestF(G, openList):
    """
    Entrée : un Graphe et une liste 
    Sortie : le noeud ayant le plus petit "f"
    """
    f = G.nodes[openList[0]]["f"]
    out = openList[0]
    for node in openList:
        newF = G.nodes[node]["f"]
        if newF < f:
            f = newF
            out = node
    return out


def aStar(G, depart, fin):
    """
    Entrée : un Graphe 'grid'
             un noeud de départ
             un noeud d'arrivé
    Sortie : une liste de noeuds correspondant à la solution de A*
    """

    open = []
    closed = []
    open.append(depart)
    attrs = {depart: {"f": 0, "h": 0, "g": 0, "parent" : None}}
    nx.set_node_attributes(G, attrs)
    while len(open) >0:
        q = findLowestF(G, open)
        open.remove(q)
        voisins = G.neighbors(q)
        for successor in voisins:
            # stockage des h au cas où successor est déjà dans open ou closed
            openH = -1
            closedH = -1
            if successor in open:
                openH = G.nodes[successor]["h"]
            if successor in closed:
                closedH = G.nodes[successor]["h"]
            
            # si successor est le noeud fin, on retourne le chemin
            if successor[0] == fin[0] and successor[1] == fin[1]:
                current = q
                chemin = [successor]  # on fait ainsi car successor n'a pas de parent défini à ce stade
                # on remonte les parents des noeuds jusqu'au départ (parent = None)
                while current != None:
                    chemin.append(current)
                    current = G.nodes[current]["parent"]
                return chemin
            
            # on calcule la distance du point au départ et à la fin
            g = G.nodes[q]["g"] + 1
            h = sqrt((successor[0] - fin[0])**2 +  (successor[1] - fin[1])**2) # distance euclidienne
            attrs = {successor: {"f": g+h, "h": h, "g": g, "parent" : q}}

            # si le noeud a déja été testé avec une heuristique moins élevé, on ne le rajoute pas
            if (openH == -1 or openH > attrs[successor]["h"]) and (closedH == -1 or closedH > attrs[successor]["h"]) :
                nx.set_node_attributes(G, attrs)
                open.append(successor)
        closed.append(q)
    




def main():
    # initialisationd des différentes variables
    windowDim = [600, 600]
    backGroundColor = (255, 255, 255)
    div = 20
    cell_dim = windowDim[0]//div
    etat = 0 # 0 = enlever/ajouter noeuds, 1 = mettre un debut, 2 = mettre une fin
    debut = (10, 3)
    fin = (10, 15)
    refresh = True # si true, on redessine la page
    solution = [] #resultat de l'algorithme pour pouvoir le dessiner

    # initialisation de pygame
    pygame.init()
    window = pygame.display.set_mode((windowDim[0], windowDim[1]))
    pygame.display.set_caption("Algorithme A*")
    window.fill(backGroundColor)

    # initialisation du Graphe
    G = nx.Graph()
    G = nx.grid_2d_graph(windowDim[0] // div - 1,windowDim[1] // div - 1)




    # boucle programme
    stopped = False  # si stopped = True, le programme s'arête au prochain tour de boucle
    while not(stopped):

        # permet de géret les évenements pygame
        for event in pygame.event.get():

            # manières d'arêter l'application
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                stopped = True
            elif event.type == MOUSEBUTTONDOWN:
                tmp = (div * event.pos[1]// windowDim[1], div * event.pos[0]// windowDim[0])
                if etat == 0: # place un obstacle en enlevant le noeud du Graphe
                    if tmp in G and not( tmp == debut or tmp == fin):
                        G.remove_node(tmp)
                        refresh = True
                    else:
                        rajouter_noeud(G, tmp)

                        refresh = True
                elif etat == 1: # permet de placer un début
                    if tmp in G and not( tmp == debut or tmp == fin):
                        debut = tmp
                        etat = 0
                        refresh = True
                    else:
                        print("placement non valide")
                elif etat == 2: # permet de placer une fin
                    if tmp in G and not( tmp == debut or tmp == fin):
                        fin = tmp
                        etat = 0
                        refresh = True
                    else:
                        print("placement non valide")

            if event.type == KEYDOWN:
                # changements d'etat
                if event.key == K_s:
                    if etat == 1:
                        etat = 0
                    else:
                        etat = 1
                elif event.key == K_e:
                    if etat == 2:
                        etat = 0
                    else:
                        etat = 2
                
                elif event.key == K_SPACE: # lance l'algorithme
                    solution = aStar(G, debut, fin)
                    refresh = True

        # ---draw---
        
        if refresh:
            window.fill(backGroundColor)

            # dessine les obstacles
            for i in range(cell_dim):
                for j in range(cell_dim):
                    if not (j, i) in G:
                        pygame.draw.rect(window, (0, 0, 0), pygame.Rect(i * cell_dim, j * cell_dim, cell_dim, cell_dim))
            
            # dessine la solution
            for noeud in solution:
                pygame.draw.rect(window, (108, 0, 190), pygame.Rect(noeud[1] * cell_dim, noeud[0] * cell_dim, cell_dim, cell_dim))
            solution = []
                

            # dessine debut et fin
            pygame.draw.rect(window, (113, 113, 113), pygame.Rect(debut[1] * cell_dim, debut[0] * cell_dim, cell_dim, cell_dim))
            pygame.draw.rect(window, (0, 255, 0), pygame.Rect(fin[1] * cell_dim, fin[0] * cell_dim, cell_dim, cell_dim))
            

            refresh = False

        # rafraichie la fenêtre
        pygame.display.flip()

if __name__ == "__main__":
    main()