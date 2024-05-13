import random
from weights import Weight

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
        self.run = True

    #sets methods to access
    def setWeight(self,a,b,c,d):
        self.weight.setWeight(a,b,c,d)
    
    
    
    def getWeight(self):
        return self.weight

    def getAll(self):
        return [self.score, self.level, self.lines]

    def getGrid(self):
        return self.grid
    
    def setGrid(self,a):
        self.grid = a

    #returns score of item and calcuates the score
    def getPureScore(self):

        temGrid = self.grid

        holes = self.holeCounter(temGrid)
        score = self.calcClearLines(temGrid)
        tetrites = 4 if (score >= 4) else 0
        bump = self.calcBump(temGrid)

        return (holes * self.weight.getHoles()) + (score * self.weight.getScore()) + (tetrites * self.weight.getTetrites()) + (bump * self.weight.getBump())

    #returns score of item and calcuates the score
    def getScore(self,x,y,r):

        temGrid = [row[:] for row in self.grid]
        for xx in rotations[self.piece][r]:
            temGrid[x+xx[0]][y+xx[1]] = self.piece

        holes = self.holeCounter(temGrid)
        score = self.calcClearLines(temGrid)
        tetrites = 4 if (score == 4) else -score
        bump = self.calcBump(temGrid)

        return (holes * self.weight.getHoles()) + (score * self.weight.getScore()) + (tetrites * self.weight.getTetrites()) + (bump * self.weight.getBump())

    #calculates hole count
    def holeCounter(self,temGrid):
        t = 0
        for x in range(10):
            c = False
            for y in range(19, -1, -1):
                if (temGrid[x][y] != -1):
                    c = True
                elif c:
                    t += 1

        return t

    #calculates any lines that are cleared and their derserved score
    def calcClearLines(self,temGrid):
        tem = 0

        for y in range(19, -1, -1):
            c = sum(temGrid[x][y] == -1 for x in range(10))

            if c == 0:
                tem += 1

        f = [0, 40, 100, 300, 1200]
        return tem

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

        total =0
        for y in range(10):
            aa=self.indCheck(temGrid,y)
            total+=abs(prev- aa)*2
            prev =aa

        return total

    #main method
    def nextMove(self):

        solution=[]
        solPoint = float('-inf')
        for x in range(10):
            for y in range(19, -1, -1):
                if self.grid[x][y] != -1:
                    break

                for z in range(4):
                    if self.ifPossible(x, y, z):
                        moveScore = self.getScore(x, y, z)

                        if moveScore > solPoint:
                            solPoint = moveScore
                            solution = [x, y, z]

        if solution  == []:
            self.gameOver()
            return -1
        else:
            solution.append(self.piece)
            self.addPiece(solution[0],solution[1],solution[2])
            if self.checkClear()==1:
                return 1
            else:
                return solution

    # checks for cleared lines
    def checkClear(self):
        tem = 0

        for y in range(19, -1, -1):
            c = sum(self.grid[x][y] == -1 for x in range(10))

            if c == 0:
                tem += 1

                for x in range(10):
                    self.grid[x].pop(y)

        for x in range(10):
            for y in range(tem):
                self.grid[x].append(-1)

        self.lines += tem
        f = [0, 40, 100, 300, 1200]
        self.score += f[tem] * (self.level + 1)
        self.level = self.lines / 10
        if tem!=0:
            return 1
        else:
            return 0

    def isRun(self):
        return self.run

    def ifPossible(self, x, y, r):
        place = True
        below = False
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

            if self.grid[x+z[0]][y+z[1]] != -1:
                place = False

            if ((y == 0) or (self.grid[x+z[0]][y +z[1]- 1] != -1)):
                below = True

        return (place and below)

    # adds piece to grid
    def addPiece(self, x, y, r):
        if not self.ifPossible(x,y,r):
            print('no possible')

        for z in rotations[self.piece][r]:
            self.grid[x + z[0]][y + z[1]] = self.piece
        self.piecePlaced()

    def piecePlaced(self):
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