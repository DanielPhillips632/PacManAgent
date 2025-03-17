from pacman import Directions
from game import Agent
import game
import util

import random
import numpy as np
import math

class SituationAgent(Agent):
    def setCode(self,codep):
        self.code = codep
    
    def getAction(self,state):
        px,py = state.getPacmanPosition()
        
        g1x,g1y= state.getGhostPosition(1)
        ghost1Angle = np.arctan2(g1y-py,g1x-px)
        if ghost1Angle<0.0:
            ghost1Angle += 2.0*math.pi
        ghost1Dist = math.floor(np.sqrt( (g1x-px)**2 + (g1y-py)**2 ))
        ghost1Pos = ""
        if ghost1Dist <= 3:
            if math.pi/4.0 < ghost1Angle <= 3.0*math.pi/3.0:
                ghost1Pos = "GhostN"
            if 3.0*math.pi/4.0 < ghost1Angle <= 5.0*math.pi/3.0:
                ghost1Pos = "GhostW"
            if 5.0*math.pi/4.0 < ghost1Angle <= 7.0*math.pi/3.0:
                ghost1Pos = "GhostS"
            if 7.0*math.pi/4.0 < ghost1Angle <= 2.0*math.pi:
                ghost1Pos = "GhostE"
            if 0.0 <= ghost1Angle <= math.pi/4.0:
                ghost1Pos = "GhostE"
        else:
            ghost1Pos = "GhostFar"

        north = self.checkDirection(state,px,py+1)
        east = self.checkDirection(state,px+1,py)
        south = self.checkDirection(state,px,py-1)
        west = self.checkDirection(state,px-1,py)
        
        if state.isGhostScared():
            edible = "GhostEdible"
        else:
            edible = "GhostInedible"
        ch = self.code[(north,east,south,west,ghost1Pos,edible)]   
        legal = state.getLegalPacmanActions()
        if ch not in legal:
            ch = random.choice(legal)
        return ch

    def checkDirection(self,state,x,y):
        if state.hasWall(x,y):
            return "Wall"
        elif state.hasFood(x,y):
            return "Pellet"
        elif state.hasCapsule(x,y):
            return "Power Pellet"
        else:
            return "Empty"

class PositionAgent(Agent):
    def setCode(self,codep):
        self.code = codep
    
    def getAction(self,state):
        px,py = state.getPacmanPosition()
  
        ch = self.code[px][py]      
        legal = state.getLegalPacmanActions()
        if ch not in legal:
            ch = random.choice(legal)
        return ch

    
    

