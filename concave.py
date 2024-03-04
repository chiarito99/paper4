import math
from shapely import Polygon, LineString, Point, MultiLineString, GeometryCollection
import matplotlib.pyplot as plt
import geopandas as gpd
import createPath as cp
import numpy as np
# Hàm check cùng phía hay khác phía giữa 2 điểm
def check_line(i1, i2, poly, edge):
    p = line_sort(edge, poly)
    if len(p) > 1:
        for i in range(len(poly)):
            if p[1] == poly[i]:
                ind = i
        if i1 < ind <= i2:
            return True
    return False


# Sắp xếp các điểm từ bé đến lớn
def sort(index, points):
    for i in range(len(index)):
        for j in range(i + 1, len(index)):
            if index[i] > index[j]:
                swap = index[i]
                index[i] = index[j]
                index[j] = swap

                temp = points[i]
                points[i] = points[j]
                points[j] = temp
    return index, points

def CrossProduct(A):
    X1 = (A[1][0] - A[0][0])
    Y1 = (A[1][1] - A[0][1])
    X2 = (A[2][0] - A[0][0])
    Y2 = (A[2][1] - A[0][1])
    return X1 * Y2 - Y1 * X2


# Hàm lấy tọa độ điểm lõm
def isConcave(poly):
    prev = 0
    concave_point = list()
    # print(len(poly))
    d = CrossProduct((poly[len(poly) - 1], poly[0], poly[1]))

    for i in range(len(poly)):
        temp = (poly[(i - 1) % len(poly)], poly[i], poly[(i + 1) % len(poly)])
        curr = CrossProduct(temp)
        if curr != 0:
            if curr * prev < 0:
                if d > 0:
                    concave_point.append(poly[i])
            else:
                if d < 0:
                    concave_point.append(poly[i])
                prev = curr

    return concave_point


# Hàm kiểm tra điểm thuộc cạnh:
def check_points_in_line(check_point, poly):
    for i in range(len(poly)):
        v1 = poly[i]
        v2 = poly[(i + 1) % len(poly)]
        delta_x = v2[0] - v1[0]
        delta_y = v2[1] - v1[1]

        if delta_x == 0 and v1[0] == check_point[0] and (v1[1] - check_point[1]) * (v2[1] - check_point[1]) < 0:
            return i
        elif delta_y == 0 and v1[1] == check_point[1] and (v1[0] - check_point[0]) * (v2[0] - check_point[0]) < 0:
            return i
        elif delta_x != 0 and delta_y != 0 and (v1[0] - check_point[0]) * (v2[0] - check_point[0]) < 0:
            slope = delta_y / delta_x
            if abs(slope * check_point[0] - check_point[1] + v1[1] - slope * v1[0]) < 1e-8:
                return i
    return -1


# Giao điểm đường thẳng qua điểm lõm với đa giác và
# xác định điểm thuộc đoạn thẳng khi đường thẳng qua điểm lõm cắt đa giác
def get_points_in_side(concave, edge, poly):
    _poly = Polygon(poly)
    # print(edge)
    minx, miny, maxx, maxy = _poly.bounds
    N = len(poly)

    v1 = poly[edge]
    v2 = poly[(edge + 1) % N]
    delta_x = v2[0] - v1[0]
    delta_y = v2[1] - v1[1]
    if delta_x == 0:
        line = LineString([(v1[0], maxy), (v1[0], miny)])
    elif delta_y == 0:
        line = LineString([(maxx, v1[1]), (minx, v1[1])])
    elif delta_x != 0 and delta_y != 0:
        slope = delta_y / delta_x
        x_maxy = concave[0] - (concave[1] - maxy) / slope
        x_miny = concave[0] - (concave[1] - miny) / slope
        line = LineString([(x_maxy, maxy), (x_miny, miny)])

    lines = line.intersection(_poly)
    # print("lines", lines)
    _list = list()
    #plt.plot(*line.xy)

    if type(lines) is LineString:
        _list.append(lines.coords[0])
        _list.append(lines.coords[1])
    elif type(lines) is MultiLineString:
        p = list(lines.geoms)
        for i in range(len(lines.geoms)):
            _list.append(p[i].coords[0])
            _list.append(p[i].coords[1])
    elif type(lines) is GeometryCollection:
        p = list(lines.geoms)
        _list.append(p[0].coords[0])
        _list.append(p[0].coords[1])
        _list.append(p[1].coords[0])

    # Xoá các điểm gần đỉnh
    index = list()
    for i in range(len(_list)):
        for j in range(N):
            if abs(_list[i][0] - poly[j][0]) < 1e-8 and abs(_list[i][1] - poly[j][1]) < 1e-8:
                index.append(i)
    for i in range(len(index)):
        _list.pop(index[i] - i)

    # Loại các điểm thuộc cạnh base
    for l in _list:
        if check_points_in_line(l, poly) == edge:
            _list.pop(_list.index(l))

    # Thêm giá trị p_decomp biểu thị vị trí
    p_decomp = list()
    for i in _list:
        if check_points_in_line(i, poly) != -1:
            p_decomp.append(check_points_in_line(i, poly))

    # Hàm thêm đỉnh và đỉnh lõm:
    _list.append(concave)
    for i in range(len(poly)):
        if concave == poly[i]:
            p_decomp.append(i)
    for i in range(len(poly)):
        if poly[i] != concave:
            temp = (concave, _list[0], poly[i])
            if abs(CrossProduct(temp)) < 1e-8:
                _list.append(poly[i])
                p_decomp.append(i)

    # Sắp xếp theo thứ tự từ bé đến lớn
    sort(p_decomp, _list)
    # Xoa cac diem trung lap trong list
    index = list()
    for i in range(len(p_decomp)):
        for j in range(i + 1, len(p_decomp)):
            if p_decomp[i] == p_decomp[j]:
                if _list[i] != _list[j] and _list[i] == poly[p_decomp[i]]:
                    if len(index) > 0 and index[len(index) - 1] == j:
                        index.pop(len(index) - 1)
                    index.append(j)
                else:
                    if len(index) > 0 and index[len(index) - 1] == i:
                        index.pop(len(index) - 1)
                    index.append(i)
    for i in range(len(index)):
        p_decomp.pop(index[i] - i)
        _list.pop(index[i] - i)

    # Loại điểm đối đỉnh:
    inde = -1
    for i in range(len(p_decomp) - 1):
        if check_line(p_decomp[i], p_decomp[i + 1], poly, edge) is True:
            inde = i
    for i in range(len(_list)):
        if _list[i] == concave:
            ind = i
    if inde > 0 and len(p_decomp) > 3:
        if ind > inde:
            for i in range(0, inde + 1):
                _list.pop(0)
                p_decomp.pop(0)
        else:
            for i in range(0, len(_list) - inde+1):
                _list.pop(len(_list) - 1)
                p_decomp.pop(len(_list) - 1)

    # print(_list, p_decomp)
    #for i in _list:
    #    plt.scatter(i[0], i[1])
    return _list, p_decomp


# Sắp xếp các đoạn thẳng đi qua điểm lõm
def line_sort(edge, poly):
    v1 = poly[edge]
    v2 = poly[(edge + 1) % len(poly)]
    delta_x = v2[0] - v1[0]
    delta_y = v2[1] - v1[1]

    concave_points = isConcave(poly)
 
    p = list()
    for i in range(len(concave_points)):
        if delta_x == 0:
            p.append(concave_points[i][1])
        elif delta_y == 0:
            p.append(concave_points[i][0])
        elif delta_x != 0 and delta_y != 0:
            slope = delta_y / delta_x
            p.append(concave_points[i][0] - concave_points[i][1] / slope)

    sort(p, concave_points)
    # print("concave", concave_points)
    return concave_points


# Ham chia
def decomp(concave_points, edge, poly, list_poly):
    concave = concave_points[0]
    concave_points.remove(concave)

    p, p_number = get_points_in_side(concave, edge, poly)
    index = list()
    if len(concave_points) > 0:
        for i in range(len(p)):
            if p[i] == concave_points[0]:
                index.append(i)
        if len(index) > 0:
            concave_points.pop(0)

    N = len(poly)
    n = len(p_number)
    t2 = list()
    t4 = list()
    for i in range(n):
        t1 = list()
        t3 = list()

        first_p = (p_number[i] + 1) % N
        second_p = p_number[(i + 1) % n]
        if p[i] != poly[first_p]:
            t1.append(p[i])

        if first_p > second_p:
            for j in range(first_p, N):
                t1.append(poly[j])
            for j in range(second_p + 1):
                t1.append(poly[j])
        else:
            for j in range(first_p, second_p + 1):
                t1.append(poly[j])

        if p[(i + 1) % n] != poly[second_p]:
            t1.append(p[(i + 1) % n])

        if len(t1) > 2:
            if len(isConcave(t1)) != 0:
                for t in t1:
                    t2.append(t)
                edge = len(t2) - 1
            elif len(isConcave(t1)) == 0:
                for t in t1:
                    t3.append(t)
                t4.append(t3)

    if len(concave_points) == 0 and len(t4) == 3:
        list_poly.append(t4[2])
        list_poly.append(t4[0])
        list_poly.append(t4[1])
    else:
        for i in range(len(t4)):
            list_poly.append(t4[len(t4) - 1 - i])

    if len(concave_points) > 0:
        #print(t2)
        return decomp(concave_points, edge, t2, list_poly)
    else:
        return list_poly
def getAngle(knee, hip, shoulder):
    ang = math.degrees(math.atan2(shoulder[1]-hip[1], shoulder[0]-hip[0]) - math.atan2(knee[1]-hip[1], knee[0]-hip[0]))
    return ang + 360 if ang < 0 else ang
def get_edge(poly):
    if not isConcave(poly):
        return None
    concave_points = isConcave(poly)
    edge = poly.index(concave_points[0])
    min_angel = getAngle(poly[edge-1],poly[edge],poly[edge+1])
    for i in range(len(poly) - 1):
        # print("angel",getAngle(poly[i-1],poly[i],poly[i+1]))
        if poly[i] in concave_points:
            if getAngle(poly[i-1],poly[i],poly[i+1]) < min_angel:
                edge = i
    # print("end",min_angel)
    # print(edge)
    return edge
def swap_pos(list_point):
    for i in range(0,len(list_point),2):
        if i >= len(list_point)-1:
            return list_point
        list_point[i],list_point[i+1] = list_point[i+1],list_point[i]
    return list_point
def closest_point(point, points):
    if not points:
        return True
    point1 = points[0]
    point2 = points[1]
    if np.linalg.norm(np.array(point) - np.array(point1)) < np.linalg.norm(np.array(point) - np.array(point2)):
        return True
    return False
def get_path( points,resolution,dr_move):
    edge = get_edge(points)
    path = []
    point1 = points[edge]
    if edge == len(points) - 1:
        next_edge = 0
    else: next_edge = edge + 1
    point2 = points[next_edge]
    points.append(points[0])
    array = np.array(points)
    x,y = cp.planning(resolution,dr_move,array[:,0],array[:,1],[],0,point1, point2)
    for j in range(len(x)):
        path.extend([[x[j],y[j]]])
    return path
if __name__ == '__main__':
    # points = [(7, 9), (3, 8.64), (1.55, 5.78), (3.88, 6.12), (3.32, 5.55), (4.25, 3.78), (5.34, 4.55), (8.47, 3.23), (8, 6), (9, 8)]
    # points = [(8, 9), (3, 8.64), (3.5, 7.5), (1.55, 7), (3.88, 6.12)]
    # points = [(0.45, 0.75),  (5.58, 1.78), (7.45, 3.21), (6.5, 3.5),
    #           (4.75, 6.15), (4.32, 5.94), (3.75, 4.55), (2.45, 6.44), (1.55, 5.45)]
    points = [(3.03, 9.35), (4.03, 3.19), (6.53, 4.5), (11.01, 2.47), (15.15, 3.73), (11.75, 4.89), (15.61, 7.01)]
    # points = [(-5.19, 1.82), (-6.57, 0.26), (-2.39, -1.56), (2.63, -0.32), (0.07, 2.2), (2.59, 3.66), (-1.13, 3.72),
    #          (-3.53, 6.78), (-6.23, 3.98)]
    # points = [(-3.24, 6.20), (-4.85, 3), (-6.97, 3.93), (-4.90, 1.17), (-5.99, -0.70), (-2,0.6),
    #          (-2.35, 3.46), (1.08, 2.75)]
    # points = [(-2.80, 8.89), (-4.46, 6.57), (-7.70, 5.58), (-4.68, 3.93),
    #          (-1.29, 3.86), (1.55, 6.25), (-1.71, 6.55)]
    
   

    ## Get path with recursive
    # edge = get_edge(points)
    # list_points = []
    # list_poly = list()
    # path = []
    # point1 = points[edge]
    # if edge == len(points) - 1:
    #     next_edge = 0
    # else: next_edge = edge + 1
    # point2 = points[next_edge]
    # concave_points = line_sort(edge, points)
    # a = decomp(concave_points, edge, points, list_poly)
    # for i in a:
    #     array = []
    #     p = Polygon(i)
    #     x, y = p.exterior.xy
    #     for j in range(len(x)):
    #         array.extend([[x[j],y[j]]])
    #     list_points.append(array)
    #     # plt.plot(*p.exterior.xy, 'b')
    # for i in range(len(list_points)):
    #     list_path = []
    #     array = np.array(list_points[i])
    #     x,y = cp.planning(0.7,-1,array[:,0],array[:,1],[],0,point1, point2)
    #     for j in range(len(x)):
    #         list_path.extend([[x[j],y[j]]])
    #     if i == 0:
    #         list_path.reverse() 
    #         if path:
    #             if not closest_point(path[-1],list_path):
    #                 list_path = swap_pos(list_path)
    #     path.extend(list_path)

    ## Get path for base
    path = get_path(points,0.7,-1)
    points.append(points[0])
    ox2,oy2 = zip(*points)
    plt.plot(ox2,oy2)
    x0,y0 = zip(*path)
    plt.plot(x0,y0)
    plt.plot(x0[0],y0[0],"-xk")
    plt.show()