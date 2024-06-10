
import os
import random
from time import sleep
from neuralCalcScore import MachineLearning
from numpy import loadtxt
#from tensorflow.keras.models import Sequential
#from tensorflow.keras.layers import Dense
#from tensorflow.keras.models import load_model


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
instance = MachineLearning()

#model = load_model('tetris.h5')
#model.summary()


#prints the grid (used to debug)
def pMain():
    mainGrid = instance.getGrid()
    for y in range(19, -1, -1):
        s = ''
        for x in range(10):
            s += str(mainGrid[x][y]) + ' '
        print(s)

def main():
    saves= []
    while instance.isRun():

        situation = instance.getSit()
        loc=random.randint(0,9)
        rot = random.randint(0,3)
        prev = instance.getResults()
        if instance.addPiece(loc,rot)==-1:
            print('something is broken bro')
            return 0
        now=instance.getResults()
        #holes, score,tetrites, bump
        score = 0
        if now[0]!=0:score += (prev[0]/now[0])-1 
        if now[1]!=0:score -= (prev[1]/now[1])-1
        if now[2]!=0:score -= (prev[2]/now[2])-1
        if now[3]!=0:score += (prev[3]/now[3])-1
        
        saves.append([situation,score])


    #we need to make this
    #input is going to be the getHigh (10) and the piece index (6) and the next piece index (6)
    #model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    # fit the keras model on the dataset
    #model.train_on_batch(X_batch, Y_batch)

    # make class predictions with the model

    print(saves)

    #model.save("tetris.h5")


if __name__ == "__main__":
    main()