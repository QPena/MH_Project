import math
import random

import time

from instance import Instance

class Solution:

    def __init__(self, instance):
        self.instance = instance
        self.list_capt = [0 for x in range(self.instance.size)]
        self.list_count_capt = [0 for x in range(self.instance.size)]

    def get_size(self):
        return sum([1 for t in self.list_capt if t == 1])

    def to_string(self):
        s = ""
        for i in range(self.instance.size):
            if(self.instance.isGrid and i%self.instance.grid_size == 0):
                s += "\n"
            s += str(self.list_capt[i]) + "(" + str(self.list_count_capt[i]) + ")  "
        return s

    def to_plot(self):
        s = "clf\n"
        circles = "theta=0:0.1:2*%pi;\n"
        circles_capt = circles
        circles_com = circles
        x_capt = []
        y_capt = []
        x_targ = []
        y_targ = []
        for i in range(self.instance.size):
            if self.list_capt[i] == 1:
                x_capt.append(self.instance.get_target(i).coordinates[0])
                y_capt.append(self.instance.get_target(i).coordinates[1])
            else:
                x_targ.append(self.instance.get_target(i).coordinates[0])
                y_targ.append(self.instance.get_target(i).coordinates[1])
        
        for i in range(len(x_capt)):
            if i%100 == 0:
                if i > 0:
                    s += x + "],[" + y + "], style=[-1,7])\n"
                x = ""
                y = ""
                s += "plot2d(["
            x += str(x_capt[i]) + ","
            circles_capt += "x = " + str(x_capt[i]) + '+' + str(self.instance.R_CAPT) + "*cos(theta);\n"
            circles_com +=  "x = " + str(x_capt[i]) + '+' + str(self.instance.R_COM) + "*cos(theta);\n"
            y += str(y_capt[i]) + ","
            circles_capt += "y = " + str(y_capt[i]) + '+' + str(self.instance.R_CAPT) + "*sin(theta);\n"
            circles_com += "y = " + str(y_capt[i]) + '+' + str(self.instance.R_COM) + "*sin(theta);\n"
            circles_capt += "plot2d(x,y)\n"
            circles_com += "plot2d(x,y)\n"

        s += x + "],[" + y + "], style=[-1,7])\n"

        c = s + circles_com

        for i in range(len(x_targ)):
            if i%100==0:
                if i > 0:
                    s += x + "],[" + y + "], style=[-2,12])\n"
                x = ""
                y = ""
                s+= "plot2d(["
            x += str(x_targ[i]) + ","
            y += str(y_targ[i]) + ","

        s += x + "],[" + y + "], style=[-2,12])\n"
        s += circles_capt

        with open("plot_sol.sci",'w') as file:
            file.write(s)

        with open("plot_capt.sci", "w") as file:
            file.write(c)


    def set_capt(self, rank):
        if self.list_capt[rank] == 0:
            self.list_capt[rank] = 1
            for neighbor in self.instance.get_target(rank).get_neighbors_capt():
                self.list_count_capt[neighbor] += 1
        else:
            self.list_capt[rank] = 0
            for neighbor in self.instance.get_target(rank).get_neighbors_capt():
                self.list_count_capt[neighbor] += -1

    def add_random_capt(self, nb):
        while nb>0 and self.get_size() < self.instance.size:
            target = random.randrange(1,self.instance.size)
            if self.list_capt[target] == 0:
                self.set_capt(target)
            nb -=1


    def generate_random_capt(self):
        #for i in range(self.instance.size):
        #    if random.random() < 0.4:
        #        self.instance.get_target(i).setCapt(self.list_capt, self.list_count_capt)
        while sum([1 for t in self.list_count_capt if t == 0]) > 0 or not self.is_comm_path():
           self.set_capt(random.randrange(1,self.instance.size))

    def generate_covering_com_solution(self):
        def add_neighbors(rank):
            for nei in self.instance.get_target(rank).get_neighbors_com():
                if nei !=0 and nei not in neighbors and self.list_capt[nei] == 0:
                    neighbors.add(nei)
            neighbors.remove(rank)

        neighbors = {0}
        add_neighbors(0)
        while sum([1 for t in self.list_count_capt if t == 0]) > 0:
            maxi = [1, 5, 13, 29, 49, 81, 113, 149, 197, 253, 317, 377, 441]
            best_next = (-1,0)
            for neighbor in neighbors:
                if self.list_capt[neighbor] == 1:
                    continue
                xx = sum([1 for n in self.instance.get_target(neighbor).get_neighbors_capt() if self.list_capt[n]==0])
                if xx > best_next[1]:
                    best_next = (neighbor, xx)
                    #if xx == maxi[R_COM] - 2:
                    #    break;
            #self.instance.get_target(best_next[0]).setCapt(self.list_capt, self.list_count_capt)
            self.set_capt(best_next[0])

            if(best_next[0] == -1): break
            add_neighbors(best_next[0])

    def improve(self):
        time_1 = 0
        time_2 = 0
        for t in range(1, self.instance.size):
            if self.list_capt[t] == 0:
                continue
            removable = False
            if self.list_count_capt[t] > 0:
                time_init = time.time()
                removable = True
                for n in self.instance.get_target(t).get_neighbors_capt():
                    if self.list_capt[n] == 0 and self.list_count_capt[n] < 2:
                    #if self.list_count_capt[n] < 2:
                        removable = False
                        break;
            time_inter = time.time()
            time_1 += time_inter - time_init
            if removable:
                self.set_capt(t)
                if not self.is_comm_path2():
                    self.set_capt(t)
            time_out = time.time()
            time_2 += time_out - time_inter
        return time_1, time_2

    def improve_random(self):
        capts = [x for x in range(self.instance.size) if self.list_capt[x]==1]
        while len(capts) > 0:
            t = capts[random.randrange(len(capts))]
            removable = False
            if self.list_count_capt[t] > 0:
                removable = True
                for n in self.instance.get_target(t).get_neighbors_capt():
                    if self.list_capt[n] == 0 and self.list_count_capt[n] < 2:
                    #if self.list_count_capt[n] < 2:
                        removable = False
                        break;
            if removable:
                self.set_capt(t)
                if not self.is_comm_path2():
                    self.set_capt(t)
            capts.remove(t)


    def is_comm_path(self):
        path = [0]
        capts = [x for x in range(self.instance.size) if self.list_capt[x]==1]
        for i in path:
            for neighbor in self.instance.get_target(i).get_neighbors_com():
                if self.list_capt[neighbor] == 1 and not neighbor in path:
                    path.append(neighbor)
            if(len(path) == len(capts) + 1):
                return True
        return False

    def is_comm_path2(self):
        path = [0]
        capts = {x for x in range(self.instance.size) if self.list_capt[x]==1}
        for i in path:
            neighbors = [x for x in self.instance.get_target(i).get_neighbors_com() \
                            if x in capts]
            path += neighbors
            capts = capts.difference(neighbors)
            if(len(capts) == 0):
                return True
        return False