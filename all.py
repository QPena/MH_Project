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


R = [(1,1),(1,2),(2,2),(2,3)]
GRID = [40] # [10,15,20,25,30,40]
INST = ["Instances\\captANOR900_15_20.dat"]

#       ["Instances\\captANOR225_9_20.dat","Instances\\captANOR400_10_80.dat","Instances\\captANOR625_15_100.dat"]
#       "Instances\\captANOR900_15_20.dat","Instances\\captANOR1500_15_100.dat","Instances\\captANOR1500_21_500.dat"]

# Results :  (Instance name, (R_CAPT, R_COM), solution, time)

for G in GRID:
    for (R_CAPT,R_COM) in R:

        time1 = time.time()

        # Initialisation de l'instance
        instance = Instance(R_CAPT, R_COM)
        print(G)
        if isinstance(G, str):
            instance.create_from_file(G)
        else:
            instance.create_grid(G)

        instance.fill_neighbors()

        solution = Solution(instance)

        # Solution admissible par algorithme glouton
        solution.generate_covering_com_solution()


        # Variables pour condition de fin de l'algorithme
        time_init_alg = time.time()
        delta_alg = 0
        no_change_alg = 0
        MAX_TIME_alg = 5*60
        MAX_NO_CHANGE_alg = 20

        best_solution = solution
        best_size = solution.get_size()

        # Parcours aléatoire des voisins
        # Voisinage : Ajout d'au plus N nouveaux capteurs, N paramétrable
        while(delta_alg < MAX_TIME_alg and no_change_alg < MAX_NO_CHANGE_alg):

            # Amélioration de la solution courante

            # Initialisation de la meilleure solution locale
            best_local_solution = solution
            best_local_size = solution.get_size()

            # Step 1 : Amélioration déterministe
            improved = copy.deepcopy(solution)
            improved.improve()
            # Comparaison avec la meilleure solution locale
            if improved.get_size() < best_local_size:
                best_local_solution = improved
                best_local_size = improved.get_size()

            # Step 2 : Suite d'améliorations aléatoires (borne temporelle)
            # Variables pour conditions de fin
            time_init_loop = time.time()
            delta = 0
            no_change_loop = 0
            MAX_TIME_loop = 45
            MAX_NO_CHANGE_loop = 20

            # Parcours aléatoire des "voisins"
            # Voisinage : Amélioration
            while(delta < MAX_TIME_loop and no_change_loop < MAX_NO_CHANGE_loop):
                # Génération du "voisin" à partir de la solution courante
                improved = copy.deepcopy(solution)
                improved.improve_random()
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
            solution.add_random_capt(int(0.25*instance.size))
            delta_alg = time.time() - time_init_alg
        time2 = time.time()
        print((G,(R_CAPT,R_COM),best_size,time2-time1))
