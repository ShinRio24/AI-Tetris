from machineLearning import MachineLearning
from weights import Weight
from multiprocessing import Process
import time
import concurrent.futures
import random
import copy
import os
import pygame
import queue

#saves all possible rotations of blocks
rotations = [[
    # blue J peace
    [[-1, 1], [-1, 0], [0, 0], [1, 0]],
    [[0, 1], [0, 0], [0, -1], [1, 1]],
    [[-1, 0], [0, 0], [1, 0], [1, -1]],
    [[-1, -1], [0, 0], [0, -1], [0, 1]]
],

    [
        # Orange L peace
        [[-1, 0], [0, 0], [1, 0], [1, 1]],
        [[0, 1], [0, 0], [0, -1], [1, -1]],
        [[-1, 0], [-1, -1], [0, 0], [1, 0]],
        [[-1, 1], [0, 1], [0, 0], [0, -1]]
    ],

    [
        # Yellow box peace
        [[0, 0], [1, 0], [0, 1], [1, 1]],
        [[0, 0], [1, 0], [0, 1], [1, 1]],
        [[0, 0], [1, 0], [0, 1], [1, 1]],
        [[0, 0], [1, 0], [0, 1], [1, 1]]
    ],

    [
        # Green S peace
        [[-1, 0], [0, 0], [0, 1], [1, 1]],
        [[0, 0], [0, 1], [1, -1], [1, 0]],
        [[-1, -1], [0, -1], [0, 0], [1, 0]],
        [[-1, 1], [-1, 0], [0, 0], [0, -1]]
    ],

    [
        # purple weird shape thing peace
        [[-1, 0], [0, 0], [0, 1], [1, 0]],
        [[0, 0], [0, -1], [0, 1], [1, 0]],
        [[-1, 0], [0, 0], [0, -1], [1, 0]],
        [[-1, 0], [0, 0], [0, 1], [0, -1]]
    ],

    [
        # red Z peace
        [[-1, 1], [0, 1], [0, 0], [1, 0]],
        [[0, 0], [1, 0], [0, -1], [1, 1]],
        [[-1, 0], [0, 0], [0, -1], [1, -1]],
        [[-1, -1], [-1, 0], [0, 0], [0, 1]]
    ],

    [
        # aqua I peace
        [[-1, 0], [0, 0], [1, 0], [2, 0]],
        [[1, 1], [1, 0], [1, -1], [1, -2]],
        [[-1, 0], [0, 0], [1, 0], [2, 0]],
        [[1, 1], [1, 0], [1, -1], [1, -2]]
    ]

]

#this is the file that actually makes the moves
#decides which move needs to be played next
#screens total that are runnning
fullWidth=23
fullHeight=7
count = fullWidth*fullHeight
boxSize = 5
fieldWidth, fieldHeight = boxSize + (boxSize*11)*fullWidth, boxSize+(boxSize*21)*fullHeight
#print(fieldWidth,fieldHeight)
FPS = 5
'''
each block is 5 by 5 tiles
the board is 10 by 20
1 block in between frames / games
have to thread correctly

each game 55 by 105 blocks 
23 games wide 7 games tall
'''

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

#main grid and set up field

display = pygame.display.set_mode((fieldWidth, fieldHeight))
#mainGrid = [[[-1] * 20 for x in range(10)] for x in range(count)]
counter = count *1
screenUpdate = queue.Queue()

def dCounter():
    counter -=1
def gCounter():
    return counter
def rCounter():
    counter = count

#draws border of the game
def addBorder():
    for x in range(fullHeight+1):
        pygame.draw.rect(display, white, (0, 0+(x*boxSize*21), fieldWidth, 5))
    
    for x in range(fullWidth+1):
        pygame.draw.rect(display, white, (0+(x*boxSize*11),0, 5, fieldHeight))

def runNext(game):
    print(1)
    if game[0].isRun()==True:
        
        tem = game[0].nextMove()
        #print(tem)
        if tem==-1:
            game[0].setRun()
            run-=1
        elif tem==1:
            screenUpdate.put_nowait([0,game[1]])
            #full update the screen
        else:
            screenUpdate.put_nowait([1,tem,game[1]])
    dCounter()



def main():
    #gets genes
    current = os.path.dirname(os.path.abspath(__file__))
    #print(((os.path.join(current, 'gene.txt'))))
    with open(((os.path.join(current, 'gene.txt')))) as f:
        lines = f.readlines()
        a,b,c,d=map(float,lines)

    #initializing game
    pygame.font.init()
    pygame.mixer.init()
    pygame.display.set_caption("Tetris AI!")
    clock = pygame.time.Clock()
    pygame.key.set_repeat(500, 100)
    display.fill(pygame.Color("black"))
    #creates machien learning instance
    genes = []
    for x in range(count):
        mainIn = MachineLearning(Weight(a,b,c,d))
        genes.append([mainIn,x])
    

    #draw the borders
    addBorder()
    pygame.display.update()
    run=count

    #creates threads that run the game and update gene slighly adjusting the genes every instance until they are optimal
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(runNext, genes)
        while run>0:
            clock.tick(FPS)
            #print(gCounter())
            if gCounter() == 0:
                print(111)
                rCounter()
                executor.map(runNext, genes)
                print((screenUpdate.qsize()))
                if not screenUpdate.empty():print(screenUpdate.empty(), "dog")
                while not screenUpdate.empty():
                    a=screenUpdate.get()
                    print(a)
                    if(a[0]==0):
                        mainGrid = genes[a[1]].getGrid()
                        for y in range(20):
                            for x in range(10):
                                pygame.draw.rect(display, colorID[mainGrid[x][19 - y]],
                                                (boxSize+((a[1]%fullWidth)*boxSize*11) + (boxSize * x), boxSize+((a[1]//fullWidth)*boxSize*21) + (boxSize * y), boxSize, boxSize))
                    else:
                        mainGrid = genes[a[1]].getGrid()
                        for moves in rotations[a[1][3]][a[1][2]]:
                            pygame.draw.rect(display, colorID[mainGrid[a[1][0]][19 - a[1][1]]],
                                (boxSize+((a[1]%fullWidth)*boxSize*11) + (boxSize * a[1][0]+moves[0]), boxSize+((a[1]//fullWidth)*boxSize*21) + (boxSize * a[1][1]+moves[1]), boxSize, boxSize))
                        
                    print(10)
                    screenUpdate.task_done()

                    pygame.display.update()


                #if game is over, quit game
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        #run=False





if __name__ == "__main__":
    main()