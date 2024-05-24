from scoreCalculations import MachineLearning
from weights import Weight
from multiprocessing import Process
import time
import concurrent.futures
import random
import copy
import os

#this is the file that actually makes the moves
#decides which move needs to be played next
count = 100
def main():
    #gets genes
    current = os.path.dirname(os.path.abspath(__file__))
    #print(((os.path.join(current, 'gene.txt'))))
    with open(((os.path.join(current, 'gene.txt')))) as f:
        lines = f.readlines()
        a,b,c,d=map(float,lines)

    #creates machien learning instance
    genes = []
    for x in range(count):
        mainIn = MachineLearning(Weight(a,b,c,d))
        genes.append(mainIn)
    while True:
        #creates threads that run the game and update gene slighly adjusting the genes every instance until they are optimal
        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = list(executor.map(MachineLearning.runBase, genes))

            results.sort(reverse=True, key=lambda x: x[0])

            print(results[0][0],results[0][1].getAll())
            s=''
            for x in results[0][1].getAll():
                s+=str(x)+'\n'
            current = os.path.dirname(os.path.abspath(__file__))
            #print(((os.path.join(current, 'gene.txt'))))
            with open(((os.path.join(current, 'gene.txt'))),'w') as f:
                f.write(s)

            mutations = []
            top=results[:100]
            genes = []

            for x in top:
                mutations.append(x[1])

            newGenes =[[],[],[],[]]
            for x in top:
                x=x[1]
                newGenes[0].append(x.getScore())
                newGenes[1].append(x.getHoles())
                newGenes[2].append(x.getBump())
                newGenes[3].append(x.getTetrites())

            for x in range(1000):
                a = random.choice(newGenes[0]) * random.uniform(.99, 1.01)
                b = random.choice(newGenes[1]) * random.uniform(.99, 1.01)
                c = random.choice(newGenes[2]) * random.uniform(.99, 1.01)
                d = random.choice(newGenes[3]) * random.uniform(.99, 1.01)
                w = Weight(a,b,c,d)
                mutations.append(w)


            for x in mutations:
                genes.append(MachineLearning(x))





if __name__ == "__main__":
    main()