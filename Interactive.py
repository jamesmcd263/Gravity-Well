import math
import pygame
import random
from numba import njit
import numpy as np
import os
import pathlib

K = 3

Positions = [[500, 600], [1100, 600], [800, 300]]

Charges = [50, 50, 50]

Sizes = [pow(abs(Charges[0]), 0.5) * K, pow(abs(Charges[1]), 0.5) * K, pow(abs(Charges[2]), 0.5) * K]

pygame.init()

screen = pygame.display.set_mode((1600,800))

pygame.display.set_caption("Charged Particles Render")

Particles = []

img = pygame.image.load("OneDrive\Desktop\Coding\Python\ChargedRender\WellFieldPre.png")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                Particles.append([event.pos[0], event.pos[1], 0, 0, True])

    screen.blit(img, (0,0))

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