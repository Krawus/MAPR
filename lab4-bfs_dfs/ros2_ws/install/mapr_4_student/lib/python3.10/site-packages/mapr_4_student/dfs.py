import rclpy
import time
from mapr_4_student.grid_map import GridMap


class DFS(GridMap):
    def __init__(self):
        super(DFS, self).__init__()
        self.stos = []
        self.i = 0
    
    def x_y_to_vec(self, point):
        return point[0] + point[1] * self.map.info.width
    
    def empty_neighbour(self, point):

        originalPoint = list(point)

        tmpPoint = list(point)
        tmpPoint[1] -= 1

        if ((tmpPoint[0] >= 0) or (tmpPoint[1] >=0)):
            if self.map.data[self.x_y_to_vec(tuple(tmpPoint))] < 50:
                return tuple(tmpPoint)
        
        tmpPoint = list(point)
        tmpPoint[0] -= 1

        if ((tmpPoint[0] >= 0) or (tmpPoint[1] >=0)):
            if self.map.data[self.x_y_to_vec(tuple(tmpPoint))] < 50:
                return tuple(tmpPoint)
            
        tmpPoint = list(point)
        tmpPoint[1] += 1

        if ((tmpPoint[0] >= 0) or (tmpPoint[1] >=0)):
            if self.map.data[self.x_y_to_vec(tuple(tmpPoint))] < 50:
                return tuple(tmpPoint)
            
        tmpPoint = list(point)
        tmpPoint[0] += 1

        if ((tmpPoint[0] >= 0) or (tmpPoint[1] >=0)):
            if self.map.data[self.x_y_to_vec(tuple(tmpPoint))] < 50:
                return tuple(tmpPoint)
        
        print('empty!')
        return []
    

    def search(self):

        if self.i < 1:
            self.stos.append(self.start)
            print(self.stos[-1])

        print(self.stos[-1])

        if len(self.stos) > 0:
            self.map.data[self.x_y_to_vec(self.stos[-1])] = 50

            if self.stos[-1] == self.end:
                print("here")
                return True
            
            empty_nei = self.empty_neighbour(self.stos[-1])

            if len(empty_nei) > 0:
                self.stos.append(empty_nei)
            else:
                self.stos.pop()

            self.i += 1
            return False


def main(args=None):
    rclpy.init(args=args)
    dfs = DFS()
    while not dfs.data_received():
        dfs.get_logger().info("Waiting for data...")
        rclpy.spin_once(dfs)
        time.sleep(0.5)

    dfs.get_logger().info("Start graph searching!")
    
    time.sleep(1)
    res = False
    while res == False:
        dfs.publish_visited()
        res = dfs.search()

if __name__ == '__main__':
    main()
