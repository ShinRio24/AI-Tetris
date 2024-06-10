from geneticCalcScore import MachineLearning
from weights import Weight
#from multiprocessing import Process
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
fullWidth=23
fullHeight=7
boxSize = 5

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
#mainGrid = [[[-1] * 20 for x in range(10)] for x in range(count)]
counter = count *1
screenUpdate = queue.Queue()
pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.display.set_caption("Tetris AI!")
clock = pygame.time.Clock()
pygame.key.set_repeat(500, 100)

#draws border of the game
def addBorder():
    for x in range(fullHeight+1):
        pygame.draw.rect(display, white, (0, 0+(x*boxSize*21), fieldWidth, boxSize))
    
    for x in range(fullWidth+1):
        pygame.draw.rect(display, white, (0+(x*boxSize*11),0, boxSize, fieldHeight))

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



def main(doDisplay):
    #gets genes
    current = os.path.dirname(os.path.abspath(__file__))
    #print(((os.path.join(current, 'gene.txt'))))
    with open(((os.path.join(current, 'gene.txt')))) as f:
        lines = f.readlines()
        a,b,c,d=map(float,lines)

    #initializing game
    
    display.fill(pygame.Color("black"))
    #creates machien learning instance
    genes = [[MachineLearning(Weight(a,b,c,d)),0,[a,b,c,d]]]

    for x in range(1,count):
        aa= a * random.uniform(.9, 1.1)
        bb= b * random.uniform(.9, 1.1)
        cc= c * random.uniform(.9, 1.1)
        dd= d * random.uniform(.9, 1.1)
        genes.append([MachineLearning(Weight(aa,bb,cc,dd)),x,[aa,bb,cc,dd]])
    

    #draw the borders
    addBorder()
    pygame.display.update()
    pygame.display.flip()

    if doDisplay==False:
        pygame.close()
    #creates threads that run the game and update gene slighly adjusting the genes every instance until they are optimal
    #with concurrent.futures.ProcessPoolExecutor() as executor:
    run = True
    finals=[]
    while run==True:
        clock.tick(FPS)

        runGenes =[]
        for gene in genes:
            runGenes.append(threading.Thread(target=runNext,args=gene))
        for gene in runGenes:
            gene.start()
        for gene in runGenes:
            gene.join()
        
        if screenUpdate.empty():
            run=False
                
        if doDisplay ==True:
            while not screenUpdate.empty():
                a=screenUpdate.get()
                #print(a[1])
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
            


        #if game is over, quit game
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         run=False
    finals.sort(reverse=True, key=lambda x: x[0])
    print(finals[0])
    s=''
    for newWeights in finals[0][1].getAll():
        s+=str(newWeights)+'\n'
    with open(((os.path.join(current, 'gene.txt'))),'w') as f:
        f.write(s)

    print("GAME OVER")
    time.sleep(.5)



if __name__ == "__main__":
    for x in range(5):main(True)
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