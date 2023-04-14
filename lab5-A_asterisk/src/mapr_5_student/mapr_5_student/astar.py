import rclpy
import time
from mapr_5_student.grid_map import GridMap
import heapq as pq
from math import sqrt


class ASTAR(GridMap):
    def __init__(self):
        super(ASTAR, self).__init__('astar_node')
        self.g_and_prev = dict()
        self.to_visit = []
        self.i = 0 
        self.path = []

    def x_y_to_vec(self, point):
        return point[0] + point[1] * self.map.info.width

    def heuristics(self, pos):

        #MANHATTAN
        # distance = abs(pos[0] - self.end[0]) + abs(pos[1] - self.end[1])

        #EUK
        # distance = sqrt((pos[0] - self.end[0])**2 + (pos[1] - self.end[1])**2)

        #CHEBYSHEV
        distance = max(abs(pos[0] - self.end[0]),  abs(pos[1] - self.end[1]))
        
        return distance
        

    def search(self):
        if self.i == 0:
            self.to_visit.append(self.start)
            self.g_and_prev[self.start] = [0, self.start]
            self.map.data[self.x_y_to_vec(self.to_visit[0])] = 50
            self.i += 1
            

        while len(self.to_visit) > 0:

            #searching node with lowest F
            tmp_min = 100
            q_curr = ()
            for x in range(len(self.to_visit)):
                tmp = self.heuristics(self.to_visit[x]) + self.g_and_prev[self.to_visit[x]][0]   # f = (h + g)
                if tmp < tmp_min:
                    tmp_min = tmp
                    q_curr = self.to_visit[x]
            
            self.to_visit.remove(q_curr)

            if q_curr == self.end:
                print("found")
                break
            else:
                print("searching...")
                self.map.data[self.x_y_to_vec(q_curr)] = 50

            x, y = q_curr
            neighbours = [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]
            for n in neighbours:
                        if (self.map.data[self.x_y_to_vec(n)] != 100) and (n not in self.to_visit):
                             if n not in self.g_and_prev:
                                  self.g_and_prev[n] = [self.g_and_prev[q_curr][0] + 1, q_curr]
                                  self.to_visit.append(n)
                             else:
                                  f = self.heuristics(n) + self.g_and_prev[q_curr][0] + 1
                                  if f < self.heuristics(n) + self.g_and_prev[n][0]:
                                       self.g_and_prev[n] = [self.g_and_prev[q_curr][0] + 1, q_curr]
                                       self.to_visit.append(n)
 
            self.publish_visited()

    def draw_path(self):
        endpoint = self.end
        point = self.end
        self.path.append(point)
        while point != self.start:
            x = point[0]
            y = point[1]
            point = self.g_and_prev[(x , y)][1]
            self.path.append(point)
        
        # print(self.path)
        self.publish_path(self.path)
         


def main(args=None):
    rclpy.init(args=args)
    astar = ASTAR()
    while not astar.data_received():
        astar.get_logger().info("Waiting for data...")
        rclpy.spin_once(astar)
        time.sleep(0.5)

    astar.get_logger().info("Start graph searching!")
    astar.publish_visited()
    time.sleep(1)
    astar.search()
    astar.draw_path()

if __name__ == '__main__':
    main()