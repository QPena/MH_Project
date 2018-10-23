from target import Target
import numpy as np
class Instance :

    def __init__(self, R_CAPT, R_COM):
        self.targets = []
        self.isGrid = False
        self.grid_size = 0
        self.R_COM = R_COM
        self.R_CAPT = R_CAPT
        self.size = 0

    def get_targets(self):
        return self.targets

    def get_target(self, i):
        return self.targets[i]

    def create_grid(self, grid_size):
        self.grid_size = grid_size
        self.isGrid = True
        self.size = grid_size**2
        for i in range(grid_size):
            for j in range(grid_size):
                self.targets.append(Target(i,j, len(self.targets)))

    def create_from_file(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                data = line.split()
                self.targets.append(Target(float(data[1]), float(data[2]), int(data[0])))
                self.size += 1

    def fill_neighbors(self):
        for target in self.get_targets():
            for j in range(target.n+1,len(self.get_targets())):
                neighbor = self.get_target(j)
                if target.distance(neighbor) <= self.R_CAPT:
                    target.neighbors_capt.append(j)
                    #target.neighbors_com.append(j)
                    neighbor.neighbors_capt.append(target.n)
                    #neighbor.neighbors_com.append(target.n)
                elif target.distance(neighbor) <= self.R_COM:
                    target.neighbors_com.append(j)
                    neighbor.neighbors_com.append(target.n)

