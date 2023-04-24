import pygame
import numpy as np
from math import *

WHITE = (255, 255, 255)
ORANGE = (255,127,80)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
FUCHSIA = (255, 0, 255)
YELLOW = (255, 255, 0)

WIDTH, HEIGHT = 900, 900
pygame.display.set_caption("3D Cube")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
MS = 0.5
MS2 = 0.2
AS = 0.05
AS2 = 0.02
ZS = 1.1
ZS2 = 1.04
scale = 50
distanceZ = 10
number_of_figures = 4
center = [WIDTH/2, HEIGHT/2]

figures = [[] for i in range(number_of_figures)]
figures[0].append(np.matrix([ 1,     1,     -9]))
figures[0].append(np.matrix([ 3,     1,     -9]))
figures[0].append(np.matrix([ 3,     3,     -9]))
figures[0].append(np.matrix([ 1,     3,     -9]))
figures[0].append(np.matrix([ 1,     1,    -11]))
figures[0].append(np.matrix([ 3,     1,    -11]))
figures[0].append(np.matrix([ 3,     3,    -11]))
figures[0].append(np.matrix([ 1,     3,    -11]))

figures[1].append(np.matrix([-3,     1,     -9]))
figures[1].append(np.matrix([-1,     1,     -9]))
figures[1].append(np.matrix([-1,     3,     -9]))
figures[1].append(np.matrix([-3,     3,     -9]))
figures[1].append(np.matrix([-3,     1,    -11]))
figures[1].append(np.matrix([-1,     1,    -11]))
figures[1].append(np.matrix([-1,     3,    -11]))
figures[1].append(np.matrix([-3,     3,    -11]))

figures[2].append(np.matrix([-3,    -3,     -9]))
figures[2].append(np.matrix([-1,    -3,     -9]))
figures[2].append(np.matrix([-1,    -1,     -9]))
figures[2].append(np.matrix([-3,    -1,     -9]))
figures[2].append(np.matrix([-3,    -3,    -11]))
figures[2].append(np.matrix([-1,    -3,    -11]))
figures[2].append(np.matrix([-1,    -1,    -11]))
figures[2].append(np.matrix([-3,    -1,    -11]))

figures[3].append(np.matrix([ 1,    -3,     -9]))
figures[3].append(np.matrix([ 3,    -3,     -9]))
figures[3].append(np.matrix([ 3,    -1,     -9]))
figures[3].append(np.matrix([ 1,    -1,     -9]))
figures[3].append(np.matrix([ 1,    -3,    -11]))
figures[3].append(np.matrix([ 3,    -3,    -11]))
figures[3].append(np.matrix([ 3,    -1,    -11]))
figures[3].append(np.matrix([ 1,    -1,    -11]))

faces = [[] for i in range(number_of_figures)]
for i in range(number_of_figures):
    faces[i].append([True, RED,     0, 1, 5, 4])
    faces[i].append([True, GREEN,   0, 1, 2, 3])
    faces[i].append([True, BLUE,    1, 2, 6, 5])
    faces[i].append([True, CYAN,    2, 3, 7, 6])
    faces[i].append([True, FUCHSIA, 3, 0, 4, 7])
    faces[i].append([True, YELLOW,  4, 5, 6, 7])

lines = [[] for i in range(number_of_figures)]
for i in range(number_of_figures):
    lines[i].append([0, 1])
    lines[i].append([1, 2])
    lines[i].append([2, 3])
    lines[i].append([3, 0])
    lines[i].append([4, 5])
    lines[i].append([5, 6])
    lines[i].append([6, 7])
    lines[i].append([7, 4])
    lines[i].append([0, 4])
    lines[i].append([1, 5])
    lines[i].append([2, 6])
    lines[i].append([3, 7])

for i in range(number_of_figures):
    projected_points = [[
        [n, n] for n in range(len(figures[i]))
    ]for j in range(number_of_figures)]

figure_center = [[] for i in range(len(figures))]
order = [0]*len(figures)
ordered = [0]*len(figures)
for i in range (len(figures)):
    order[i]=i
distance = [0]*len(figures)

def calculate_figure_center(i):
    x, y, z = 0, 0, 0
    for j in range(len(figures[i])):
        x += figures[i][j].A[0][0]
        y += figures[i][j].A[1][0]
        z += figures[i][j].A[2][0]
    figure_center[i] = [x/len(figures[i]), y/len(figures[i]), z/len(figures[i])]

def specify_order():
    for i in range(len(figure_center)):
        distance[i] = pow(pow(figure_center[i][0], 2) + pow(figure_center[i][1], 2) + pow(figure_center[i][2], 2), 1/3)
    localordered = [order for _, order in sorted(zip(distance, order))]
    localordered.reverse()
    global ordered
    ordered = localordered.copy()

def connect_points(figure, i, j):
    pygame.draw.line(
        screen, WHITE, (projected_points[figure][i][0], projected_points[figure][i][1]), (projected_points[figure][j][0], projected_points[figure][j][1]))

def check_face_orienatation():
    for i in range (number_of_figures):
        calculate_figure_center(i)
        for j in range (len(faces[i])):
            point1 = faces[i][j][2]
            point2 = faces[i][j][3]
            point3 = faces[i][j][4]
            x=figures[i][point1].A[0][0]
            y=figures[i][point1].A[1][0]
            z=figures[i][point1].A[2][0]
            v1 = [-x, -y, -z]
            v2 = calculate_normal_vector(i, point1, point2, point3)
            if (np.dot(v1, v2) > 0):
                faces[i][j][0]=True
            else:
                faces[i][j][0]=False
            # print("Figure number:", i, "Face number:", j, "Face orientation:", faces[i][j][4])

def calculate_normal_vector(i, point1, point2, point3):
    A = []
    B = []
    C = []
    for j in range (3):
        A.append(figures[i][point1].A[j][0])
        B.append(figures[i][point2].A[j][0])
        C.append(figures[i][point3].A[j][0])
    AB = np.subtract(B, A)
    AC = np.subtract(C, A)
    normal_vector = np.cross(AB, AC)
    center = figure_center[i]
    if np.dot(normal_vector, np.subtract(center, A)) > 0:
        normal_vector *= -1
    return normal_vector

def check_face_visibility(i, j):
    if (faces[i][j][0] == True):
        return True

def check_point_visibility(i, j):
    for k in range (len(faces[i])):                     # iterujemy po kazdej scianie danej figury
        if (faces[i][k][0]==True):                      # jesli sciana jest widoczna
            for l in range (2, len(faces[i][k]), 1):    # to jesli ktorykolwiek z jej wierzcholkow jest szukanym
                if faces[i][k][l] == j:                 
                    return True                         # to go malujemy
    return False

def check_line_visibility(i, j):
    if check_point_visibility(i, lines[i][j][0]) == True and check_point_visibility(i, lines[i][j][1]) == True:
        return True
    else:
        return False

def init_act():
    for i in range(len(figures)):
        for j in range(len(figures[i])):
            figures[i][j] = figures[i][j].reshape(3, 1)
            figures[i][j] = np.r_[figures[i][j], np.matrix([1])]

def translate(moveX, moveY, moveZ):
    translation = np.matrix([
        [1,             0,              0,              moveX],
        [0,             1,              0,              moveY],
        [0,             0,              1,              moveZ],
        [0,             0,              0,              1],
    ])
    for i in range(len(figures)):
        for j in range(len(figures[i])):
            translated = figures[i][j]
            translated = np.dot(translation, translated)
            if(translated[3][0]!=0):
                translated /= translated[3][0] #normalizacja
            figures[i][j]=translated

def rotateX(angleX):
    rotation_x = np.matrix([
        [1,             0,              0,              0],
        [0,             cos(angleX),    -sin(angleX),   0],
        [0,             sin(angleX),    cos(angleX),    0],
        [0,             0,              0,              1],
    ])
    for i in range(len(figures)):
        for j in range(len(figures[i])):
            rotated2d = figures[i][j]
            rotated2d = np.dot(rotation_x, rotated2d)
            figures[i][j]=rotated2d

def rotateY(angleY):
    rotation_y = np.matrix([
        [cos(angleY),   0,              sin(angleY),    0],
        [0,             1,              0,              0],
        [-sin(angleY),  0,              cos(angleY),    0],
        [0,             0,              0,              1],
    ])
    for i in range(len(figures)):
        for j in range(len(figures[i])):
            rotated2d = figures[i][j]
            rotated2d = np.dot(rotation_y, rotated2d)
            figures[i][j]=rotated2d       

def rotateZ(angleZ):
    rotation_z = np.matrix([
        [cos(angleZ),   -sin(angleZ),   0,              0],
        [sin(angleZ),   cos(angleZ),    0,              0],
        [0,             0,              1,              0],
        [0,             0,              0,              1],
    ])
    for i in range(len(figures)):
        for j in range(len(figures[i])):
            rotated2d = figures[i][j]
            rotated2d = np.dot(rotation_z, rotated2d)
            figures[i][j]=rotated2d

def draw_polygons():
    for i in ordered:
        for j in range(len(faces[i])):
            if (check_face_visibility(i, j) == True):
                tabXY = [[0]*2 for k in range (2, len(faces[i][j]))]
                for k in range (2, len(faces[i][j]), 1):
                    tabXY[k-2][0]=(projected_points[i][faces[i][j][k]][0])
                    tabXY[k-2][1]=(projected_points[i][faces[i][j][k]][1])
                pygame.draw.polygon(screen, faces[i][j][1], tabXY)

def draw_lines():
     for i in ordered:
        for j in range(len(lines[i])):
            if (check_line_visibility(i, j) == True):
                pygame.draw.line(screen, WHITE, (projected_points[i][lines[i][j][0]][0], projected_points[i][lines[i][j][0]][1]),
                                  (projected_points[i][lines[i][j][1]][0], projected_points[i][lines[i][j][1]][1]))

def draw_points():
     for i in ordered:
        for j in range(len(figures[i])):
            if (check_point_visibility(i, j) == True):
                [x, y] = projected_points[i][j]
                pygame.draw.circle(screen, ORANGE, (x,y), scale/10)

def act():
    for i in range(len(figures)):
        for j in range(len(figures[i])):
            projected2d = np.dot(projection_matrix, figures[i][j])
            if(projected2d[3][0]!=0):
                projected2d /= projected2d[3][0] #normalizacja
            x=int(projected2d[0][0]/projected2d[2][0]*distanceZ*scale+center[0])
            y=int(center[1]-projected2d[1][0]/projected2d[2][0]*distanceZ*scale)
            projected_points[i][j] = [x, y]
    
init_act()
clock = pygame.time.Clock()
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

            ### Movement ###
            if event.key == pygame.K_w:
                translate(0, 0, MS)
            if event.key == pygame.K_s:
                translate(0, 0, -MS)
            if event.key == pygame.K_a:
                translate(-MS, 0, 0)
            if event.key == pygame.K_d:
                translate(MS, 0, 0)
            if event.key == pygame.K_q:
                translate(0, MS, 0)
            if event.key == pygame.K_e:
                translate(0, -MS, 0)
            
            ### Rotation ###
            if event.key == pygame.K_r:
                rotateZ(AS)
            if event.key == pygame.K_y:
                rotateZ(-AS)
            if event.key == pygame.K_t:
                rotateX(AS)
            if event.key == pygame.K_g:
                rotateX(-AS)
            if event.key == pygame.K_f:
                rotateY(AS)
            if event.key == pygame.K_h:
                rotateY(-AS)

            ### Zoom ###
            if event.key == pygame.K_z:
                scale*=ZS
            if event.key == pygame.K_x:
                scale/=ZS

        if pygame.key.get_pressed()[pygame.K_w] == True:
            translate(0, 0, MS2)
        if pygame.key.get_pressed()[pygame.K_s] == True:
            translate(0, 0, -MS2)
        if pygame.key.get_pressed()[pygame.K_a] == True:
            translate(-MS2, 0, 0)
        if pygame.key.get_pressed()[pygame.K_d] == True:
            translate(MS2, 0, 0)
        if pygame.key.get_pressed()[pygame.K_q] == True:
            translate(0, MS2, 0)
        if pygame.key.get_pressed()[pygame.K_e] == True:
            translate(0, -MS2, 0)
            
        if pygame.key.get_pressed()[pygame.K_r] == True:
            rotateZ(AS2)
        if pygame.key.get_pressed()[pygame.K_y] == True:
            rotateZ(-AS2)
        if pygame.key.get_pressed()[pygame.K_t] == True:
            rotateX(AS2)
        if pygame.key.get_pressed()[pygame.K_g] == True:
            rotateX(-AS2)
        if pygame.key.get_pressed()[pygame.K_f] == True:
            rotateY(AS2)
        if pygame.key.get_pressed()[pygame.K_h] == True:
            rotateY(-AS2)

        if pygame.key.get_pressed()[pygame.K_z] == True:
            scale*=ZS2
        if pygame.key.get_pressed()[pygame.K_x] == True:
            scale/=ZS2

    screen.fill(BLACK)

    projection_matrix = np.matrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, float(1/distanceZ), 0],
    ])

    act()
    check_face_orienatation()
    specify_order()
    draw_polygons()
    draw_lines()
    draw_points()

    pygame.display.update()