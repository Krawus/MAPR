import rclpy
import time
from mapr_4_student.grid_map import GridMap


class BFS(GridMap):
    def __init__(self):
        super(BFS, self).__init__()
        self.queue = []
        self.current_point = ()
        self.i = 0
        rows, cols = (15, 15)
        self.prev = [[(0, 0) for i in range(15)] for j in range(15)]
        self.path = []
        


    def x_y_to_vec(self, point):
        return point[0] + point[1] * self.map.info.width

    def neighbours(self, point):
        
        neighboursArray = []

        tmpPoint = list(point)
        tmpPoint[1] -= 1

        if ((tmpPoint[0] >= 0) and (tmpPoint[1] >=0)):
            if (self.map.data[self.x_y_to_vec(tuple(tmpPoint))] < 50):
                neighboursArray.append(tuple(tmpPoint))

        tmpPoint = list(point)
        tmpPoint[0] -= 1

        if ((tmpPoint[0] >= 0) and (tmpPoint[1] >=0)):
            if (self.map.data[self.x_y_to_vec(tuple(tmpPoint))] < 50):
                neighboursArray.append(tuple(tmpPoint))
        
        tmpPoint = list(point)
        tmpPoint[1] += 1

        if ((tmpPoint[0] >= 0) and (tmpPoint[1] >=0)):
            if (self.map.data[self.x_y_to_vec(tuple(tmpPoint))] < 50):
                neighboursArray.append(tuple(tmpPoint))

        tmpPoint = list(point)
        tmpPoint[0] += 1

        if ((tmpPoint[0] >= 0) and (tmpPoint[1] >=0)):
            if (self.map.data[self.x_y_to_vec(tuple(tmpPoint))] < 50):
                neighboursArray.append(tuple(tmpPoint))


        return neighboursArray


    def search(self):

        if (self.i < 1):
            self.queue.append(self.start)
            # self.visited.append(self.start)

        # print(self.queue)

        if (len(self.queue) > 0):

            print(self.queue)
            self.map.data[self.x_y_to_vec(self.queue[0])] = 50

            if (self.queue[0] == self.end):
                print('finito')
                return True
            
            # print(self.queue[0])
            # self.path.append(self.queue[0])
            emptyneighbours = self.neighbours(self.queue[0])
            for n in emptyneighbours:
                if (n not in self.queue):
                    # print('prev to ', n[0], n[1], '|  is : ', self.queue[0])
                    self.prev[n[0]][n[1]] = self.queue[0]
                    self.queue.append(n)

            self.queue.pop(0)           
            
            
        self.i += 1
        return False
    
    def drawPath(self):
        print(self.prev)
        endpoint = self.end
        point = self.end
        print("START ", point)
        self.path.append(point)
        
        while point != self.start:
            
            x = point[0]
            y = point[1]
            point = self.prev[x][y]
            self.path.append(point)
            print(point)
            


def main(args=None):
    rclpy.init(args=args)
    bfs = BFS()
    while not bfs.data_received():
        bfs.get_logger().info("Waiting for data...")
        rclpy.spin_once(bfs)
        time.sleep(0.5)

    bfs.get_logger().info("Start graph searching!")
    # bfs.publish_visited()
    time.sleep(1)

    res = False
    while res == False:
        bfs.publish_visited()
        res = bfs.search()

    bfs.drawPath()
    bfs.publish_path(bfs.path)
    

if __name__ == '__main__':
    main()
