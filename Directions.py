#!/usr/bin/python3
# by Jan-Ruben Schmid


# Import the EV3-robot library
import ev3dev.ev3 as ev3
from time import sleep

class Turn:
    def __init__(self):
        # lCs = ev3.ColorSensor("in1");    assert lCs.connected
        # rCs = ev3.ColorSensor("in2");   assert rCs.connected
        # lCs.mode = 'COL-REFLECT'  # measure light intensity
        # rCs.mode = 'COL-REFLECT'

        self.gy = ev3.GyroSensor('in3')
        # self.gy.mode = 'GYRO-ANG'; assert self.gy.connected
        # sleep(5) #wait 5 seconds until calibrated
        # # motors
        self.lm = ev3.LargeMotor('outA');  assert self.lm.connected  # left motor
        self.rm = ev3.LargeMotor('outC');  assert self.rm.connected  # right motor
        
        self.speed = 500  # deg/sec, [-1000, 1000]
        self.dt = 100 #ms

        self.stop_action = "coast"
        
    def TurnDebug(self, direction):
        ang = self.gy.value()
        targetAng = ang
        if(direction == "left"):
            targetAng +=90
            while(ang<targetAng):
                self.lm.run_timed(time_sp=self.dt*1.5, speed_sp=0, stop_action=self.stop_action)
                self.rm.run_timed(time_sp=self.dt*1.5, speed_sp=self.speed, stop_action=self.stop_action)
                sleep(self.dt / 1000)
                ang = self.gy.value()
            return

        elif(direction == "right"):
            targetAng -=90
            while(ang>targetAng):
                self.rm.run_timed(time_sp=self.dt*1.5, speed_sp=0, stop_action=self.stop_action)
                self.lm.run_timed(time_sp=self.dt*1.5, speed_sp=self.speed, stop_action=self.stop_action)
                sleep(self.dt / 1000)
                ang= self.gy.value()
            return

        else:
            raise Exception("unknown direction")


