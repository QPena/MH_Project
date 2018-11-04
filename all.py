import time
import copy

from instance import Instance
from solution import Solution

'''
Stratégies :
(300, 16000 / (n**0,75+100), 30, igb/4, 10 ou 25 ou 50)
(300, 8000 / ..., 45, igb, ...)
(300, 4000 / ..., 60, 4*igb, ...)
'''

STRATS = [  # Petite boucle
            (300, 16000, 30, 1/4, 0.10),
            (300, 16000, 30, 1/4, 0.25),
            (300, 16000, 30, 1/4, 0.50),
            # Intermédiaire
            (300, 8000, 45, 1, 0.10),
            (300, 8000, 45, 1, 0.25),
            (300, 8000, 45, 1, 0.50),
            # Grande boucle
            (300, 4000, 60, 4, 0.10),
            (300, 4000, 60, 4, 0.25),
            (300, 4000, 60, 4, 0.50)
        ]


R = [(1,1),(1,2),(2,2),(2,3)]
GRID = [10] # [10,15,20,25,30,40]
INST = ["Instances\\captANOR225_9_20.dat"]

#       ["Instances\\captANOR225_9_20.dat","Instances\\captANOR400_10_80.dat","Instances\\captANOR625_15_100.dat"]
#       "Instances\\captANOR900_15_20.dat","Instances\\captANOR1500_15_100.dat","Instances\\captANOR1500_21_500.dat"]

# Results :  (Instance name, (R_CAPT, R_COM), solution, time)

for G in GRID + INST:
    for (R_CAPT,R_COM) in R:
        print("")
        for STRAT in STRATS:
            print("")
            time1 = time.time()

            # Initialisation de l'instance
            instance = Instance(R_CAPT, R_COM)
            if isinstance(G, str):
                instance.create_from_file(G)
            else:
                instance.create_grid(G)

            solution = Solution(instance)

            # Solution admissible par algorithme glouton
            solution.generate_covering_com_solution()

            # Paramètres
            MAX_TIME_alg = STRAT[0]
            MAX_NO_CHANGE_alg = int(STRAT[1] / (100 + instance.size**0.75))
            MAX_TIME_loop = STRAT[2]
            MAX_NO_CHANGE_loop = int(MAX_NO_CHANGE_alg * STRAT[3])
            ADD_CAPTS = int(STRAT[4]*instance.size)

            # Variables pour condition de fin de l'algorithme
            time_init_alg = time.time()
            delta_alg = 0
            no_change_alg = 0

            best_solution = solution
            best_size = solution.get_size()

            # Parcours aléatoire des voisins
            # Voisinage : Ajout d'au plus N nouveaux capteurs, N paramétrable
            while(delta_alg < MAX_TIME_alg and no_change_alg < MAX_NO_CHANGE_alg):

                # Amélioration de la solution courante

                # Initialisation de la meilleure solution locale
                best_local_solution = solution
                best_local_size = solution.get_size()

                # Suite d'améliorations aléatoires (borne temporelle)

                # Variables pour conditions de fin
                time_init_loop = time.time()
                delta = 0
                no_change_loop = 0


                # Parcours aléatoire des "voisins"
                # Voisinage : Amélioration
                while(delta < MAX_TIME_loop and no_change_loop < MAX_NO_CHANGE_loop):
                    # Génération du "voisin" à partir de la solution courante
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
            time2 = time.time()
            print(STRAT)
            print((G,(R_CAPT,R_COM),best_size,time2-time1))
