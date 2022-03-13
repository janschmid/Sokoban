#!/usr/bin/env python3
""" Main function of robot, needs to be executed on ev3. 
"""
import time
from time import sleep

import ev3dev.ev3 as ev3
from Directions import Turn
from PidFollowLine import LineFollower
from ReadDirections import ReadInDirection


def RunFromFile():
    """Take robot commands as input"""
    lm = ev3.LargeMotor("outC")
    assert lm.connected  # left motor
    rm = ev3.LargeMotor("outA")
    assert rm.connected  # right motor
    drive = ReadInDirection()
    t0 = time.time()
    a = True
    while a:
        a = drive.run()
    t1 = time.time()
    lm.run_forever(speed_sp=(0))
    rm.run_forever(speed_sp=(0))
    return t1 - t0


def RunDebug():
    """Debug script to test multiple commands for fine tuning"""
    lm = ev3.LargeMotor("outC")
    assert lm.connected  # left motor
    rm = ev3.LargeMotor("outA")
    assert rm.connected  # right motor
    lineFollower = LineFollower()
    turn = Turn()

    # start....
    # lineFollower.zrun(False, True)
    # lineFollower.zrun(False, True)
    # lineFollower.zrun(False, True)
    lineFollower.run()
    lineFollower.run(True)
    turn.TurnAround()
    lineFollower.run()
    lineFollower.run(True)
    turn.TurnAround()
    lm.run_forever(speed_sp=0)
    rm.run_forever(speed_sp=0)


# Main function
if __name__ == "__main__":
    # RunDebug()
    elapsedTime = (int)(RunFromFile())

    sound = ev3.Sound()
    sound.speak("Mission completed in {0} seconds".format(elapsedTime))
    sleep(10)

    exit()
