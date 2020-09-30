#!/usr/bin/env python3

import ev3dev.ev3 as ev3
from time import sleep
from PidFollowLine import LineFollower
from Directions import Turn

class ReadInDirection:
    # Constructor
    def __init__(self):
    
        self.f = open('Sokoban_Moves.txt','r')
        self.previous = 'a'
        




    # Main method
    def run(self):
        lineFollower = LineFollower()
        directions = Turn()
        ch = self.f.read(1)
        if not ch:
            print("End of file")
            return False
        
        if (ch.lower == self.previous.lower):
            lineFollower.run()
        elif (self.previous == 'a'):
            lineFollower.run()
        else:
            turndir = findorientation(ch,self.previous)
            directions.TurnDebug(turndir)
        lineFollower.run()

        self.previous = ch
        return True

def findorientation(input,prev_input):
    turndir = ""
    if (input == 'u' and (prev_input == 'l' or prev_input =='L')):
        turndir = "right"
    elif (input == 'u' and (prev_input == 'r' or prev_input =='R')):
        turndir = "left"
    elif (input == 'l' and (prev_input == 'u' or prev_input =='U')):
        turndir = "left"
    elif (input == 'l' and (prev_input == 'd' or prev_input =='D')):
        turndir = "right"
    elif (input == 'r' and (prev_input == 'u' or prev_input =='U')):
        turndir = "right"
    elif (input == 'r' and (prev_input == 'd' or prev_input =='D')):
        turndir = "left"
    elif (input == 'd' and (prev_input == 'l' or prev_input =='L')):
        turndir = "left"
    elif (input == 'd' and (prev_input == 'r' or prev_input =='R')):
        turndir = "right"
    

    return turndir