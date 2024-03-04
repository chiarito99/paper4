import math
import numpy as np
import matplotlib.pyplot as plt
import createPath as cp
def calculate_polygon_area(vertices):
    n = len(vertices)
    area = 0.0
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i+1) % n]  # Lấy đỉnh kế tiếp (hoặc đỉnh đầu tiên nếu i là đỉnh cuối cùng)
        area += x1*y2 - x2*y1
    return abs(area) / 2.0
vertices = [[59, -40],[-10,-40],[-20, -79], [-63, 24], [-31, 61], [52, 26]]
area = calculate_polygon_area(vertices)


def getAngle(knee, hip, shoulder):
    ang = math.degrees(math.atan2(shoulder[1]-hip[1], shoulder[0]-hip[0]) - math.atan2(knee[1]-hip[1], knee[0]-hip[0]))
    return ang + 360 if ang < 0 else ang
def takeA(K):
    for i in range(len(K)-1):
        if i==len(K) - 2:
            print(getAngle(K[i],K[i+1],K[1]))
        else:
            print(getAngle(K[i],K[i+1],K[i+2]))


def checkangle(K):
    point_angle = []
    for i in range(len(K)-1):
        if i == len(K)-2:
            if getAngle(K[i],K[i+1],K[1]) > 180:
                point_angle.append(i+1)
        else:
            if getAngle(K[i],K[i+1],K[i+2]) > 180:
                point_angle.append(i+1)

    return point_angle



#pt duong thang
def line_eq(point_1, point_2):
    A = point_1[0]
    B = point_1[1]
    C = point_2[0]
    D = point_2[1]

    a = B - D
    b = C - A
    c = a * -A + b * -B
    return a, b, c

# tim diem giao
def find_intersect_point(points, index_center):
    index_angel = checkangle(points)
    point1 = points[index_center]
    # print("point1 = ", point1)
    point2 = points[index_center-1]
    # print("point2 = ", point2)
    a1, b1, c1 = line_eq(point1, point2)
    tow  = index_center + 1
    if index_center == len(points) - 1:
        tow = 0
    point2 = points[tow]
    # print("point21", point2)
    a2, b2, c2 = line_eq(point1, point2)
    no = []
    points.append(points[0])
    # print(a2, b2, c2)
    for i in range(len(points)-1):
        if(check_side([a1, b1, c1], points[i], points[i+1])):
            # if i == index_center - 1: continue
            a, b, c = line_eq(points[i], points[i+1])
            # print("point1x =", points[i])
            # print("point2x =", points[i+1])
            x = eq2_solve([a,b,c], [a1, b1, c1])
            # print("x1",x)
            print("Done x1")
            no.append(list(x))
        if(check_side([a2, b2, c2], points[i], points[i+1])):
            # if i == tow: continue
            a, b, c = line_eq(points[i], points[i+1])
            x = eq2_solve([a,b,c], [a2, b2, c2])
            # print("point1x =", points[i])
            # print("point2x =", points[i+1])
            # print("x2",x)
            print("Done x2")
            no.append(list(x))
        print("no", no)
    return no
def check_point_on_line(a, b, c, x, y):
    right_side = a * x + b * y + c
    if right_side == 0:
        return True
    else:
        return False
#kiem tra vi tri tuong doi
def check_side(paraline, point_1, point_2):
    check1 = point_1[0] * paraline[0] + point_1[1] * paraline[1] + paraline[2]
    check2 = point_2[0] * paraline[0] + point_2[1] * paraline[1] + paraline[2]
    # print("point_1", point_1)
    # print("point_2", point_2)
    # print("check1", check1)
    # print("check2", check2)
    if check1*check2 < 0:
        return True
    else:
        return False
    
def eq2_solve(para_1, para_2):
    a1 = para_1[0]
    b1 = para_1[1]
    c1 = para_1[2]
    a2 = para_2[0]
    b2 = para_2[1]
    c2 = para_2[2]

    A = [[a1, b1], [a2, b2]]
    B = [-c1, -c2]

    x = np.linalg.solve(A, B)

    return x

def sort_points(sub_points):
    # print("sub_points", sub_points)
    angle_vec = []
    new_sub_points = []
    new_sub_points.extend(sub_points)
    for i in range(len(sub_points)-1):
        #vector.append([sub_points[i+1][0] - sub_points[i][0], sub_points[i+1][1] - sub_points[i][1]])
        angle_vec.append( math.atan2(sub_points[i+1][1] - sub_points[0][1], sub_points[i+1][0] - sub_points[0][0]))
    if (max(angle_vec)>math.pi/2) and (min(angle_vec)<-math.pi/2):
        for i in range (len(angle_vec)):
            if angle_vec[i]<0:
                angle_vec[i] = angle_vec[i] + 2*math.pi
    for i in range(len(sub_points)-1):
        temp = angle_vec.index(max(angle_vec[i:]))
        # if(temp == max(angle_vec[i:])): continue
        angle_vec[i], angle_vec[temp] = angle_vec[temp], angle_vec[i]
        new_sub_points[i+1], new_sub_points[temp+1] = new_sub_points[temp+1], new_sub_points[i+1]
    if(len(new_sub_points) != len(sub_points)):
        print("error")
    # print("new_sub_points", new_sub_points)
    # print('angle_vec', angle_vec)
    # print("new_sub_points", new_sub_points)
    return new_sub_points
def sort_points1(points,sub,index_center, intersect_point):
    # print('sub',sub)
    sorted_point = []
    check = 0
    # sorted_point.append(intersect_point)

    # print("sorted",sorted_point)
    # print("index",index_center)
    point1 = points[index_center]
    point2 = points[index_center-1]
    
    a,b,c = line_eq(point1, point2)
    for i in range(1, len(points)-1):
        if  i == index_center - 1:
            continue
        a1, b1, c1 = line_eq(points[i], points[i+1])
        # print(eq2_solve([a,b,c], [a1,b1,c1]) )
        x = eq2_solve([a,b,c], [a1,b1,c1])
        if(intersect_point == x.tolist()):
            # print("before add 1",points)
            points.insert(i + 1, intersect_point)
            check = 1
            # print("after add 1",points)
            # print("success")
            break
    # print("check",check)
    if check == 0:
        # print("before add",points)
        points.insert(0,intersect_point)
        # print("after add ",points)
    sorted_point = sorted([x for x in sub if x in points], key=lambda x: points.index(x))
    # print("sorted_point", sorted_point)
    points.remove(intersect_point)
    return sorted_point
def take_sub_Points(points, center, intersect_point): #tim toa do diem cua 2 phan map
    sub_point1 = [center, intersect_point]

    sub_point2 = [center, intersect_point]
    index_angel = checkangle(points)
    special_point = []
    flag_point = []
    # tim dinh da giac thuoc duong thang chua center, intersect_point
    index = points.index(center)
    a, b, c = line_eq(center, intersect_point)
    tow = index + 1
    if(index == len(points) -1):
        tow = 0

    check =  a*points[tow][0] + b*points[tow][1] + c
    # print("check", check)
    if tow in index_angel:
        tow = tow + 1
    else:
        tow = index + 1
    if(check < 0.001):
        special_point = points[tow]
    else:
        special_point = points[index-1]
    index_special_point = points.index(special_point)
    new_points = []
    new_points.extend(points)
    
    new_points.remove(points[index_special_point])
    new_points.remove(points[index])
    # print("new_points", new_points)
    #find flag_point : ke cua special point khac center
    tow2 = index_special_point+1
    if(index_special_point == len(points) -1 ):
        tow2 = 0
    if(points[tow2] != center ):
        flag_point = points[tow2]
    elif(points[index_special_point-1] != center):
        flag_point = points[index_special_point-1]

    # print('flag_point', flag_point)
    # print('special_point', special_point)
    # #tim sub_point chua sap xep
    #
    temp1 = a * new_points[0][0] + b * new_points[0][1] + c
    sub_point1.append(new_points[0])
    # print('pp',new_points)
    flag  = 0
    if new_points[0] == flag_point:
        sub_point1.append(special_point)
        flag = 1
    for i in range(1, len(new_points) - 1):
        temp2 = a * new_points[i][0] + b * new_points[i][1] + c
        if (temp1 * temp2 > 0):
            sub_point1.append(new_points[i])
            if new_points[i] == flag_point and i != len(new_points) - 1:
                sub_point1.append(special_point)
                flag = 1
            # print('sb', new_points[i])
            # print('ss',sub_point1)
        else:
            sub_point2.append(new_points[i])
            if new_points[i] == flag_point and i != len(new_points) - 1:
                sub_point2.append(special_point)
                flag = 2
    #
    # print('sub1', sub_point1)
    # print('sub2', sub_point2)
    if not sub_point1 or not sub_point2:
        return None, None
    # sub_point1 = sort_points(sub_point1)
    # sub_point2 = sort_points(sub_point2)
    sub_point1 = sort_points1(points, sub_point1, index, intersect_point)
    sub_point2 = sort_points1(points, sub_point2, index,intersect_point)
    # print('sub_point22', sub_point22)
    # print("sub_point2", sub_point2)
    if (flag == 1):
        # print("center", center)
        sub_point1.remove(center)
    elif (flag == 2):
        # print("center", center)
        sub_point2.remove(center)
    

    # print('sub1', sub_point1)
    # print('sub2', sub_point2)
    return sub_point1, sub_point2
def plan (points):
    points.append(points[0])
    index = checkangle(points)
    print(index)
    if not index:
        print('function checkangle return None')
        return None, None
    if index[0] == len(points) - 1   :
        index = [0]
    del points[-1]
    center = points[index[0]]
    # print("center", center )
    
    inter_P = find_intersect_point(points, index[0])
    if(len(inter_P) < 2):
        sub_point1, sub_point2 = take_sub_Points(points, center, inter_P[0])
        return sub_point1, sub_point2
    # print(inter_P)
    sub_point1, sub_point2 = take_sub_Points(points, center, inter_P[0])
    sub_point3, sub_point4 = take_sub_Points(points, center, inter_P[1])
    if not sub_point1 or not sub_point3:
        print('function take_sub_Points return None')
        return None, None

    s1 = calculate_polygon_area(sub_point1)
    # print('s1', s1)
    s2 = calculate_polygon_area(sub_point2)
    # print('s2', s2)
    s3 = calculate_polygon_area(sub_point3)
    # print('s3', s3)
    s4 = calculate_polygon_area(sub_point4)
    # print('s4', s4)


    if(abs(s1-s2) > abs(s3-s4)):
        # print("get12")
        return sub_point1, sub_point2
    elif(abs(s1-s2) < abs(s3-s4)):
        # print("get34")
        return sub_point3, sub_point4
    else:
        print('Can not compare S')
        return None, None
result = []
def recursive(points, index = 0):
    a, b = plan(points)
    # if index == 0: 
    #     # plt.figure()
    #     if a:
    #         a.append(a[0])
    #         oxa,oya= zip(*a)
    #         plt.plot(oxa, oya )
    #     if b:
    #         b.append(b[0])
    #         oxb,oyb= zip(*b)
    #         plt.plot(oxb, oyb )
    #         return None
    if a and b:
        if len(a) < len(b):
            # print('a', a)
            # print('b', b)
            a.append(a[0])
            array = np.array(a)
            cp.planning(2,-1,array[:,0],array[:,1],[],0)
            result.append(a)
            # b.append(b[0])
            # print('b', b)
            # ox,oy= zip(*b)
            recursive(b,index+1)
            # plt.plot(ox,oy)
            # result.append(result_temp)
            cp.Find_intersect(a,-1)
        else:
            # print('a', a)
            # print('b', b)
            b.append(b[0])
            array = np.array(b)
            cp.planning(2,-1,array[:,0],array[:,1],[],0)
            result.append(b)
            # ox,oy= zip(*a)
            # plt.plot(ox,oy)
            recursive(a, index + 1 )
            # result.append(result_temp)
            cp.Find_intersect(b,-1)
        oxa,oya= zip(*a)
        plt.plot(oxa, oya )
        oxb,oyb= zip(*b)
        plt.plot(oxb, oyb )
    else:
        array = np.array(points)
        cp.planning(2,-1,array[:,0],array[:,1],[],0)
        oxa,oya= zip(*points)
        plt.plot(oxa, oya )
        # print('a', a)
        # print('b', b)
        result.append(points)
    return None

#non convex has a angle > 180
# K2 = [[59, -40],[-10,-40],[-20, -85], [-63, 24], [-31, 56], [52, 26]]
# K2 = [ [59, -40],[-10,-40],  [-63, 24],[-31, 56] , [52, 26],[-20,0]]  
# K2 = [ [59, -40],[-10,-40],  [-63, 24],[-31, 56] ,[-20,0], [52, 26]]
# K2 = [ [59, -40],[-10,-40],  [-63, 24],[- 20,0],[-31, 56] , [52, 26]]
# K2 = [ [59, -40],[-10,-40],[-20,0],  [-63, 24] ,[-31, 56], [20, 45], [47,60] , [52, 26]]
# K2 = [ [59, -40],[40, -20], [-10,-40], [-46,-30],[-36.5,-8], [-63, 24],[-60, 48],[-45,45],[-31, 56] ,  [52, 26]] #xbisme da sua
# K2 = [ [59, -40],[40, -20], [-10,-40], [-46,-30],[-36.5,-8], [-63, 24],[-60, 48],[-45,45],[-31, 56] ,  [52, 26]] #xbisme da sua3
# K2 = [ [59, -40],[40, -20], [-10,-40],  [-63, 24],[-60, 48],[-45,45],[-31, 56],[-3,45], [20,56] ,  [52, 26]] #xbisme da sua 1
# # K2 = [ [59, -40],[40, -20], [15, -30],[26, -39],[-10,-40],  [-63, 24],[-60, 48],[-45,45],[-31, 56],[52, 26]] #xbisme da sua 2
# # K2 = [ [59, -40],[40, -20], [15, -30],[26, -39],[-10,-40],  [-63, 24],[-62.04950495049505, 31.603960396039604],[-31, 56],[52, 26]] #xbisme da sua 2
# # K2 = [[56.191860465116285, -13.523255813953487],  [-10, -40], [-63, 24], [-62.04950495049505, 31.603960396039604], [-31, 56], [-3, 45], [20, 56], [52, 26] ]
# # K2 = [[56.191860465116285, -13.523255813953487],  [-10, -40], [-63, 24], [-62.04950495049505, 31.603960396039604], [-31, 56], [-3, 45], [20, 56], [52, 26] ]
# # # K2 = [ [0, 4],[3,-1],  [1, -1],[-2, -2] ]
# # # K2 = [[0, 0], [3, 2], [6, -3], [4,-3], [1, -4]]
# # K2 = [[0, -1], [-2, 1], [-1, 2], [-1, 3], [3, 1] ]
# # # K2 =[[-4, -4], [-6, 0], [-2, 4], [-8, 6], [5, 10], [10, 8], [8,2], [3, -4]]

# # print('K2', K2)
# plt.figure()
# points = K2
# recursive(points)
# # points = points.append(points[0])
# ox,oy= zip(*K2)
# print('poly1', result[0])
# print('poly2', result[1])
# print('poly3', result[2])
# print('poly4', result[2])
# ox1,oy1 = zip(*result[2])
# plt.plot(ox1, oy1,'-xk',label = 'range')
# plt.plot(ox, oy,'-xk',label = 'range')
# print('result', result)
plt.show()