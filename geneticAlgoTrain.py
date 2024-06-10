#import all of the libraries
from geneticCalcScore import MachineLearning
from weights import Weight
import threading
import time
import concurrent.futures
import random
import copy
import os
import contextlib
with contextlib.redirect_stdout(None):
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
# fullWidth=23
# fullHeight=7
# boxSize = 5

#set parameters of the build
fullWidth=5
fullHeight=5
boxSize = 5
#%mutation, lower this number as you have run your bot more
alpha=.05
iterations=100

count = fullWidth*fullHeight
fieldWidth, fieldHeight = boxSize + (boxSize*11)*fullWidth, boxSize+(boxSize*21)*fullHeight
#print(fieldWidth,fieldHeight)
FPS = 10
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
counter = count *1
#setting up pygame (library used for the display of the game)
screenUpdate = queue.Queue()
pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.display.set_caption("Tetris AI!")
clock = pygame.time.Clock()
pygame.key.set_repeat(500, 100)

#draws border of the game
def addBorder():
    #adding all horizontal lines
    for x in range(fullHeight+1):
        pygame.draw.rect(display, white, (0, 0+(x*boxSize*21), fieldWidth, boxSize))
    #adding all verticle lies
    for x in range(fullWidth+1):
        pygame.draw.rect(display, white, (0+(x*boxSize*11),0, boxSize, fieldHeight))


#this is to run the next move, must use this to call with multithreading
def runNext(game,ind,weights):
    if game.isRun()==True:
        
        tem = game.nextMove()
        #print(tem)
        if tem==-1:
            screenUpdate.put_nowait([-1,game])
        elif tem==1:
            screenUpdate.put_nowait([1,ind])
            #full update the screen
        else:
            screenUpdate.put_nowait([0,tem,ind])


#the main method
def main(doDisplay):
    #gets genes that are saved in the text file
    current = os.path.dirname(os.path.abspath(__file__))
    with open(((os.path.join(current, 'gene.txt')))) as f:
        lines = f.readlines()
        a,b,c=map(float,lines)


    #initializing game
    display.fill(pygame.Color("black"))
    #creates machien learning instance
    genes = [[MachineLearning(Weight(a,b,c)),0,[a,b,c]]]

    #mutates genes slightly so that there is growth
    for x in range(1,count):
        aa= a * random.uniform(1-alpha, 1+alpha)
        bb= b * random.uniform(1-alpha, 1+alpha)
        cc= c * random.uniform(1-alpha, 1+alpha)
        genes.append([MachineLearning(Weight(aa,bb,cc)),x,[aa,bb,cc]])
    

    #draw the borders
    addBorder()
    pygame.display.update()
    pygame.display.flip()

    #option to display game (performance is slower when game is displayed)
    if doDisplay==False:
        pygame.close()
    #creates threads that run the game and update gene slighly adjusting the genes every instance until they are optimal
    run = True
    finals=[]
    #this is the acutal game loop, simply runs all the multithreading instances
    while run==True:
        clock.tick(FPS)

        #run multi threading instances
        runGenes =[]
        for gene in genes:
            runGenes.append(threading.Thread(target=runNext,args=gene))
        for gene in runGenes:
            gene.start()
        for gene in runGenes:
            gene.join()
        

        if screenUpdate.empty():
            run=False

        #runs the display   
        if doDisplay ==True:
            #update screen
            while not screenUpdate.empty():
                a=screenUpdate.get()
                if(a[0]==-1):
                    finals.append([a[1].getAll()[0],a[1].getWeight()])
                elif(a[0]==1):
                    #reset whole map
                    mainGrid = genes[a[1]][0].getGrid()
                    for y in range(20):
                        for x in range(10):
                            pygame.draw.rect(display, colorID[mainGrid[x][19 - y]],
                                            (boxSize+((a[1]%fullWidth)*boxSize*11) + (boxSize * x),
                                                boxSize+((a[1]//fullWidth)*boxSize*21) + (boxSize * y), boxSize, boxSize))
                else:
                    #only add new piece
                    mainGrid = genes[a[2]][0].getGrid()
                    #print(mainGrid)
                    #print([a[1][0]],[a[1][1]])
                    for moves in rotations[a[1][3]][a[1][2]]:
                        #print(moves)
                        pygame.draw.rect(display, colorID[mainGrid[a[1][0]][a[1][1]]],
                                        (boxSize+((a[2]%fullWidth)*boxSize*11) + (boxSize * (a[1][0]+moves[0])), 
                                        boxSize+((a[2]//fullWidth)*boxSize*21) + (boxSize * (19-(a[1][1]+moves[1]))), boxSize, boxSize))
                #pygame.draw.rect(display,colorID[0],[50,50,10,10])
                screenUpdate.task_done()

                pygame.display.update()
                pygame.display.flip()
            


    #print out final results
    finals.sort(reverse=True, key=lambda x: x[0])
    print(finals[0])
    s=''
    
    #save new weights
    for newWeights in finals[0][1].getAll():
        s+=str(newWeights)+'\n'
    with open(((os.path.join(current, 'gene.txt'))),'w') as f:
        f.write(s)

    print("GAME OVER")
    time.sleep(.5)



if __name__ == "__main__":
    for x in range(iterations):main(True)
    pygame.quit()




'''
to do:
change genetics so that you take values of top 5 and swithc around
make calculations more efficient
use a* algo
make sure hole calculations are working


PROBABLY SHOULD USE Q LEARNING ALGO
Q LEARNING
Q LEARNING Q LEARNING
JUST LOOK INTO IT


check this line in the ifPossible function of machine learning file
if ((y == 0) or (self.grid[x+z[0]][y +z[1]- 1] != -1)):

for q lerning, calculate score of move 3 moves after (just use score of board 3 moves after) so that the computer can factor in 
the choice made knowing the next piece that is dropping


'''