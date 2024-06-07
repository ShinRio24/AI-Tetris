
import os
import random
from time import sleep
from calcScore import MachineLearning


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
mainGrid = []

current = os.path.dirname(os.path.abspath(__file__))

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

  


    #runs game, sets game timer
    run = instance.isRun()

    #sets speed of the game
    FPS = 5
    while run:
        sideText = 'Hi'
        # text on side
        #settings side display, to show user game stats
        score,level,lines = instance.getAll()
        displayItems = ["Score:" + str(score),'Level:' + str(level),'Lines:' + str(lines)]

        #sets side display
        for x in range(len(displayItems)):

        #calculates next move
        instance.nextMove()
        run = instance.isRun()


    #print final score
    print("Final Score: "  + str(instance.getAll()[0]))

if __name__ == "__main__":
    view()