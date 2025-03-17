from pacman import *
import ghostAgents
import layout
import textDisplay
import graphicsDisplay
import copy
import numpy as np
from pprint import pprint
import sys

## set up the parameters to newGame
numtraining = 0
timeout = 30
beQuiet = True
pacmanType = loadAgent("PositionAgent", True)
numGhosts = 1
ghosts = [ghostAgents.RandomGhost(i+1) for i in range(numGhosts)]
catchExceptions = True

def run(code,noOfRuns):
    rules = ClassicGameRules(timeout)
    games = []
    if beQuiet:
        gameDisplay = textDisplay.NullGraphics()
        rules.quiet = True
    else:
        timeInterval = 0.001
        textDisplay.SLEEP_TIME = timeInterval
        gameDisplay = graphicsDisplay.PacmanGraphics(1.0, timeInterval)
        rules.quiet = False
    for gg in range(noOfRuns):
        thePacman = pacmanType()
        thePacman.setCode(code)
        game = rules.newGame( mylayout, thePacman, ghosts, gameDisplay, \
                          beQuiet, catchExceptions )
        game.run()
        games.append(game)
    scores = [game.state.getScore() for game in games]
    return sum(scores) / float(len(scores))

####### genetic algorithm

options = [Directions.NORTH, Directions.EAST, Directions.SOUTH, Directions.WEST]
    
def mutate(parentp,mutationChance = 0.01):
    parent = copy.deepcopy(parentp)
    for xx in range(width):
        for yy in range(height):
            if random.random() < mutationChance:
                parent[xx][yy] = random.choice(options)
    return parent

def crossover(parent1,parent2,crossoverChance = 0.6):
    child1 = np.empty((width,height),dtype=object)
    child2 = np.empty((width,height),dtype=object)
    for xx in range(width):
        for yy in range(height):
            if random.random() < crossoverChance:
                child1[xx][yy] = parent2[xx][yy]
                child2[xx][yy] = parent1[xx][yy]
            else:
                child1[xx][yy] = parent1[xx][yy]
                child2[xx][yy] = parent2[xx][yy]
    return child1, child2

def runGA(popSiz=20,timescale=20,numberOfRuns=2,tournamentSize=4,gridLayout="mediumClassic"):

    global mylayout
    mylayout = layout.getLayout(gridLayout)
    global height
    height = mylayout.height-1
    global width
    width = mylayout.width-1

    population = []
    for _ in range(popSiz):
        program = np.empty((width,height),dtype=object)
        for xx in range(width):
            for yy in range(height):
                program[xx][yy] = random.choice(options)
        population.append(program)
            
    print("Beginning Evolution")
    averages = []
    bests = []
    for _ in range(timescale):
        ## evaluate population
        fitness = []
        for pp in population:
            print(".",end="",flush=True)
            fitness.append(run(pp,numberOfRuns))
        print("\n******")
        print(fitness)
        averages.append(1000+sum(fitness)/popSiz)
        print("av ",1000+sum(fitness)/popSiz)
        bests.append(1000+max(fitness))
        print("max ",1000+max(fitness))

        popFitPairs = list(zip(population,fitness))
        newPopulation = []
        for _ in range(popSiz // 2):

                tournament = random.sample(popFitPairs, tournamentSize)
                parent1 = max(tournament, key=lambda x: x[1])[0]
                tournament = random.sample(popFitPairs, tournamentSize)
                parent2 = max(tournament, key=lambda x: x[1])[0]
                child1, child2 = crossover(parent1, parent2)

                child1 = mutate(child1)
                child2 = mutate(child2)

                newPopulation.append(child1)
                newPopulation.append(child2)
                
        best_member = max(popFitPairs, key=lambda x: x[1])[0]
        newPopulation.append(best_member)

        population = copy.deepcopy(newPopulation)
        
    return averages, bests

def runTest():
    
    global mylayout
    mylayout = layout.getLayout("mediumClassic")
    global height
    height = mylayout.height-1
    global width
    width = mylayout.width-1
    
    program = np.empty((width,height),dtype=object)
    for xx in range(width):
        for yy in range(height):
            program[xx][yy] = Directions.EAST
    
    run(program,1)

#runTest()    
#runGA()
        

