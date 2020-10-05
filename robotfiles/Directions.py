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
        self.lm = ev3.LargeMotor('outC');  assert self.lm.connected  # left motor
        self.rm = ev3.LargeMotor('outA');  assert self.rm.connected  # right motor
        
        self.speed = -700  # deg/sec, [-1000, 1000]
        self.stop_action = "hold"
        self.totalDegrees = 430
        
        turnFactor = 0.9 # if value 0, overshoot
        self.outerDegrees = self.totalDegrees*turnFactor
        self.innerDegrees = self.totalDegrees*(turnFactor-1)
        
    def TurnDebug(self, direction):
        print ("out: {0}, in: {1} \n".format(self.outerDegrees, self.innerDegrees))
        if(direction == "left"):
            self.rm.run_to_rel_pos(position_sp=self.outerDegrees, speed_sp=self.speed, stop_action=self.stop_action)
            self.lm.run_to_rel_pos(position_sp=self.innerDegrees, speed_sp=self.speed, stop_action=self.stop_action)
            self.rm.wait_while('running')
            self.lm.wait_while('running')
            return

        elif(direction == "right"):
            self.lm.run_to_rel_pos(position_sp=self.outerDegrees, speed_sp=self.speed, stop_action=self.stop_action)
            self.rm.run_to_rel_pos(position_sp=self.innerDegrees, speed_sp=self.speed, stop_action=self.stop_action)
            self.rm.wait_while('running')
            self.lm.wait_while('running')
            return

        else:
            raise Exception("unknown direction")


    def Backup(self):
        time = 0
        dt=80
        while(time < dt*11):
            self.rm.run_timed(time_sp=dt*1.5, speed_sp=self.speed*(-1), stop_action=self.stop_action)
            self.lm.run_timed(time_sp=dt*1.5, speed_sp=self.speed*(-1), stop_action=self.stop_action)
            sleep(dt / 1000)
            time += dt
        return

    def TurnAround(self):
        self.rm.run_to_rel_pos(position_sp=self.totalDegrees, speed_sp=self.speed, stop_action=self.stop_action)
        self.lm.run_to_rel_pos(position_sp=-self.totalDegrees, speed_sp=self.speed, stop_action=self.stop_action)
        self.rm.wait_while('running')
        self.lm.wait_while('running')
        return