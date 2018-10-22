import math

class Target:

    def __init__(self, i, j, rank):
        self.coordinates = (i,j)
        self.n = rank
        self.neighbors_capt = []
        self.neighbors_com = []

    def __str__(self):
        return "Target (" + str(self.coordinates[0]) + " , " + str(self.coordinates[1]) + ") " + str(self.neighbors_capt)

    def distance(self, target):
        (i,j) = self.coordinates
        (k,l) = target.coordinates
        return math.sqrt((i-k)**2+(j-l)**2)

    def setCapt(self, list_capt, list_count_capt):
        if list_capt[self.n] == 0:
            list_capt[self.n] = 1
            for rank in self.neighbors_capt:
                list_count_capt[rank] += 1
        else:
            list_capt[self.n] = 0
            for rank in self.neighbors_capt:
                list_count_capt[rank] += -1
