import pygame
import os
import random
from time import sleep
from multiprocessing import Process
from pygame.locals import *
from machineLearning import MachineLearning
from weights import Weight


#rgb for all the colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
purple = (128, 0, 128)
orange = (255, 165, 0)
green = (0, 255, 0)
aqua = (0, 255, 255)
#their id, index returns rgb value
colorID = [blue, orange, yellow, green, purple, red, aqua, white, black]
#size of the entire screen and each tile in tetris
fieldWidth, fieldHeight = 600, 700
boxWidth, boxHeight = 30, 30

#main grid and set up field
display = pygame.display.set_mode((fieldWidth, fieldHeight))
mainGrid = []

#score, holes, bump, tetrites
#imports the gene data from saved txt file
current = os.path.dirname(os.path.abspath(__file__))
#print(((os.path.join(current, 'gene.txt'))))
with open(((os.path.join(current, 'gene.txt')))) as f:
    lines = f.readlines()
    a, b, c, d = map(float,lines)
#creates instance of game as well as weights
tempWeight = Weight(a,b,c,d)
instance = MachineLearning(tempWeight)


#goes through every box to update their color (even ones that have already been updated)
def update():
    # display the boxes
    mainGrid = instance.getGrid()
    for y in range(20):
        for x in range(10):
            pygame.draw.rect(display, colorID[mainGrid[x][19 - y]],
                             (50 + (boxWidth * x), 50 + (boxHeight * y), boxWidth, boxHeight))

#prints the grid (used to debug)
def pMain():
    mainGrid = instance.getGrid()
    for y in range(19, -1, -1):
        s = ''
        for x in range(10):
            s += str(mainGrid[x][y]) + ' '
        print(s)

#draws border of the game
def addBorder():
    pygame.draw.rect(display, white, (49, 49, 302, 1))
    pygame.draw.rect(display, white, (49, 49, 1, 602))
    pygame.draw.rect(display, white, (351, 49, 1, 602))
    pygame.draw.rect(display, white, (49, 651, 302, 1))


#main function, runs when file is ran
def view():
    #initializing game
    pygame.font.init()
    pygame.mixer.init()

    display = pygame.display.set_mode((fieldWidth, fieldHeight))
    #creates display
    pygame.display.set_caption("Tetris AI!")
    pygame.key.set_repeat(500, 100)
    sideFont = pygame.font.SysFont("monospace", 20)


    pygame.display.update()
    #runs game, sets game timer
    run = instance.isRun()
    clock = pygame.time.Clock()
    pygame.key.set_repeat(500, 100)
    #sets speed of the game
    FPS = 5
    while run:
        clock.tick(FPS)
        sideText = 'Hi'
        # text on side
        #settings side display, to show user game stats
        score,level,lines = instance.getAll()
        display.fill(pygame.Color("black"))
        addBorder()
        displayItems = ["Score:" + str(score),'Level:' + str(level),'Lines:' + str(lines)]

        #sets side display
        for x in range(len(displayItems)):
            sideInfo = sideFont.render(displayItems[x], 1, (255, 255, 255))
            display.blit(sideInfo, (375, 100+x*30))

        #calculates next move
        instance.nextMove()
        run = instance.isRun()

        #updates screen
        update()
        pygame.display.update()

        #if game is over, quit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run=False

    #print final score
    print("Final Score: "  + str(instance.getAll()[0]))

if __name__ == "__main__":
    view()