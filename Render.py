import math
import pygame
import random
from numba import njit
import numpy as np

K = 3

toPrint = np.zeros((1280000, 5))

class Planet:
    def __init__(self, pos, charge, color):
        self.pos = pos
        self.charge = charge
        self.size = pow(abs(charge), 0.5) * K
        self.color = color

                    #(xPos,yPos),charge,(color)
Planets = [Planet([700, 200],  1000,  [255,0,0]),
           Planet([900, 250],  -70,   [255,255,0])]
           #Planet([600, 400],  100,  [0,255,0]),
           #Planet([1000, 400], 20,   [0,0,255]),
           #Planet([700, 550],  110,  [0,255,255]),
           #Planet([900, 600],  50,   [255,0,255])]

Positions = []
Charges = []
Sizes = []
Colors = []

for i in Planets:
    Positions.append(i.pos)
    Charges.append(i.charge)
    Sizes.append(i.size)
    Colors.append(i.color)

Positions = np.array(Positions, dtype=np.float64)
Charges = np.array(Charges, dtype=np.float64)
Sizes = np.array(Sizes, dtype=np.float64)
Colors = np.array(Colors, dtype=np.float64)

@njit
def particleLines(toPrint):
    for X in range(1600):
        if X % 10 == 0:
            print("x =", X, "/ 1600")
        for Y in range(800):
            x = X
            y = Y
            xVel = 0
            yVel = 0
            colored = False
            toPrint[(X*800)+Y, 0] = X
            toPrint[(X*800)+Y, 1] = Y
            while not colored:
                for i in range(len(Positions)):
                    dist = ((((Positions[i, 0] - x) ** 2) + ((Positions[i, 1] - y) ** 2)) ** 0.5)
                    if dist < Sizes[i]:
                        toPrint[(X*800)+Y, 2] = Colors[i, 0] * 0.5
                        toPrint[(X*800)+Y, 3] = Colors[i, 1] * 0.5
                        toPrint[(X*800)+Y, 4] = Colors[i, 2] * 0.5
                        colored = True
                    else:
                        accel = (Charges[i] * K) / (dist ** 2)
                        xVel += accel * (Positions[i, 0] - x) / (dist*10)
                        yVel += accel * (Positions[i, 1] - y) / (dist*10)
                xVel *= 0.99999
                yVel *= 0.99999
                x += xVel
                y += yVel

pygame.init()
screen = pygame.display.set_mode((1600,800))
pygame.display.set_caption("Charged Particles Render")
background = pygame.Surface((1600, 800))

Particles = []

particleLines(toPrint)
for i in toPrint:
    background.set_at((int(i[0]), int(i[1])), (int(i[2]), int(i[3]), int(i[4])))

for i in range(Positions.shape[0]):
    pygame.draw.circle(background, Colors[i].astype(int), Positions[i].astype(int), int(Sizes[i]))

#pygame.image.save(screen, "./save.png")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                Particles.append([event.pos[0], event.pos[1], 0, 0, True])
    
    screen.blit(background, (0,0))

    for p in reversed(range(len(Particles))):
        for i in range(len(Positions)):
            if Particles[p][4]:
                dist = ((((Positions[i][0] - Particles[p][0]) ** 2) + ((Positions[i][1] - Particles[p][1]) ** 2)) ** 0.5)
                pygame.draw.circle(screen, (0,0,0), (Particles[p][0], Particles[p][1]), 5)
                if dist < Sizes[i]:
                    Particles[p][4] = False
                else:
                    accel = (Charges[i] * K) / (dist ** 2)
                    Particles[p][2] += accel * (Positions[i][0] - Particles[p][0]) / (dist*10)
                    Particles[p][3] += accel * (Positions[i][1] - Particles[p][1]) / (dist*10)
        Particles[p][2] *= 0.99999
        Particles[p][3] *= 0.99999
        Particles[p][0] += Particles[p][2]
        Particles[p][1] += Particles[p][3]
        if not Particles[p][4]:
            Particles.pop(p)

    pygame.display.update()
pygame.quit()