#!/usr/bin/env python3

import ev3dev.ev3 as ev3
from time import sleep
from PidFollowLine import LineFollower
from Directions import Turn
from ReadDirections import ReadInDirection


def RunFromFile():
    lm = ev3.LargeMotor('outC');  assert lm.connected  # left motor
    rm = ev3.LargeMotor('outA');  assert rm.connected  # right motor
    drive = ReadInDirection()

    a = True
    while (a):
        a = drive.run()
    lm.run_forever(speed_sp=(0))
    rm.run_forever(speed_sp=(0))


def RunDebug():
    lm = ev3.LargeMotor('outC');  assert lm.connected  # left motor
    rm = ev3.LargeMotor('outA');  assert rm.connected  # right motor
    lineFollower = LineFollower()
    turn = Turn()

    #start....
    lineFollower.zrun(True)
    lineFollower.zrun(True)
    turn.TurnDebug("left")
    #end...

# Main function
if __name__ == "__main__":
    
    RunFromFile()
        
    sound = ev3.Sound()
    sound.speak("Mission completed")
    sleep(10)

    
    exit()
        
    
