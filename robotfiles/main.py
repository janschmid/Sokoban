#!/usr/bin/env python3

import ev3dev.ev3 as ev3
from time import sleep
from PidFollowLine import LineFollower
from Directions import Turn
from ReadDirections import ReadInDirection


def RunFromFile(self):
    lm = ev3.LargeMotor('outC');  assert lm.connected  # left motor
    rm = ev3.LargeMotor('outA');  assert rm.connected  # right motor
    drive = ReadInDirection()

    a = True
    while (a):
        a = drive.run()
  


def RunDebug(self):
    lm = ev3.LargeMotor('outC');  assert lm.connected  # left motor
    rm = ev3.LargeMotor('outA');  assert rm.connected  # right motor
    lineFollower = LineFollower()
    turn = Turn()

    #start....
    lineFollower._run(True)
    lineFollower._run(True)
    turn.TurnDebug("left")
    #end...

# Main function
if __name__ == "__main__":
    
    RunDebug()
        
    sound = ev3.Sound()
    sound.speak("Mission completed")
    exit()
    #lineFollower.run()
    #directions = Turn()
    #directions.TurnDebug("left")
    #directions.TurnDebug("right")
        
    
