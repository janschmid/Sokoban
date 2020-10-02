#!/usr/bin/env python3

import ev3dev.ev3 as ev3
from time import sleep
from PidFollowLine import LineFollower
from Directions import Turn
from ReadDirections import ReadInDirection


# Main function
if __name__ == "__main__":
    lineFollower = LineFollower()
    drive = ReadInDirection()
    a = True
    while (a):
        a = drive.run()
        
    
    
    #lineFollower.run()
    #directions = Turn()
    #directions.TurnDebug("left")
    #directions.TurnDebug("right")
        
    
