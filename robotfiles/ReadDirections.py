#!/usr/bin/env python3

import ev3dev.ev3 as ev3
from time import sleep
from PidFollowLine import LineFollower
from Directions import Turn

class ReadInDirection:
    # Constructor
    def __init__(self):
        self.MoveList = []
        self.f = open('Sokoban_Moves.txt','r')
        ch = self.f.read(1)
        while(ch):
            self.MoveList.append(ch)
            ch = self.f.read(1)
            
            
        self.MoveList.append('End')
        orientation = 'u'
        for i in range(len(self.MoveList)):
            if (self.MoveList[i] == 'End'):
                break
            if (self.MoveList[i] == orientation):
                self.MoveList[i] = 'Straight'
            else:
                if (self.MoveList[i].isupper()):
                    if (self.MoveList[i+1] != self.MoveList[i]):
                        self.MoveList[i] = 'LastPush'
                    else:
                        orientationPlus = orientation.lower()
                        self.MoveList[i] = findorientation(self.MoveList[i],orientation)
                        orientation = orientationPlus
                else:
                    orientationPlus = self.MoveList[i].lower()
                    self.MoveList[i] = findorientation(self.MoveList[i],orientation)
                    orientation = orientationPlus
        self.i = 0
        self.lineFollower = LineFollower()
        self.directions = Turn()
        for item in self.MoveList:
            print ("{0}\n", item)


    # Main method
    def run(self):

        

        if (self.MoveList[self.i] == 'End'):
            return False

        if (self.MoveList[self.i] == 'LastPush'):
            self.lineFollower.run(True)
            print("LastPush")
        elif( (self.MoveList[self.i] == 'left') or (self.MoveList[self.i] == 'right') ):
            self.directions.TurnDebug(self.MoveList[self.i])
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