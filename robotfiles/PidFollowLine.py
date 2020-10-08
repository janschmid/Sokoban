#!/usr/bin/python3
# by Jan-Ruben Schmid


# Import the EV3-robot library
import ev3dev.ev3 as ev3
from time import sleep


class LineFollower:
    # Constructor
    def __init__(self):
        self.btn = ev3.Button()
        self.shut_down = False
        # sensors
        self.lCs = ev3.ColorSensor("in1");    assert self.lCs.connected
        self.rCs = ev3.ColorSensor("in2");   assert self.rCs.connected
        self.lCs.mode = 'COL-REFLECT'  # measure light intensity
        self.rCs.mode = 'COL-REFLECT'

        # motors
        self.lm = ev3.LargeMotor('outC');  assert self.lm.connected  # left motor
        self.rm = ev3.LargeMotor('outA');  assert self.rm.connected  # right motor
        # mm = ev3.MediumMotor('outD'); assert mm.connected  # medium motor
        
        self.targetSpeed = -600  # deg/sec, [-1000, 1000]
        
        self.lightThreashold = 50 #when return values of both line sensors is smaller then threashold -> corner
        self.dt = 10 #ms
        self.stop_action = "coast"
        self.totalCanPushDistance = 920


    def run(self, lastPushOfCan=False):
        if(not lastPushOfCan):
            _run()
        else:
            _run(True)#push can forward
            _run(True, True)##and move to target position back


    def _run(self, pushCan=False, runBackwards=False):
        
        if(pushCan):
            startPosition = self.lm.position+self.rm.position
            if(not runBackwards):
                targetPosition = startPosition-self.totalCanPushDistance #going backwards (robot design)
            else:
                targetPosition = startPosition+self.totalCanPushDistance
        # P controller tuning
        Kp = 1.2  # proportional gain

        integral = 0
        previous_error = 0   
        # initial measurment
        target_value = 0 # left and right color sensor should return same brightness -> driving in the middle of line
        # Start the main loop
        loopCount = 0
        while not self.shut_down:
            if (self.lCs.value() + self.rCs.value()< self.lightThreashold and loopCount>20):
                print ("Return loop count: {0} with threashold {1}".format(loopCount, self.lightThreashold))
                return
            else:
                self.lightThreashold = (self.lCs.value() + self.rCs.value())*0.7
            
            if(pushCan and (self.lm.position+self.rm.position<targetPosition)):
                return
            loopCount+=1
            # Calculate steering using PID algorithm
            error = (self.lCs.value() - self.rCs.value())

            u = (Kp * error) #+ (Ki * integral) + (Kd * derivative)
            if(not runBackwards):
                speed = self.targetSpeed
            else:
                speed = self.targetSpeed*(-1)

            if((abs(speed)+abs(u))>1000):
                if(speed>0):
                    speed = speed-abs(u)
                else:
                    speed = speed+abs(u)

            # run motors
            self.lm.run_forever(speed_sp=(speed + u))
            self.rm.run_forever(speed_sp=(speed - u))

