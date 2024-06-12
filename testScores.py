import pygame
import os
import random
from time import sleep
from pygame.locals import *
from geneticCalcScore import MachineLearning
from weights import Weight

mainGrid = []

#score, holes, bump, tetrites
#imports the gene data from saved txt file
current = os.path.dirname(os.path.abspath(__file__))
#print(((os.path.join(current, 'gene.txt'))))
with open(((os.path.join(current, 'gene.txt')))) as f:
    lines = f.readlines()
    a, b, c= map(float,lines)
#creates instance of game as well as weights
tempWeight = Weight(a,b,c)
instance = MachineLearning(tempWeight)



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


#prints the grid (used to debug)
def pMain():
    mainGrid = instance.getGrid()
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

#goes through every box to update their color (even ones that have already been updated)
def update():
    # display the boxes
    mainGrid = instance.getGrid()
    for y in range(20):
        for x in range(10):
            pygame.draw.rect(display, colorID[mainGrid[x][19 - y]],
                             (50 + (boxWidth * x), 50 + (boxHeight * y), boxWidth, boxHeight))

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
    display.fill(pygame.Color("black"))
    addBorder()


    grrid=[
        [1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [4,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [4,-1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,4,-1,-1,-1],
        [4,-1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [4,-1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [4,4,4,4,4,4,4,4,4,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [1,-1,-1,-1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
    ]
    instance.setGrid(grrid)
    pMain()
    instance.setNext(0)

    print(instance.getPureScore())

    instance.nextMove()
    print(instance.getPureScore())
    rune =True
    while rune:
        update()
        pygame.display.update()
            
        
        #if game is over, quit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run=False
        

    
if __name__ == "__main__":
    view()