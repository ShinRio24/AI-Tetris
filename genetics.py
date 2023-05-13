from machineLearning import MachineLearning
from weights import Weight
from multiprocessing import Process
import time
import concurrent.futures
import random
import copy

count = 100
def main():
    with open('gene.txt') as f:
        lines = f.readlines()
        a,b,c,d,e=map(float,lines)

    genes = []
    for x in range(count):
        mainIn = MachineLearning(Weight(a,b,c,d,e))
        genes.append(mainIn)
    while True:

        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = list(executor.map(MachineLearning.runBase, genes))

            results.sort(reverse=True, key=lambda x: x[0])

            print(results[0][0],results[0][1].getAll())

            s=''
            for x in results[0][1].getAll():
                s+=str(x)+'\n'
            with open('gene.txt', 'w') as f:
                f.write(s)

            mutations = []
            top=results[:100]
            genes = []

            for x in top:
                mutations.append(x[1])

            newGenes =[[],[],[],[],[]]
            for x in top:
                x=x[1]
                newGenes[0].append(x.getScore())
                newGenes[1].append(x.getHoles())
                newGenes[2].append(x.getBump())
                newGenes[3].append(x.getTetrites())
                newGenes[4].append(x.getHeight())

            for x in range(100):
                a = random.choice(newGenes[0]) * random.uniform(.99, 1.01)
                b = random.choice(newGenes[1]) * random.uniform(.99, 1.01)
                c = random.choice(newGenes[2]) * random.uniform(.99, 1.01)
                d = random.choice(newGenes[3]) * random.uniform(.99, 1.01)
                e = random.choice(newGenes[4]) * random.uniform(.99, 1.01)
                w = Weight(a,b,c,d,e)
                mutations.append(w)


            for x in mutations:
                genes.append(MachineLearning(x))





if __name__ == "__main__":
    main()