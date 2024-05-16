import pygame
import os
import random
from time import sleep
from pygame.locals import *
from scoreCalculations import MachineLearning
from weights import Weight

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


#prints the grid (used to debug)
def pMain():
    mainGrid = instance.getGrid()
    for y in range(19, -1, -1):
        s = ''
        for x in range(10):
            s += str(mainGrid[x][y]) + ' '
        print(s)

#main function, runs when file is ran
def view():
    grrid=[
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [1,-1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [1,-1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [1,-1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [1,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
    ]
    instance.setGrid(grrid)
    pMain()

    print(len(grrid), len(grrid[0]))
    print(instance.calcBump(grrid))
    print(instance.holeCounter(grrid))
    print(instance.getPureScore())
      
     

        

    
if __name__ == "__main__":
    view()