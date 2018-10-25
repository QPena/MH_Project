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
#instance.create_from_file("Instances\\captANOR225_9_20.dat")
#instance.create_from_file("Instances\\captANOR400_10_80.dat")
instance.create_from_file("Instances\\captANOR900_15_20.dat")
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



#print(solution.to_string())
print("length: " + str(solution.get_size()))

# Amélioration
time_nei, time_con = solution.improve()
#solution.improve_random()
#print(solution.to_string())

print("length: " + str(solution.get_size()))



time_improv = time.time()

print(str(solution.is_comm_path()))

time15 = time.time()

print(str(solution.is_comm_path2()))

time2 = time.time()





print("Construction : " + str(time_construc_grid-time1))
print("Voisins : " + str(time_neighbors-time_construc_grid))
print("Génération : " + str(time_random-time_neighbors))
print("Amélioration : " + str(time_improv-time_random))
print("dont Removability : " + str(time_nei))
print("dont Path : " + str(time_con))
print("Admissibilité 2 : " + str(time15-time_improv))
print("Admissibilité : " + str(time2-time15))
print("Total : " + str(time2-time1))

solution.to_plot()
#print(neighbors_capt)