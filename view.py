import pygame
import os
import random
from time import sleep
from multiprocessing import Process
from pygame.locals import *
from machineLearning import MachineLearning
from weights import Weight

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
purple = (128, 0, 128)
orange = (255, 165, 0)
green = (0, 255, 0)
aqua = (0, 255, 255)
colorID = [blue, orange, yellow, green, purple, red, aqua, white, black]
fieldWidth, fieldHeight = 600, 700
boxWidth, boxHeight = 30, 30

display = pygame.display.set_mode((fieldWidth, fieldHeight))
mainGrid = []

#score, holes, bump, tetrites
with open('gene.txt') as f:
    lines = f.readlines()
    a, b, c, d,e = map(float,lines)

tempWeight = Weight(a,b,c,d,e)
instance = MachineLearning(tempWeight)

def update():
    # display the boxes
    mainGrid = instance.getGrid()
    for y in range(20):
        for x in range(10):
            pygame.draw.rect(display, colorID[mainGrid[x][19 - y]],
                             (50 + (boxWidth * x), 50 + (boxHeight * y), boxWidth, boxHeight))

def pMain():
    mainGrid = instance.getGrid()
    print('DDDDDDD')
    for y in range(19, -1, -1):
        s = ''
        for x in range(10):
            s += str(mainGrid[x][y]) + ' '
        print(s)

def addBorder():
    pygame.draw.rect(display, white, (49, 49, 302, 1))
    pygame.draw.rect(display, white, (49, 49, 1, 602))
    pygame.draw.rect(display, white, (351, 49, 1, 602))
    pygame.draw.rect(display, white, (49, 651, 302, 1))

def view():

    pygame.font.init()
    pygame.mixer.init()

    display = pygame.display.set_mode((fieldWidth, fieldHeight))

    pygame.display.set_caption("Tetris AI!")
    pygame.key.set_repeat(500, 100)
    sideFont = pygame.font.SysFont("monospace", 20)


    pygame.display.update()

    run = instance.isRun()
    clock = pygame.time.Clock()
    pygame.key.set_repeat(500, 100)
    FPS = 10
    while run:
        clock.tick(FPS)
        sideText = 'Hi'
        # text on side

        score,level,lines = instance.getAll()
        display.fill(pygame.Color("black"))
        addBorder()
        displayItems = ["Score:" + str(score),'Level:' + str(level),'Lines:' + str(lines)]

        for x in range(len(displayItems)):
            sideInfo = sideFont.render(displayItems[x], 1, (255, 255, 255))
            display.blit(sideInfo, (375, 100+x*30))

        instance.nextMove()
        run = instance.isRun()

        update()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run=False

    print("Final Score: "  + str(instance.getAll()[0]))

if __name__ == "__main__":
    view()