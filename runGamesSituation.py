from pacman import *
import ghostAgents
import layout
import textDisplay
import graphicsDisplay
import copy
import numpy as np
from pprint import pprint
import sys
import itertools

## set up the parameters to newGame
numtraining = 0
timeout = 30
beQuiet = True
pacmanType = loadAgent("SituationAgent", True)
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
    for p in parent:
        if random.random() < mutationChance:
            parent[p] = random.choice(options)
    return parent

def crossover(parent1,parent2,crossoverChance = 0.6):
    child1 = {}
    child2 = {}
    for p in parent1:
        if random.random() < crossoverChance:
            child1[p] = parent2[p]
            child2[p] = parent1[p]
        else:
            child1[p] = parent1[p]
            child2[p] = parent2[p]
    return child1, child2
    

def runGA(popSiz=20,timescale=20,numberOfRuns=2,tournamentSize=4,gridLayout="mediumClassic"):

    global mylayout
    mylayout = layout.getLayout(gridLayout)
    
    population = []
    boundaries = list(itertools.product(["Empty","Wall","Pellet","Power Pellet"], repeat=4))
    threats = ["GhostFar","GhostN", "GhostE", "GhostS", "GhostW"]
    edible = ["GhostEdible", "GhostInedible"]
    situation = [(b+(t,e)) for b in boundaries for t in threats for e in edible]
    for _ in range(popSiz):
        program = {}
        for s in situation:
            program[s] = random.choice(options)
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
    mylayout = layout.getLayout("smallClassic")
    
    boundaries = list(itertools.product(["Empty","Wall","Pellet","Power Pellet"], repeat=4))
    threats = ["GhostFar","GhostN", "GhostE", "GhostS", "GhostW"]
    edible = ["GhostEdible", "GhostInedible"]
    situation = [(b+(t,e)) for b in boundaries for t in threats for e in edible]
    program = {}
    for s in situation:
        program[s] = Directions.EAST
    
    run(program,1)

#runTest()
#runGA()

