import time
import copy

from instance import Instance
from solution import Solution

#       INST : Instance à traiter
#       Valeurs pour les instances de test : 
#       "Instances\\captANOR225_9_20.dat","Instances\\captANOR400_10_80.dat","Instances\\captANOR625_15_100.dat"
#       "Instances\\captANOR900_15_20.dat","Instances\\captANOR1500_15_100.dat","Instances\\captANOR1500_21_500.dat"
#       10,15,20,25,30,40

INST = 13

#       R : Couple R_CAPT, R_COM
#       Valeurs pour les tests :
#       (1,1),(1,2),(2,2),(2,3)

(R_CAPT, R_COM) = (1,2)

#       PARAM : paramétrage

PARAM = (300, 16000, 30, 0.25, 0.10)

# Résultat :  (Nom de l'instance, (R_CAPT, R_COM), taille de la solution, temps d'exécution)


time1 = time.time() # Temps de commencement de l'algorithme

# Initialisation de l'instance
instance = Instance(R_CAPT, R_COM)
if isinstance(INST, str):
    instance.create_from_file(INST)
else:
    instance.create_grid(INST)

# Génération d'une solution admissible par algorithme glouton
solution = Solution(instance)
solution.generate_covering_com_solution()

# Paramètres
MAX_TIME_alg = PARAM[0] # Temps d'exécution maximal de l'algorithme
MAX_NO_CHANGE_alg = int(PARAM[1] / (100 + instance.size**0.75)) # Nombre de grandes boucles maximum sans amélioration
MAX_TIME_loop = PARAM[2] # Temps d'exécution maximal d'exploration d'un voisinage
MAX_NO_CHANGE_loop = int(MAX_NO_CHANGE_alg * PARAM[3]) # Nombre de petites boucles maximum sans amélioration
ADD_CAPTS = int(PARAM[4]*instance.size) # Nombre de capteurs à ajouter à chaque boucle

# Initialisation de la meilleure solution à la solution gloutonne
best_solution = solution
best_size = solution.get_size()


# Variables pour condition de fin de l'algorithme
time_init_alg = time.time()
delta_alg = 0
no_change_alg = 0

# Parcours aléatoire du voisinage augmentant de la meilleure solution courante
while(delta_alg < MAX_TIME_alg and no_change_alg < MAX_NO_CHANGE_alg):

    # Amélioration de la solution courante

    # Initialisation de la meilleure solution locale
    best_local_solution = solution
    best_local_size = solution.get_size()

    # Suite d'améliorations aléatoires (borne temporelle)

    # Variables pour conditions de fin de la petite boucle
    time_init_loop = time.time()
    delta = 0
    no_change_loop = 0


    # Parcours aléatoire du voisinage diminuant du voisin augmentant
    while(delta < MAX_TIME_loop and no_change_loop < MAX_NO_CHANGE_loop):
        # Génération du voisin diminuant à partir du voisin augmentant
        improved = copy.deepcopy(solution)
        improved.reduce()
        # Comparaison avec la meilleure solution locale
        if improved.get_size() < best_local_size:
            best_local_solution = improved
            best_local_size = improved.get_size()
            no_change_loop = 0
        else:
            no_change_loop += 1
        delta = time.time() - time_init_loop

    # Comparaison de la meilleure solution locale avec la meilleure solution
    if best_local_size < best_size:
        best_solution = best_local_solution
        best_size = best_local_size
        no_change_alg = 0
    else:
        no_change_alg += 1

    # Sélection aléatoire d'un voisin 
    solution = copy.deepcopy(best_solution)
    solution.add_random_capt(ADD_CAPTS)
    delta_alg = time.time() - time_init_alg

time2 = time.time() # Temps de terminaison de l'algorithme

# Affichage des résultats
print((INST,(R_CAPT,R_COM),best_size,time2-time1))

# Création des fichiers SCILAB pour tracer la solution
best_solution.to_plot()
