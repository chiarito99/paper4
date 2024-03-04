from importlib.util import set_loader
from dubins_path_planner import *
from grid_based_sweep import *
import numpy as np
from sweep_line_has_bad_copy import getOpSweep
from shapely.geometry import LineString
from shapely.ops import unary_union

class Env1:
    def __init__(self ,xy_start,xy_end, resolution,path):
        # The range of the map
        self.x_start = xy_start[0]
        self.y_start = xy_start[1]
        self.x_end = xy_end[0]
        self.y_end = xy_end[1]
        self.resolution= resolution
        self.distance = 0

        path = np.array(path)
        for i in range(0,len(path)-1):
            a= path[i+1]-path[i]
            b = np.hypot(a[0],a[1])
            self.distance = self.distance + b
        self.point = path
        px = []
        py = []
        si = path.shape[0] - 1
        curvature = 2.0

        for i in range(si):
            if i == 0:
                start_x = path[i][0]
                start_y = path[i][1]
                start_yaw = 0
                end_x = path[i+1][0]  # [m]
                end_y = path[i+1][1]  # [m]
                end_yaw = np.arctan2(path[i+1][1]-path[i][1],path[i+1][0]-path[i][0])  # [rad]
            else:
                start_x = path[i][0]
                start_y = path[i][1]
                start_yaw = np.arctan2(path[i][1]-path[i-1][1],path[i][0]-path[i-1][0])
                end_x = path[i+1][0]  # [m]
                end_y = path[i+1][1]  # [m]
                end_yaw = np.arctan2(path[i+1][1]-path[i][1],path[i+1][0]-path[i][0])  # [rad]   

            path_x, path_y, path_yaw, mode, lengths = plan_dubins_path(start_x,
                                                               start_y,
                                                               start_yaw,
                                                               end_x,
                                                               end_y,
                                                               end_yaw,
                                                               curvature)
            for i in range(len(path_x)):
                px.append(path_x[i])
                py.append(path_y[i])

        # Desired trajectory
        self.traj = np.array([px, py])
        # self.ryaw = ryaw
        # self.rk=rk

        # Obstacle
        # self.obs = np.array([[20,30,2],
        #                      [-25,10,2],
        #                      [10,20,2]])
        
        # # Obstacle
        # self.obs = np.array([[100,100,0],
        #                      [-100,100,0],
        #                      [90,90,0]])

# if __name__ == "__main__":
#     # ox = [0.0, 50.0, 50.0, 0.0, 0.0]
#     # oy = [0.0, 0.0, 60.0, 60.0, 0.0]
#     resolution = 5
#     x_start = -20
#     y_start = -50
#     x_end = 10
#     y_end = 10
#     xystart =[x_start,y_start]
#     xyend = [x_end,y_end]

#     # M, Mshifted= getConvexPolygon(n_vertices,polygon_radius,rad_var,ang_var)
#     # K = M.tolist()
#     # print(K)
    
#     K = [[58.98295314305732, -40.46389776524755], [-19.5748849118947, -78.531936254165], [-62.674712335622026, 24.06481669719506], [-31.09947113556031, 61.08658069805723],[30,55.4],[52.20911077098446, 26.412130624396212]]
#     # K = [[-10, -40], [-36.28155339805825, -40.0], [-20, -79],[-10,-40]]
#     # K = [[200.0,200.0],[800.0,200.0],[800.0,700.0],[200.0,700.0],[200,200]]
#     # oy = [223.0, 28.0,19.0,4.0,0.0, 0.0,  119.0, 223.0]
#     # ox = [0.0, 50.0, 50.0, 0.0, 0.0]
#     # oy = [0.0, 0.0, 60.0, 60.0, 0.0]
#     altitude = 11
#     overlap = 0.3
#     path = getOpSweep(K, [x_start,y_start], [x_end,y_end],resolution)
#     env = Env1(xystart,xyend,resolution,path)

#     K.append(K[0])
#     ox, oy = zip(*K)
    
#     plt.figure()
#     plt.plot(ox, oy, '-xk', label='range')
#     plt.plot(env.traj[0,:], env.traj[1,:], '-b', label='reference')
#     plt.axis('scaled')
#     plt.show()

