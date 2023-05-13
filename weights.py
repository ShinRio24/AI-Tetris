import random
class Weight:
    def __init__(self,a,b,c,d,e):
        self.score=a
        self.holes =b
        self.bump =c
        self.tetrites=d
        self.height=e

    def setWeight(self,a,b,c,d,e):
        self.score =a
        self.holes = b
        self.bump = c
        self.tetrites = d
        self.height = e

    def mutateScore(self,x):
        self.score*=x
        return self.score

    def mutateHoles(self,x):
        self.holes*=x
        return self.holes

    def mutateBump(self,x):
        self.bump*=x
        return self. bump

    def mutateHeight(self,x):
        self.height*=x
        return self.height

    def mutateTetrites(self,x):
        self.tetrites*=x
        return self.tetrites

    def getScore(self):
        return self.score

    def getHoles(self):
        return self.holes

    def getBump(self):
        return self.bump

    def getTetrites(self):
        return self.tetrites

    def getHeight(self):
        return self.height

    def getAll(self):
        return [self.score,self.holes,self.bump,self.tetrites,self.height]

    def setScore(self,x):
        self.score=x
        return self.score

    def setHoles(self, x):
        self.holes = x
        return self.holes

    def setBump(self,x):
        self.bump=x
        return self.bump

    def setTetrites(self,x):
        self.tetrites=x
        return self.tetrites

    def setHeight(self,x):
        self.height=x
        return self.height