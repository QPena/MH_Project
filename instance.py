from target import Target
import numpy as np
# Représente une instance
class Instance :

    '''
    Initialise l'objet Instance
    R_CAPT : rayon de captation
    R_COM : rayon de communication
    '''
    def __init__(self, R_CAPT, R_COM):
        self.targets = [] # ensemble des cibles de l'instance
        self.size = 0 # nombre de cibles dans l'instance
        self.R_COM = R_COM # rayon de captation
        self.R_CAPT = R_CAPT # rayon de communication
        self.isGrid = False
        self.grid_size = 0


    '''
    Accède aux cibles de l'instance
    '''
    def get_targets(self):
        return self.targets

    '''
    Accède à une cible de l'instance
    rank : position de la cible à retourner
    '''
    def get_target(self, rank):
        return self.targets[rank]


    '''
    Crée une instance de type grille
    grid_size : taille de la grille
    '''
    def create_grid(self, grid_size):
        self.grid_size = grid_size
        self.isGrid = True
        self.size = grid_size**2
        # Boucle de création des cibles
        for i in range(grid_size):
            for j in range(grid_size):
                self.targets.append(Target(i,j, len(self.targets)))
        # Mise à jour des voisins
        self.fill_neighbors()


    '''
    Crée une instance à partir d'un fichier
    filename : nom du fichier de données de l'instance à créer
    '''
    def create_from_file(self, filename):
        # Lecture des cibles à créer
        with open(filename, 'r') as file:
            for line in file:
                data = line.split()
                self.targets.append(Target(float(data[1]), float(data[2]), int(data[0])))
                self.size += 1
        # Mise à jour des voisins
        self.fill_neighbors()


    '''
    Met à jour les voisins au sens de la captation et de la communication pour toutes les cibles
    '''
    def fill_neighbors(self):
        # Pour chaque cible
        for target in self.get_targets():
            # Pour chaque cible de position strictement supérieure
            for j in range(target.n+1,len(self.get_targets())):
                neighbor = self.get_target(j)
                # Si la distance entre les deux cibles est inférieure au rayon de captation
                if target.distance(neighbor) <= self.R_CAPT:
                    # On ajoute chacune dans le voisinage au sens de la captation de l'autre
                    # NOTE : de par l'implémentation de l'objet Target, et comme R_CAPT <= R_COM,
                    # ajouter une cible dans le voisinage au sens de la captation l'ajoute également
                    # dans le voisinage au sens de la communication
                    target.neighbors_capt.append(j)
                    neighbor.neighbors_capt.append(target.n)
                # Si la distance entre les deux cibles est inférieure au rayon de communication
                elif target.distance(neighbor) <= self.R_COM:
                    # On ajoute chacune dans le voisinage au sens de la communication de l'autre
                    target.neighbors_com.append(j)
                    neighbor.neighbors_com.append(target.n)

