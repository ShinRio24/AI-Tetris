import random
#methods for the genetics and weights
class Weight:
    #initizlaised method
    def __init__(self,a,b,c):
        self.score=a
        self.holes =b
        self.bump =c

    #setter method
    def setWeight(self,a,b,c):
        self.score =a
        self.holes = b
        self.bump = c

    #mutate just score
    def mutateScore(self,x):
        self.score*=x
        return self.score
    #mutate hole count
    def mutateHoles(self,x):
        self.holes*=x
        return self.holes
    #mutate bump count
    def mutateBump(self,x):
        self.bump*=x
        return self. bump

    #getter for score
    def getScore(self):
        return self.score

    def getHoles(self):
        return self.holes

    def getBump(self):
        return self.bump



    def getAll(self):
        return [self.score,self.holes,self.bump]

    def setScore(self,x):
        self.score=x
        return self.score

    def setHoles(self, x):
        self.holes = x
        return self.holes

    def setBump(self,x):
        self.bump=x
        return self.bump