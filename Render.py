import math
import pygame
import random
from numba import njit
import numpy as np

K = 3
drag = 0.99999999
scaleTimeSpan = 1000
scaled = True

toPrint = np.zeros((1280000, 3))
rightClick = False

class Planet:
    def __init__(self, pos, charge, color):
        self.pos = pos
        self.charge = charge
        self.size = pow(abs(charge), 0.5) * K
        self.color = color

                #([xPos,yPos], mass, [color]
Planets = [
           Planet([800, 300],  200,  [255,0,0]),
           #Planet([1000, 500],  80,   [255,255,0]),
           Planet([600, 600],  150,  [0,255,0]),
           Planet([1200, 600], 100,  [0,0,255]),
           #Planet([700, 550],  150,  [0,255,255]),
           #Planet([800, 300],  305,  [255,0,255])
           ]

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
def colorIn(toPrint):
    for X in range(1600):
        if (X + 1) % 10 == 0:
            print("x =", (X + 1), "/ 1600")
        for Y in range(800):
            x = X
            y = Y
            xVel = 0
            yVel = 0
            colored = False
            time = 0
            while not colored:
                time += 1
                for i in range(len(Positions)):
                    dist = ((((Positions[i, 0] - x) ** 2) + ((Positions[i, 1] - y) ** 2)) ** 0.5)
                    if dist < Sizes[i]:
                        scale = 1
                        if scaled:
                            if time > scaleTimeSpan:
                                time = scaleTimeSpan
                            scale = time / scaleTimeSpan
                            #scale = -pow(0.9999, time) + 1
                        toPrint[(X*800)+Y, 0] = Colors[i, 0] * scale * 0.5
                        toPrint[(X*800)+Y, 1] = Colors[i, 1] * scale * 0.5
                        toPrint[(X*800)+Y, 2] = Colors[i, 2] * scale * 0.5
                        colored = True
                    else:
                        accel = (Charges[i] * K) / (dist ** 2)
                        xVel += accel * (Positions[i, 0] - x) / (dist*10)
                        yVel += accel * (Positions[i, 1] - y) / (dist*10)
                xVel *= drag
                yVel *= drag
                x += xVel
                y += yVel

@njit
def createLine(x, y):
    toReturn = []
    xVel = 0
    yVel = 0
    colored = False
    time = 0
    while not colored:
        for i in range(len(Positions)):
            dist = ((((Positions[i, 0] - x) ** 2) + ((Positions[i, 1] - y) ** 2)) ** 0.5)
            if dist < Sizes[i]:
                colored = True
            else:
                accel = (Charges[i] * K) / (dist ** 2)
                xVel += accel * (Positions[i, 0] - x) / (dist*10)
                yVel += accel * (Positions[i, 1] - y) / (dist*10)
        if time % 10 == 0 or colored == True:
            toReturn.append([x, y])
        time += 1

        xVel *= drag
        yVel *= drag
        x += xVel
        y += yVel
    if len(toReturn) < 2:
        toReturn = None

    return toReturn
        
        

pygame.init()
screen = pygame.display.set_mode((1600,800))
pygame.display.set_caption("Charged Particles Render")
background = pygame.Surface((1600, 800))

Particles = []

colorIn(toPrint)
for i in range(1280000):
    background.set_at((int(i/800), i%800), (int(toPrint[i, 0]), int(toPrint[i, 1]), int(toPrint[i, 2])))

for i in range(Positions.shape[0]):
    pygame.draw.circle(background, Colors[i].astype(int), Positions[i].astype(int), int(Sizes[i]))

#pygame.image.save(screen, "./save.png") # uncomment to save the image generated


previousCoords = None
previousX = -1
previousY = -1

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                xPos = sorted([0, pygame.mouse.get_pos()[0], 1599])[1]
                yPos = sorted([0, pygame.mouse.get_pos()[1], 799])[1]
                toPrintID = (xPos * 800) + yPos
                Particles.append([xPos, yPos, 0, 0, True, 
                                  (int(toPrint[toPrintID, 0] * 2), int(toPrint[toPrintID, 1] * 2), int(toPrint[toPrintID, 2] * 2))])
            elif event.button == 3:
                rightClick = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                rightClick = False
    
    screen.blit(background, (0,0))

    if rightClick:
        xPos = sorted([0, pygame.mouse.get_pos()[0], 1599])[1]
        yPos = sorted([0, pygame.mouse.get_pos()[1], 799])[1]
        
        toPrintID = (xPos * 800) + yPos

        if xPos == previousX and yPos == previousY and previousCoords != None:
            pygame.draw.lines(screen, (int(toPrint[toPrintID, 0] * 2), int(toPrint[toPrintID, 1] * 2), int(toPrint[toPrintID, 2] * 2)), False, previousCoords, 2)
        else:
            coordinates = createLine(xPos, yPos)
            previousCoords = coordinates
            if coordinates != None:
                pygame.draw.lines(screen, (int(toPrint[toPrintID, 0] * 2), int(toPrint[toPrintID, 1] * 2), int(toPrint[toPrintID, 2] * 2)), False, coordinates, 2)

    for p in reversed(range(len(Particles))):
        for i in range(len(Positions)):
            if Particles[p][4]:
                dist = ((((Positions[i][0] - Particles[p][0]) ** 2) + ((Positions[i][1] - Particles[p][1]) ** 2)) ** 0.5)
                pygame.draw.circle(screen, Particles[p][5], (Particles[p][0], Particles[p][1]), 5)
                if dist < Sizes[i]:
                    Particles[p][4] = False
                else:
                    accel = (Charges[i] * K) / (dist ** 2)
                    Particles[p][2] += accel * (Positions[i][0] - Particles[p][0]) / (dist*10)
                    Particles[p][3] += accel * (Positions[i][1] - Particles[p][1]) / (dist*10)
        Particles[p][2] *= drag
        Particles[p][3] *= drag
        Particles[p][0] += Particles[p][2]
        Particles[p][1] += Particles[p][3]
        if not Particles[p][4]:
            Particles.pop(p)

    pygame.display.update()
pygame.quit()