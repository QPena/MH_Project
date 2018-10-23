import time
import copy

from instance import Instance
from solution import Solution

GRID_SIZE = 20
R_CAPT = 2
R_COM = 3

instance = Instance(R_CAPT, R_COM)

time1 = time.time()

#instance.create_grid(GRID_SIZE)
instance.create_from_file("Instances\\captANOR225_9_20.dat")
#instance.create_from_file("Instances\\captANOR400_10_80.dat")
#instance.create_from_file("Instances\\captANOR1500_15_100.dat")
#instance.create_from_file("Instances\\captANOR1500_21_500.dat")

time_construc_grid = time.time()

instance.fill_neighbors()

# print("Targets :")
# for target in instance.get_targets():
#     print(target)


time_neighbors = time.time()


# generate_random_capt(list_capt, list_count_capt)
solution = Solution(instance)
solution.generate_covering_com_solution()
#solution.generate_random_capt() # WARNING : do not use on big instances 


time_random = time.time()

time_init_alg = time.time()
delta_alg = 0

best_solution = solution
best_size = solution.get_size()

while(delta_alg < 120):

    #print(solution.to_string())
    print("length: " + str(solution.get_size()))

    # Amélioration

    best_local_solution = solution
    best_local_size = solution.get_size()

    # Step 1 : Amélioration déterministe (pour données temps ; à supprimer)
    improved = copy.deepcopy(solution)
    time_nei, time_con = improved.improve()
    #solution.improve_random()
    #print(solution.to_string())
    if improved.get_size() < best_local_size:
        best_local_solution = improved
        best_local_size = improved.get_size()

    print("length: " + str(best_local_size))

    # Step 2 : Suite d'améliorations aléatoires (borne temporelle)
    time_init_loop = time.time()
    delta = 0
    while(delta < 10):
        improved = copy.deepcopy(solution)
        improved.improve_random()
        if improved.get_size() < best_local_size:
            best_local_solution = improved
            best_local_size = improved.get_size()
        # print("length: " + str(improved.get_size()))
        delta = time.time() - time_init_loop

    print("best local length: " + str(best_local_size))
    if best_local_size < best_size:
        best_solution = best_local_solution
        best_size = best_local_size
    print("new best global best" + str(best_size) + "\n")

    solution = copy.deepcopy(best_solution)
    solution.add_random_capt(100)
    delta_alg = time.time() - time_init_alg



time_improv = time.time()

print(str(best_solution.is_comm_path()))

time2 = time.time()





print("Construction : " + str(time_construc_grid-time1))
print("Voisins : " + str(time_neighbors-time_construc_grid))
print("Génération : " + str(time_random-time_neighbors))
print("Amélioration : " + str(time_improv-time_random))
print("dont Removability : " + str(time_nei))
print("dont Path : " + str(time_con))
print("Admissibilité : " + str(time2-time_improv))
print("Total : " + str(time2-time1))

best_solution.to_plot()
#print(neighbors_capt)