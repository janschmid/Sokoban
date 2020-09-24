#!/usr/bin/env python3

import ev3dev.ev3 as ev3
from time import sleep
from PidFollowLine import LineFollower
from Directions import Turn
# Main function
if __name__ == "__main__":
    lineFollower = LineFollower()
    # lineFollower.run()
    directions = Turn()
    lineFollower.run()
    lineFollower.run()
    
    directions.TurnDebug("left")