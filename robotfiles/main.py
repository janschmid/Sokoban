#!/usr/bin/env python3

import ev3dev.ev3 as ev3
from time import sleep
from PidFollowLine import LineFollower
from Directions import Turn
from ReadDirections import ReadInDirection


# Main function
if __name__ == "__main__":
    lm = ev3.LargeMotor('outC');  assert lm.connected  # left motor
    rm = ev3.LargeMotor('outA');  assert rm.connected  # right motor
    lineFollower = LineFollower()
    drive = ReadInDirection()
    a = True
    count=0
    while (a):
        a = drive.run()

    lm.run_forever(speed_sp=0)
    rm.run_forever(speed_sp=0)
        
    
    
    #lineFollower.run()
    #directions = Turn()
    #directions.TurnDebug("left")
    #directions.TurnDebug("right")
        
    
