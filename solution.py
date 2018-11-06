import math
import random
import time

from instance import Instance

# Représente une solution pour une instance
class Solution:

    '''
    Initialise l'objet Solution
    instance : instance pour laquelle la solution est générée
    '''
    def __init__(self, instance):
        self.instance = instance # Instance
        self.list_capt = [0 for x in range(self.instance.size)] # 1 si capteur sur la cible i, 0 sinon
        self.list_count_capt = [0 for x in range(self.instance.size)] # nombre de capteurs couvrant la cible i
        self.criticals = [] # liste des capteurs critiques de la solution


    '''
    Retourne la taille de la solution
    '''
    def get_size(self):
        return sum(self.list_capt)


    '''
    Retourne la solution sous forme d'une chaine de caractères
    '''
    def __str__(self):
        s = ""
        for i in range(self.instance.size):
            if(self.instance.isGrid and i%self.instance.grid_size == 0):
                s += "\n"
            s += str(self.list_capt[i]) + "(" + str(self.list_count_capt[i]) + ")  "
        return s


    '''
    Crée deux fichiers pour tracer la solution sur SCILAB
    plot_sol.sci : ensemble des capteurs et cibles avec rayon de captation
    plot_capt.sci : ensemble des capteurs uniquement avec rayon de communication
    '''
    def to_plot(self):
        plot_sol = "clf\n"
        plot_capt = ""
        circles = "theta=0:0.1:2*%pi;\n"
        circles_capt = circles
        circles_com = circles
        x_capt = []
        y_capt = []
        x_targ = []
        y_targ = []
        # Récupération des coordonnées des capteurs et des cibles
        for i in range(self.instance.size):
            if self.list_capt[i] == 1:
                x_capt.append(self.instance.get_target(i).coordinates[0])
                y_capt.append(self.instance.get_target(i).coordinates[1])
            else:
                x_targ.append(self.instance.get_target(i).coordinates[0])
                y_targ.append(self.instance.get_target(i).coordinates[1])
        
        # Création des commandes pour tracer les capteurs
        for i in range(len(x_capt)):
            if i%100 == 0: # Note: on trace les points 100 par 100 pour ne pas faire planter SCILAB
                if i > 0:
                    plot_sol += x + "],[" + y + "], style=[-1,7])\n"
                x = ""
                y = ""
                plot_sol += "plot2d(["
            x += str(x_capt[i]) + ","
            # Commandes pour le tracé des rayons de captation et de communication pour chaque capteur
            circles_capt += "x = " + str(x_capt[i]) + '+' + str(self.instance.R_CAPT) + "*cos(theta);\n"
            circles_com +=  "x = " + str(x_capt[i]) + '+' + str(self.instance.R_COM) + "*cos(theta);\n"
            y += str(y_capt[i]) + ","
            circles_capt += "y = " + str(y_capt[i]) + '+' + str(self.instance.R_CAPT) + "*sin(theta);\n"
            circles_com += "y = " + str(y_capt[i]) + '+' + str(self.instance.R_COM) + "*sin(theta);\n"
            circles_capt += "plot2d(x,y)\n"
            circles_com += "plot2d(x,y)\n"

        plot_sol += x + "],[" + y + "], style=[-1,7])\n"

        plot_capt = plot_sol + circles_com

        # Création des commandes pour tracer les cibles
        for i in range(len(x_targ)):
            if i%100==0: # Note: on trace les points 100 par 100 pour ne pas faire planter SCILAB
                if i > 0:
                    plot_sol += x + "],[" + y + "], style=[-2,12])\n"
                x = ""
                y = ""
                plot_sol+= "plot2d(["
            x += str(x_targ[i]) + ","
            y += str(y_targ[i]) + ","

        plot_sol += x + "],[" + y + "], style=[-2,12])\n"
        plot_sol += circles_capt

        with open("plot_sol.sci",'w') as file:
            file.write(plot_sol)

        with open("plot_capt.sci", "w") as file:
            file.write(plot_capt)


    '''
    Ajoute ou retire un capteur
    rank : position du capteur à ajouter/retirer
    '''
    def set_capt(self, rank):
        # Ajout d'un capteur
        if self.list_capt[rank] == 0:
            self.list_capt[rank] = 1
            # Mise à jour du nombre de capteurs couvrant les voisins
            for neighbor in self.instance.get_target(rank).get_neighbors_capt():
                self.list_count_capt[neighbor] += 1
        # Retrait d'un capteur
        else:
            self.list_capt[rank] = 0
            # Mise à jour du nombre de capteurs couvrant les voisins
            for neighbor in self.instance.get_target(rank).get_neighbors_capt():
                self.list_count_capt[neighbor] += -1


    '''
    Création du voisin augmentant
    nb : nombre de capteurs à ajouter au maximum
    '''
    def add_random_capt(self, nb):
        # On enregistre les capteurs avant ajout
        # Note : cela permet de limiter la recherche des capteurs critiques à ces derniers
        # En effet, les capteurs nouvellement ajoutés sont retirables par construction
        capts = [x for x in range(self.instance.size) if self.list_capt[x]==1]

        # On choisit aléatoirement nb positions où ajouter un capteur
        while nb>0 and self.get_size() < self.instance.size:
            target = random.randrange(1,self.instance.size)
            # On ajoute un capteur uniquement à une cible sans capteur
            if self.list_capt[target] == 0:
                self.set_capt(target)
            nb -=1
        # On met à jour la liste des capteurs critiques
        self.find_criticals(capts)


    '''
    Génère une solution admissible pour l'instance en suivant une heuristique gloutonne
    '''
    def generate_covering_com_solution(self):
        '''
        Ajoute les voisins au sens de R_COM à la liste des cibles à considérer
        rank : position de la cible dont les voisins doivent être ajoutés
        '''
        def add_neighbors(rank):
            for nei in self.instance.get_target(rank).get_neighbors_com():
                # On ajoute tous les voisins qui ne sont pas le puits, pas déjà dans la liste
                # et sur lesquels il n'y a pas déjà un capteur
                if nei !=0 and nei not in neighbors and self.list_capt[nei] == 0:
                    neighbors.add(nei)
            # On retire la cible rank des voisins à considérer
            neighbors.remove(rank)

        neighbors = {0} # Liste des cibles en communication avec le puits
        add_neighbors(0)
        # On ajoute de nouveaux capteurs tant qu'il existe une position non captée
        while sum([1 for t in self.list_count_capt if t == 0]) > 0:
            best_next = (-1,0)
            # On cherche le voisin qui couvrira le plus de cibles non encore couvertes
            for neighbor in neighbors:
                if self.list_capt[neighbor] == 1:
                    continue
                nb_capt = sum([1 for n in self.instance.get_target(neighbor).get_neighbors_capt() if self.list_capt[n]==0])
                if nb_capt > best_next[1]:
                    best_next = (neighbor, nb_capt)
            # On ajoute un capteur au meilleur emplacement
            self.set_capt(best_next[0])
            # Si aucun voisin ne couvre de nouvelles cibles, on sort de la boucle
            if(best_next[0] == -1): break
            # On ajoute les voisins du nouveau capteur aux cibles à considérer
            add_neighbors(best_next[0])
        # On met à jour la liste des capteurs critiques de la solution générée
        self.find_criticals()


    '''
    Teste si le retrait du capteur casse la couverture au sens de la captation
    rank : position du capteur à tester
    NOTE : un capteur peut être "retirable" au sens de la captation mais casser la chaîne de communication
    '''
    def is_removable(self, rank):
        # Si le capteur n'est pas lui-même couvert, il ne peut être retiré
        if self.list_count_capt[rank] > 0:
                # Si une des cibles voisines de ce capteur n'est couverte qu'une fois, il ne peut être retiré
                for n in self.instance.get_target(rank).get_neighbors_capt():
                    if self.list_capt[n] == 0 and self.list_count_capt[n] < 2:
                        return False
                return True
        return False


    '''
    Met à jour la liste des capteurs critiques
    capts : sous-liste des capteurs à considérer ; si non renseignée alors prendre l'ensemble des capteurs
    '''
    def find_criticals(self, capts = []):
        self.criticals = []
        if len(capts) == 0:
            capts = [x for x in range(self.instance.size) if self.list_capt[x]==1]
        # Pour chaque capteur
        for capt in capts :
            # Si le retrait du capteur casse la couverture au sens de la captation, l'ajouter
            if not self.is_removable(capt):
                self.criticals.append(capt)
            # Sinon, s'il casse la chaîne de communication, l'ajouter
            else:
                # On enlève le capteur
                self.set_capt(capt)
                # On teste la connexité du graphe de communication
                if not self.is_comm_path():
                    self.criticals.append(capt)
                # On remet le capteur
                self.set_capt(capt)


    '''
    Génère un voisin diminuant de la solution courante
    '''
    def reduce(self):
        # Liste des capteurs "retirables"
        capts = [x for x in range(self.instance.size) if self.list_capt[x]==1 and x not in self.criticals]
        # Sélection aléatoire des capteurs
        while len(capts) > 0:
            t = capts[random.randrange(len(capts))]
            # Si le retrait du capteur conserve la couverture au sens de la captation
            if self.is_removable(t):
                # On retire le capteur
                self.set_capt(t)
                # Si le retrait casse la chaine de communication
                if not self.is_comm_path():
                    # On réajoute le capteur
                    self.set_capt(t)
            # On retire le capteur de la liste des capteurs à considérer
            capts.remove(t)


    '''
    Teste si la chaine de communication n'est pas coupée
    '''
    def is_comm_path(self):
        # Parcours en profondeur des capteurs en commençant par le puits

        # Liste des sommets marqués
        path = [0]
        # Liste des capteurs restants à rencontrer
        capts = {x for x in range(self.instance.size) if self.list_capt[x]==1}
        # Pour chaque sommet marqué
        for i in path:
            # On marque les voisins du sommet courant qui sont des capteurs non déjà marqués
            neighbors = [x for x in self.instance.get_target(i).get_neighbors_com() \
                            if x in capts]
            path += neighbors
            # On retire les voisins ajoutés de la liste des capteurs non rencontrés
            capts = capts.difference(neighbors)
            # Si tous les capteurs ont été rencontrés, la chaîne de communication est préservée
            if(len(capts) == 0):
                return True
        # La chaîne de communication est coupée
        return False
