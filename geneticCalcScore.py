import random
from weights import Weight
import numpy as np


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
#changes drop rate based on the level you are at (increased drop speed)
levelDropRate={0:48,1:43,2:38,3:33,4:28,5:23,6:18,7:13,8:8,9:6,10:5,13:4,16:3,19:2,29:1}

#instance of machine learning, instances so that you can run multiple at a time to test for best mutation
class MachineLearning:
    def __init__(self, w):
        #all the variables of a instance for tetris, including weights the grid scores rates and what the current piece is
        self.weight = w
        self.grid = [[-1] * 20 for x in range(10)]
        self.score = 0
        self.level = 1
        self.lines = 0
        self.fallRate = levelDropRate[1]
        self.piece = random.randint(0, 6)
        self.nxtPiece = random.randint(0, 6)
        self.run = True

    #sets methods to access
    def setWeight(self,a,b,c,d):
        self.weight.setWeight(a,b,c,d)
    
    #getter for weight
    def getWeight(self):
        return self.weight

    #getter for height + current and next piece
    def getSit(self):
        return self.getHigh()+[self.piece]+[self.nxtPiece]

    #getts all scoreboard attributes
    def getAll(self):
        return [self.score, self.level, self.lines]

    #get main grid
    def getGrid(self):
        return self.grid
    
    #adjust main grid
    def setGrid(self,a):
        self.grid = a
    
    #get all weight elements returned
    def getResults(self):
        #creating copy to not affect main grid
        temGrid = [row[:] for row in self.grid]

        holes = self.holeCounter(temGrid)
        score = self.lines
        bump = self.calcBump(temGrid)

        return [holes,score,bump]

    #get highest point at each grid point
    def getHigh(self):
        r=[]
        for x in range(10):
            tem=0
            for y in range(20):
                if(self.grid[x][y]!=-1):
                    r.append(y+1)
                    tem=1
                    break
            if tem==0:
                r.append(0)
        return r
    
    #get highest point for temp grid (for testing each piece placement)
    def getHighTem(self,temGrid):
        r=[]
        for x in range(10):
            tem=0
            for y in range(19,-1,-1):
                if(temGrid[x][y]!=-1):
                    r.append(y+1)
                    tem=1
                    break
            if tem==0:
                r.append(0)
        return r

    #returns score of item and calcuates the score
    def getPureScore(self):

        temGrid = [row[:] for row in self.grid]

        holes = self.holeCounter(temGrid)
        score = 0
        bump = self.calcBump(temGrid)

        return (holes * self.weight.getHoles()) + (score * self.weight.getScore())+ (bump * self.weight.getBump())


    #returns score of item and calcuates the score
    def getScore(self,x,y,r,temGrid=[], piece = 1):
        if temGrid==[]:
            temGrid = [row[:] for row in self.grid]
        if piece ==1:
            piece =self.piece
        else:
            piece=self.nxtPiece
        #calcualting score if item is placed
        for xx in rotations[piece][r]:
            if ((x+xx[0])<10) and ((x+xx[0])>-1) and ((y+xx[1])<20) and ((y+xx[1])>-1):
                temGrid[x+xx[0]][y+xx[1]] = piece

        holes = self.holeCounter(temGrid)
        score = self.calcClearLines(temGrid,y,r )
        bump = self.calcBump(temGrid)

        return (holes * self.weight.getHoles()) + (score * self.weight.getScore())+ (bump * self.weight.getBump())

    #calculates hole count
    def holeCounter(self,temGrid):
        t = 0
        highs= self.getHighTem(temGrid)
        for x in range(10):
            c = False
            for y in range(min(highs[x],19), -1, -1):
                #print(x,y)
                if (temGrid[x][y] != -1):
                    c = True
                elif c:
                    t += 1

        return t

    #calculates any lines that are cleared and their derserved score
    def calcClearLines(self,temGrid,yy,r):

        
        tem = 0
        dd=set()
        #only looking at Y values which had blocked placed (reduicng calculations)
        for xx in rotations[self.piece][r]:
            dd.add(yy+xx[1])
        dd=list(dd)
        #calculating how many lines are cleared and their respective points
        for y in dd:
            c = sum(temGrid[x][y] == -1 for x in range(10))

            if c == 0:
                tem += 1

        f = [0, 40, 100, 300, 1200]
        return f[tem]

    #check if that certain x value has a peak y block
    def indCheck(self,temGrid, ind):
        prev = 0
        for x in range(19,-1,-1):
            if temGrid[ind][x]!=-1:
                prev=x
                break
        return prev
    
    #calculates bumpyness
    def calcBump(self,temGrid):
        prev = self.indCheck(temGrid,0)
        highs=self.getHighTem(temGrid)
        total =0
        for y in range(10):
            aa=highs[y]
            total+=abs(prev- aa)**2
            prev =aa

        return total

    #main method
    def nextMove(self):

        #reference variables
        solPoint = float('-inf')
        highs=self.getHigh()
        moveScore=float('-inf')
        all=[]

        #check every index that is open for a possible placment
        for x in range(10):
            moveScore=float('-inf')
            for y in range(highs[x], 20):
                #if that block is empty
                if self.grid[x][y] == -1:
                    #test all rotations of block
                    for z in range(4):
                        if self.ifPossible(x, y, z, self.grid):
                            moveScore=self.getScore(x,y,z,[],1)
                            all.append([moveScore,x,y,z])

                    if moveScore!=float('-inf'):
                        break
            
        #looking at all possible placements
        if all  == []:
            self.gameOver()
            return -1
        else:
            #getting placemnt with highet score
            all= sorted(all, key=lambda x: x[0], reverse=True)[:5]
            nMove=float('-inf')
            solution=[]

            #for top 5, looking at the move after to see highest score, and doing that move
            for x in all:
                mn=self.next2Move(x[1],x[2],x[3])
                #print(mn)
                if mn>nMove:
                    nMove=mn
                    solution=[x[1],x[2],x[3]]

            solution.append(self.piece)
            #print(solution[0],solution[1],solution[2])
            self.addPiece(solution[0],solution[1],solution[2])
            if self.checkClear(solution[1],solution[2])==1:
                return 1
            else:
                return solution
    

    #main method #2, this is to calulate the second move
    def next2Move(self,ix,iy,ir):
        #create temp grid with frist move
        temGrid =  [row[:] for row in self.grid]
        for xx in rotations[self.piece][ir]:
            temGrid[ix+xx[0]][iy+xx[1]] = self.piece

        #variables
        solution=[]
        solPoint = float('-inf')
        moveScore=float('-inf')
        highs=self.getHighTem(temGrid)

        #all possible open squares
        for x in range(10):
            for y in range(highs[x], 20):
                if temGrid[x][y] == -1:
                    #all roatations
                    for z in range(4):
                        if self.ifPossible(x, y, z,temGrid):
                            #get scores for eacha nd store best one
                            moveScore = self.getScore(x, y, z, temGrid,2)
                            if moveScore > solPoint:
                                solPoint = moveScore
                    break

        if moveScore  == float('-inf'):
            return -1
        else:
            #return peak score
            return moveScore

    # checks for cleared lines
    def checkClear(self,yy,r):
        

        tem = 0
        dd=set()
        for xx in rotations[self.piece][r]:
            if (yy+xx[1]<20) and (yy+xx[1]>-1):
                dd.add(yy+xx[1])
        dd=sorted(list(dd),reverse=True)
        #clear lines that are full and then add back a empty line
        for y in dd:
            c = sum(self.grid[x][y] == -1 for x in range(10))

            if c == 0:
                for zz in range(10):
                    self.grid[zz].pop(y)
                    self.grid[zz].append(-1)
                tem += 1
        
        #add score for clearning line
        self.lines += tem
        f = [0, 40, 100, 300, 1200]
        self.score += f[tem] * (self.level + 1)
        self.level = self.lines / 10
        if tem!=0:
            return 1
        else:
            return 0

    #if game is still running
    def isRun(self):
        return self.run

    #check if move is possible
    def ifPossible(self, x, y, r, grid=[]):
        if grid==[]:
            grid=self.grid

        place = True
        below = False
        #check all placements for all blocks in that piece
        for z in rotations[self.piece][r]:

            if (x + z[0] < 0):
                place = False
                break

            if (x + z[0] > 9):
                place = False
                break

            if (y + z[1] < 0):
                place = False
                break

            if (y + z[1] > 19):
                place = False
                break
            
            if grid[x+z[0]][y+z[1]] != -1:
                place = False
                break
            #check if something is bleow that piece
            if ((y == 0) or (grid[x+z[0]][y +z[1]- 1] != -1)):
                below = True

        return (place and below)
    
    

    # adds piece to grid
    def addPiece(self, x, y, r):
        if not self.ifPossible(x,y,r):
            print('no possible')

        for z in rotations[self.piece][r]:
            self.grid[x + z[0]][y + z[1]] = self.piece
        self.piecePlaced()

    #when piece is placed, change next pieces in queue
    def piecePlaced(self):
        self.piece = self.nxtPiece
        self.piece = random.randint(0, 6)

    # game is over
    def gameOver(self):
        #print("GAME OVER")
        self.run = False

    #runs actual game
    def runBase(self):
        run = self.isRun()
        while run:
            self.nextMove()
            run = self.isRun()
        return [self.score,self.weight]



if __name__ == "__main__":
    print('idk if this even works because u run view not this file')