#!/usr/bin/env python3

import ev3dev.ev3 as ev3
from time import sleep
from PidFollowLine import LineFollower
from Directions import Turn

class ReadInDirection:
    # Constructor
    def __init__(self):
    
        self.f = open('Sokoban_Moves.txt','r')
        self.previous = 'u'
        




    # Main method
    def run(self):
        lineFollower = LineFollower()
        directions = Turn()
        ch = self.f.read(1)
        if not ch:
            print("End of file")
            return False
        
        if (ch == self.previous):
            lineFollower.run()
        #elif (self.previous == 'a'):
         #   lineFollower.run()
        elif (ch.isupper()):
            turndir = findorientation(ch,self.previous)
            print("isupper")
            directions.TurnDebug(turndir)
            lineFollower.run()
            lineFollower.run()
            directions.Backup()
            directions.TurnAround()
            lineFollower.run()
            directions.TurnAround()
        else:
            turndir = findorientation(ch,self.previous)
            print("else")
            directions.TurnDebug(turndir)
            lineFollower.run()
            

        self.previous = ch
        return True

def findorientation(input,prev_input):
    turndir = ""
    if (input.lower() == 'u' and (prev_input == 'l' or prev_input =='L')):
        turndir = "right"
    elif (input.lower() == 'u' and (prev_input == 'r' or prev_input =='R')):
        turndir = "left"
    elif (input.lower() == 'l' and (prev_input == 'u' or prev_input =='U')):
        turndir = "left"
    elif (input.lower() == 'l' and (prev_input == 'd' or prev_input =='D')):
        turndir = "right"
    elif (input.lower() == 'r' and (prev_input == 'u' or prev_input =='U')):
        turndir = "right"
    elif (input.lower() == 'r' and (prev_input == 'd' or prev_input =='D')):
        turndir = "left"
    elif (input.lower() == 'd' and (prev_input == 'l' or prev_input =='L')):
        turndir = "left"
    elif (input.lower() == 'd' and (prev_input == 'r' or prev_input =='R')):
        turndir = "right"
    

    return turndir