#!/usr/bin/env python3

import ev3dev.ev3 as ev3
from time import sleep
from PidFollowLine import LineFollower
from Directions import Turn

class ReadInDirection:
    # Constructor
    def __init__(self):
        charlist = []
        self.MoveList = []
        self.ExecutionList = []
        self.f = open('Sokoban_Moves.txt','r')
        ch = self.f.read(1)
        while(ch):
            charlist.append(ch)
            ch = self.f.read(1)
            
            
        charlist.append('End')
        orientation = 'u'
        for i in range(len(charlist)):
            if (charlist[i] == 'End'):
                break
            if (charlist[i].lower() == orientation):
                self.ExecutionList.append('Straight')
            else:
                orientationPlus = orientation.lower()
                self.ExecutionList.append(findorientation(charlist[i],orientation))
                orientation = orientationPlus
            if (charlist[i].isupper()):
                if (charlist[i+1] != charlist[i]):
                    self.ExecutionList.append('LastPush')
        self.ExecutionList.append('End')
        self.i = 0
        self.lineFollower = LineFollower()
        self.directions = Turn()
        for item in self.ExecutionList:
            print ("{0}\n", item)


    # Main method
    def run(self):

        

        if (self.ExecutionList[self.i] == 'End'):
            return False

        if (self.ExecutionList[self.i] == 'LastPush'):
            self.lineFollower.run(True)
            print("LastPush")
        elif( (self.ExecutionList[self.i] == 'left') or (self.ExecutionList[self.i] == 'right') ):
            self.directions.TurnDebug(self.ExecutionList[self.i])
            self.lineFollower.run(False)
            print("Turn")
        else: # Straight
            self.lineFollower.run(False)
            print("Straight")

        self.i += 1
        return True



def findorientation(input,orientation):
    turndir = ""
    if (input.lower() == 'u' and (orientation == 'l' ) ):
        turndir = "right"
    elif (input.lower() == 'u' and (orientation == 'r' ) ):
        turndir = "left"
    elif (input.lower() == 'l' and (orientation == 'u' ) ):
        turndir = "left"
    elif (input.lower() == 'l' and (orientation == 'd' ) ):
        turndir = "right"
    elif (input.lower() == 'r' and (orientation == 'u' ) ):
        turndir = "right"
    elif (input.lower() == 'r' and (orientation == 'd' ) ):
        turndir = "left"
    elif (input.lower() == 'd' and (orientation == 'l' ) ):
        turndir = "left"
    elif (input.lower() == 'd' and (orientation == 'r' ) ):
        turndir = "right"
    

    return turndir