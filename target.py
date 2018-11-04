import math
import itertools

# Représente une cible
class Target:

    '''
    Initialise l'objet Target
    (i,j) : coordonnées de la cible
    rank : position de la cible dans l'instance
    '''
    def __init__(self, i, j, rank):
        self.coordinates = (i,j) # coordonnées
        self.n = rank # position dans l'instance
        self.neighbors_capt = [] # voisins au sens de captation
        self.neighbors_com = [] # voisins au sens de communication mais pas de captation
        # NOTE : retirer les voisins au sens de la captation de la liste des voisins au sens de la communication,
        # et comme R_CAPT <= R_COM, permet de réduire la taille mémoire des cibles en éliminant les doublons


    '''
    Retourne les informations de la cible sous forme d'une chaine de caractères
    '''
    def __str__(self):
        return "Target (" + str(self.coordinates[0]) + " , " + str(self.coordinates[1]) + ") " + str(self.neighbors_capt)


    '''
    Retourne un itérateur sur les voisins au sens de la captation
    '''
    def get_neighbors_capt(self):
        return iter(self.neighbors_capt)


    '''
    Retourne un itérateur sur les voisins au sens de la communication
    '''
    def get_neighbors_com(self):
        # Les voisins au sens de la captation sont également des voisins au sens de la communication
        return itertools.chain(iter(self.neighbors_com),iter(self.neighbors_capt))


    '''
    Calcule la distance entre la cible courante et une autre cible
    target : cible à laquelle calculer la distance
    '''
    def distance(self, target):
        (i,j) = self.coordinates
        (k,l) = target.coordinates
        return math.sqrt((i-k)**2+(j-l) **2)
