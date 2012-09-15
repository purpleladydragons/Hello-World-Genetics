import random
import sys

sys.setrecursionlimit(9999999)

class Gene:
    def __init__(self,code=''):
        self.cost = 9999
        self.code = code

    def random(self,length):
        while length > 0:
            self.code += chr(random.randint(0,255))
            length -= 1


    def mutate(self,chance):
        if random.random() <= chance:
            index = int(random.random() * len(self.code))
            upOrDown = -1 if random.random() <= .5 else 1
            try:newChar = chr(ord(self.code[index]) + upOrDown) 
            except ValueError:
                if upOrDown > 0:
                    newChar = chr(0)
                else:
                    newChar = chr(255)
            newString = ''
            for i in range(len(self.code)):
                if i == index:
                    newString += newChar
                else:
                    newString += self.code[i]

            self.code = newString

    def mate(self,gene):
        pivot = int(round(len(self.code))/2 - 1) #int(round()) may cause problems because floats are gay
        child1 = self.code[:pivot] + gene.code[pivot:] #this may cause problems cause idk whats going on
        child2 = gene.code[:pivot] + self.code[pivot:]

        return [Gene(child1),Gene(child2)]

    def calcCost(self,compareTo):
        total = 0
        for i in range(len(self.code)):
            total += (ord(self.code[i]) - ord(compareTo[i])) ** 2
        self.cost = total

class Population:
    def __init__(self,goal,size):
        self.members = []
        self.goal = goal
        self.generationNum = 0
        while size > 0:
            gene = Gene()
            gene.random(len(self.goal))
            self.members.append(gene)
            size -= 1
    
    def display(self):
        for i in range(len(self.members)):
            print self.members[i].code, self.members[i].cost

    def sort(self):
        self.members.sort(key = lambda x: x.cost, reverse=False) #toggle reverse maybe? 

    def generation(self):
        for i in range(len(self.members)):
            self.members[i].calcCost(self.goal)

        self.sort()
        self.display()
        children = self.members[0].mate(self.members[1])
        self.members[-2] = children[0]
        self.members[-1] = children[1]

        for i in range(len(self.members)):
            self.members[i].mutate(.5)
            self.members[i].calcCost(self.goal)
            if self.members[i].code == self.goal:
                self.sort()
                self.display()
                return True

        self.generationNum += 1
        scope = self
        scope.generation()

population = Population("Hello, world!", 5)
population.generation()

print population.members[0].code














