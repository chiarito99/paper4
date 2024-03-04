import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg
class Find_intersect():

    def __init__(self, resolution, move_dr):
        self.resolution = resolution
        self.move_dr = move_dr
        # other para
        self.x_ori = 0
        self.y_ori = 0
        self.th = 0
        self.new_resolution = resolution
        self.scale_para = 1
        self.limit_ratio = 1000

    #calibarate xo yo, resolution
    def cali_para(self, ox, oy):
        cali_ox = []
        cali_oy = []
        # print(ox)
        # print(oy)

        if (max(oy) - min(oy)) / self.resolution > self.limit_ratio :
            self.resolution = round(self.resolution)
            return ox, oy
        else:
            if (self.resolution) % 1 == 0 :
                self.scale_para = 1
                return ox, oy
            elif (self.resolution)*10 % 1 ==0:
                self.scale_para = 10
                self.resolution = self.resolution*10
                cali_ox = list(np.array(ox)*10)
                cali_oy = list(np.array(oy)*10)
            else:
                self.scale_para = 100
                self.resolution = round(self.resolution*100)
                cali_ox = list(np.array(ox)*100)
                cali_oy = list(np.array(oy)*100)
        # print(self.scale_para)
        # print(self.resolution)
        # print(cali_ox)
        # print(cali_oy)
        return cali_ox, cali_oy

    #tim cac toa do cat voi resolution = 0.5
    def find_intersect1(self,ox, oy):
        x_grid =[]
        y_grid =[]
        # print(cox)
        # print(coy)
        # print(self.resolution)
        for k in range(len(ox) - 1):
            xA = ox[k]
            yA = oy[k]
            xB = ox[k + 1]
            yB = oy[k + 1]
            # truong hop y=a
            if oy[k] == oy[k + 1]:
                x = list(np.arange(min(ox[k], ox[k + 1]), max(ox[k], ox[k + 1]), 0.5))
                y = list(oy[k] * np.ones(len(x)))
                x_grid.extend(x)
                y_grid.extend(y)
                continue
            for i in np.arange(int(min(oy[k], oy[k + 1])), int(max(oy[k], oy[k + 1]))+1, 0.5):
                x = (i - yA) * (xB - xA) / (yB - yA) + xA
                x_grid.append(x)
                y_grid.append(i)
        # print(x_grid)
        # print(y_grid)
        return x_grid, y_grid
    # tìm các tọa do cat voi resolution bat ky
    def find_intersect(self, ox, oy, pRx, pRy, len_landmark):#pRy: y_coordinate of intersect point that Robot passed
        #chuan hoa PrY
        if pRy != None:
            pRy = np.ceil((pRy+0.0001)*2)/2
        else:
            pRy = 0

        x_intersect = []
        y_intersect = []
        x_grid, y_grid = self.find_intersect1(ox, oy)
        offset = -self.resolution / 2
        begin = self.resolution / 2
        ed = int(max(oy))
        # print(x_grid)
        # print(y_grid)
        # print(offset)

        for i in np.arange(begin, ed, 0.5):
            if (i < pRy and len_landmark > 0):
                continue
            if (i + offset) % self.resolution == 0:
                if self.move_dr == 1:
                    x_intersect.extend([min(self.take_element(x_grid, self.indexes(y_grid, i))),
                                        max(self.take_element(x_grid, self.indexes(y_grid, i)))])
                    y_intersect.extend([i, i])
                else:
                    x_intersect.extend([max(self.take_element(x_grid, self.indexes(y_grid, i))),
                                        min(self.take_element(x_grid, self.indexes(y_grid, i)))])
                    y_intersect.extend([i, i])
                cali_i = i
            #change resolution if need
            if i == pRy and len_landmark > 0: #:
                offset = - pRy
                if (self.move_dr == 1 and len_landmark % 2 == 0 and len_landmark % 4 != 0) or (self.move_dr != 1 and len_landmark % 2 == 0 and len_landmark % 4 == 0):
                    x_intersect = []
                    y_intersect = []
                    self.move_dr = 1
                    continue
                elif (self.move_dr == 1 and len_landmark % 2 == 0 and len_landmark % 4 == 0) or (self.move_dr != 1 and len_landmark % 2 == 0 and len_landmark % 4 != 0):
                    x_intersect = []
                    y_intersect = []
                    self.move_dr = -1
                    continue
                elif (self.move_dr == 1 and len_landmark % 2 == 1 and (len_landmark-1)%4==0 ) or (self.move_dr == -1 and len_landmark % 2 == 1 and (len_landmark-1) % 4 != 0):
                    x_intersect.extend([min(self.take_element(x_grid, self.indexes(y_grid, i))),
                                        max(self.take_element(x_grid, self.indexes(y_grid, i)))])
                    y_intersect.extend([i, i])
                    self.move_dr = 1
                    continue
                elif (self.move_dr == 1 and len_landmark % 2 == 1 and (len_landmark-1)%4!=0 ) or (self.move_dr == -1 and len_landmark % 2 == 1 and (len_landmark-1) % 4 == 0):
                    x_intersect.extend([max(self.take_element(x_grid, self.indexes(y_grid, i))),
                                        min(self.take_element(x_grid, self.indexes(y_grid, i)))])
                    y_intersect.extend([i, i])
                    self.move_dr = -1
                    continue

            if (i + offset) % self.resolution == self.resolution - 0.5:
                self.swap_moving_direction()
        #print(y_intersect)
        return x_intersect, y_intersect
    # ham lay cac index cua list co gia tri ref
    def indexes(self, list, ref):
        result = []
        for i in range(len(list)):
            if list[i] == ref:
                result.append(i)
        return result
    # hàm lấy các gái trị trong list với index trong index_list
    def take_element(self, list, index_list):
        return [list[i] for i in index_list]
    def swap_moving_direction(self):
        self.move_dr *= -1
    def convert(self, ox, oy,base_point,next_base_point): #convert points of grap
        #calibarate
        ox, oy = self.cali_para(ox, oy)

        self.find_base(ox, oy,base_point,next_base_point)
        cx = []
        cy = []
        # print("th",self.th)
        T_matrix = np.matrix([[np.cos(self.th), -np.sin(self.th), 0, self.x_ori],
                              [np.sin(self.th),  np.cos(self.th), 0, self.y_ori],
                              [0,                0,               1,          0],
                              [0,                0,               0,          1]])
        T_matrix = linalg.inv(T_matrix)
        for i in range(len(ox)):
            temp = T_matrix * np.matrix([[ox[i]],
                                        [oy[i]],
                                        [0],
                                        [1]])
            cx.append(float(np.squeeze(np.array(temp[0]))))
            cy.append(float(np.squeeze(np.array(temp[1]))))
        # hiệu chỉnh co trường hợp xoay và dich xong vẫn có các tọa độ âm(x_point=0)
        min_x = 0
        min_y = 0
        # if min(cx) < 0:
        min_x = min(cx)
        # self.x_ori = self.x_ori + min(cx)
        # print("x_ori1", self.x_ori)
        cx = list(np.array(cx) - min(cx))
    # if min(cy) < 0:
        min_y = min(cy)
        # self.y_ori = self.y_ori + min(cy)
        # print("y_ori1", self.y_ori)
        cy = list(np.array(cy) - min(cy))
        return cx, cy,min_x, min_y
    def convert_point(self, p_R): #convert other point
        if len(p_R) == 0:
            return None, None
        #cali point

        p_R[0] = p_R[0]*self.scale_para
        p_R[1] = p_R[1]*self.scale_para
        T_matrix = np.matrix([[np.cos(self.th), -np.sin(self.th), 0, self.x_ori],
                              [np.sin(self.th), np.cos(self.th), 0, self.y_ori],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1]])
        T_matrix = linalg.inv(T_matrix)
        temp = T_matrix * np.matrix([[p_R[0]],
                                     [p_R[1]],
                                     [0],
                                     [1]])
        cx = (float(np.squeeze(np.array(temp[0]))))
        cy = (float(np.squeeze(np.array(temp[1]))))

        return  cx, cy
    def in_convert(self,cx, cy,min_x,min_y):
     # Dịch và xoay, scale lại hình
        in_cx = []
        in_cy = []
        # print("x_ori2", self.x_ori)
        # print("y_ori2", self.y_ori)
        # print("th2", self.th)
        T_matrix = np.matrix([[np.cos(self.th), -np.sin(self.th), 0,      self.x_ori],
                              [np.sin(self.th),  np.cos(self.th), 0,      self.y_ori],
                              [0,                0,               1,          0],
                              [0,                0,               0,          1]])
        for i in range(len(cx)):
            temp = T_matrix * np.array([[cx[i] + min_x],
                                        [cy[i] + min_y],
                                        [0],
                                        [1]])
            in_cx.append(float(np.squeeze(np.array(temp[0])/self.scale_para)))
            in_cy.append(float(np.squeeze(np.array(temp[1])/self.scale_para)))
        # print("in_cx", in_cx)
        # print("in_cy", in_cy)
        return in_cx, in_cy
    # hàm tìm vector base,o_ori,y_ori góc xoay

    def find_base(self, ox, oy,base_point,next_base_point):
        x_new = [base_point[0], next_base_point[0]]
        y_new = [base_point[1], next_base_point[1]]
        x_vector = []
        y_vector = []
        for i in range(len(ox)-1):
            x_vector = [ox[i+1], ox[i]]
            y_vector = [oy[i+1], oy[i]]
            if are_parallel(x_vector,y_vector, x_new, y_new):
                self.x_ori = ox[i]
                self.y_ori = oy[i]
                self.th = np.arctan2(oy[i+1] - oy[i], ox[i+1] - ox[i])
                break
    
    def change_resolution(self, resolution):
        self.resolution = round(resolution*self.scale_para)
def are_parallel(x1, y1, x2, y2):
    # Tính toán vectơ hướng của mỗi đoạn thẳng
    dx1 = x1[1] - x1[0]
    dy1 = y1[1] - y1[0]
    dx2 = x2[1] - x2[0]
    dy2 = y2[1] - y2[0]

    # Kiểm tra xem hai vectơ có cùng hướng hay không
    cross_product = dx1 * dy2 - dy1 * dx2
    if abs(cross_product) < 1e-9:  # Sử dụng một ngưỡng rất nhỏ để xem xét sai số
        return True
    else:
        return False
def planning(resolution, dr_move, xo, yo, p_R, len_landmark,base_point,next_base_point):# p_R :current_position_Robot_leader, best is intersect point
    emp = Find_intersect(resolution, dr_move)
    ox, oy,min_x,min_y = emp.convert(xo, yo,base_point,next_base_point)
    pRx, pRy = emp.convert_point(p_R)
    cx, cy = emp.find_intersect(ox, oy, pRx, pRy, len_landmark)
    # print("cx", cx)
    # print("cy", cy) 
    x, y = emp.in_convert(cx, cy,min_x,min_y)
    # plt.plot(ox,oy)
    # plt.plot(x,y)
    # plt.show()
    return x, y

# [[59, -40], [52, 26], [-31, 61], [-63, 24], [-36.28155339805825, -40.0], [59, -40]]
# xo = [40, 56.191860465116285, 59, 40]
# yo = [-20, -13.523255813953487, -40, -20]
# x, y = planning(7.5, 1, xo, yo, [-47.302912621359226,-13.6 ], 0)
# print(x)
# print(y)
# plt.plot(xo, yo)
# plt.plot(x,y)
# plt.show()
# xo = [0, 150, 90,  60,  -20,  0 ]
# yo = [0,  0, 100, 120, 60,    0 ]
# # # xo = [-10, - 36.28, - 20, - 10]
# # # yo = [-40, - 40, - 79, - 40]
# a = [25, 51]
# x, y = planning(7.5, 1, xo, yo, [],0)
# plt.subplot(1,2,1)
# plt.plot(xo, yo)
# plt.plot(x, y)
# print(x)
# plt.plot([25], [51], marker="o", markersize=5, markeredgecolor="red", markerfacecolor="green")
# # plt.subplot(1,2,2)
# # x2, y2 = planning(7.5, 1, xo, yo,a ,6)
# # plt.plot(xo, yo)
# # plt.plot([25],[51], marker="o", markersize=5, markeredgecolor="red", markerfacecolor="green")
# # plt.plot(x2, y2)
# # # plt.plot(x, y)
# plt.show()