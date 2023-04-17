import pygame
import numpy as np
from math import *

WHITE = (255, 255, 255)
ORANGE = (255,127,80)
BLACK = (0, 0, 0)

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

for i in range(number_of_figures):
    projected_points = [[
        [n, n] for n in range(len(figures[i]))
    ]for j in range(number_of_figures)]

def connect_points(figure, i, j):
    pygame.draw.line(
        screen, WHITE, (projected_points[figure][i][0], projected_points[figure][i][1]), (projected_points[figure][j][0], projected_points[figure][j][1]))

def init_act():
    for i in range(len(figures)):
        for j in range(len(figures[i])):
            figures[i][j] = figures[i][j].reshape(3, 1)
            figures[i][j] = np.r_[figures[i][j], np.matrix([1])]

init_act()

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

def act():
    num = 0
    fig = 0
    for i in range(len(figures)):
        for j in range(len(figures[i])):
            projected2d = np.dot(projection_matrix, figures[i][j])
            if(projected2d[3][0]!=0):
                projected2d /= projected2d[3][0] #normalizacja
            x=int(projected2d[0][0]/projected2d[2][0]*distanceZ*scale+center[0])
            y=int(center[1]-projected2d[1][0]/projected2d[2][0]*distanceZ*scale)
            projected_points[fig][num] = [x, y]
            pygame.draw.circle(screen, ORANGE, (x,y), scale/10)
            num+=1
        num = 0
        fig+=1

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

    connect_points(0, 0, 1)
    connect_points(0, 1, 2)
    connect_points(0, 2, 3)
    connect_points(0, 3, 0)
    connect_points(0, 4, 5)
    connect_points(0, 5, 6)
    connect_points(0, 6, 7)
    connect_points(0, 7, 4)
    connect_points(0, 0, 4)
    connect_points(0, 1, 5)
    connect_points(0, 2, 6)
    connect_points(0, 3, 7)

    connect_points(1, 0, 1)
    connect_points(1, 1, 2)
    connect_points(1, 2, 3)
    connect_points(1, 3, 0)
    connect_points(1, 4, 5)
    connect_points(1, 5, 6)
    connect_points(1, 6, 7)
    connect_points(1, 7, 4)
    connect_points(1, 0, 4)
    connect_points(1, 1, 5)
    connect_points(1, 2, 6)
    connect_points(1, 3, 7)

    connect_points(2, 0, 1)
    connect_points(2, 1, 2)
    connect_points(2, 2, 3)
    connect_points(2, 3, 0)
    connect_points(2, 4, 5)
    connect_points(2, 5, 6)
    connect_points(2, 6, 7)
    connect_points(2, 7, 4)
    connect_points(2, 0, 4)
    connect_points(2, 1, 5)
    connect_points(2, 2, 6)
    connect_points(2, 3, 7)

    connect_points(3, 0, 1)
    connect_points(3, 1, 2)
    connect_points(3, 2, 3)
    connect_points(3, 3, 0)
    connect_points(3, 4, 5)
    connect_points(3, 5, 6)
    connect_points(3, 6, 7)
    connect_points(3, 7, 4)
    connect_points(3, 0, 4)
    connect_points(3, 1, 5)
    connect_points(3, 2, 6)
    connect_points(3, 3, 7)

    pygame.display.update()