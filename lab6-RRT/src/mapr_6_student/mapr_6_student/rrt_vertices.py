import rclpy
import time
from mapr_6_student.grid_map import GridMap
import numpy as np
from random import randrange
from math import sqrt

np.random.seed(444)


class RRT(GridMap):
    def __init__(self):
        super(RRT, self).__init__()
        self.step = 0.1

    def check_if_valid(self, a, b):
        """
        Checks if the segment connecting a and b lies in the free space.
        :param a: point in 2D
        :param b: point in 2D
        :return: boolean
        """
        v = b - a
        u = v / np.linalg.norm(v)

        dist = sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)

        distances = np.linspace(0.0, dist)
        in_free_space = True
        for d in distances:
            pt = a + d*u
            pt = pt * 10
            pt = np.floor(pt)
            # print("###########")
            # print("FLOATING POINT: ", pt)
            # print("checking [{}][{}]".format(int(pt[1]), int(pt[0])))
            if self.map[int(pt[1])][int(pt[0])] == 100:
                return False
            
        return in_free_space

    def random_point(self):
        """
        Draws random point in 2D
        :return: point in 2D
        """

        x = np.random.random() * self.width
        y = np.random.random() * self.height 
        

        return np.array([x, y])

    def find_closest(self, pos):
        """
        Finds the closest vertex in the graph to the pos argument

        :param pos: point id 2D
        :return: vertex from graph in 2D closest to the pos
        """
        x = pos[0]
        y = pos[1]

        closest = pos
        dist = 100000
    
        for key in self.parent:
            
            key_dist = sqrt((key[0] - x)**2 + (key[1] - y)**2)

            if (key_dist < dist):
                dist = key_dist
                closest = key
            
            if self.parent[key] == None:
                continue

            parent_dist = sqrt((self.parent[key][0] - x)**2 + (self.parent[key][1] - y)**2)

            if (parent_dist < dist):
                dist = parent_dist
                closest = self.parent[key]
        
        return closest

    def new_pt(self, closest, rand):
        """
        Finds the point on the segment connecting closest with pt, which lies self.step from the closest (vertex in graph)

        :param pt: point in 2D
        :param closest: vertex in the tree (point in 2D)
        :return: point in 2D
        """
        v = rand - closest
        u = v / np.linalg.norm(v)

        pt = closest + self.step * u
        pt = np.round(pt, decimals=2)

        return pt

    def search(self):
        """
        RRT search algorithm for start point self.start and desired state self.end.
        Saves the search tree in the self.parent dictionary, with key value pairs representing segments
        (key is the child vertex, and value is its parent vertex).
        Uses self.publish_search() and self.publish_path(path) to publish the search tree and the final path respectively.
        """
        path_found = False
        print("START: ", self.start)
        print("END: ", self.end)
        print("RESOLUTION: ", self.resolution)
        print("######################")
        self.parent[self.start] = None
        
        found_endpoint = False
        while (found_endpoint == False):

            rand_point = self.random_point()
            # print("RANDOM POINT: ", rand_point)

            closest_point = self.find_closest(rand_point)
            # print("CLOSEST POINT: ", closest_point)

            new_point = self.new_pt(closest_point, rand_point)
            # print("NEW POINT: ", new_point)

            if self.check_if_valid(closest_point, new_point):
                self.parent[tuple(new_point)] = closest_point
                self.publish_search()
                
                if self.check_if_valid(new_point, self.end):
                    print("endpoint found!")
                    self.parent[tuple(self.end)] = new_point 
                    self.publish_search()

                    found_endpoint = True
       
        if found_endpoint == True:

            start = self.end
            point = self.end
            path = []
            path.append(point)
            while tuple(point) != self.start:
                point = self.parent[tuple(point)]
                path.append(point)

            self.publish_path(path)


def main(args=None):
    rclpy.init(args=args)
    rrt = RRT()
    while not rrt.data_received():
        rrt.get_logger().info("Waiting for data...")
        rclpy.spin_once(rrt)
        time.sleep(0.5)

    rrt.get_logger().info("Start graph searching!")
    time.sleep(1)
    rrt.search()


if __name__ == '__main__':
    main()
