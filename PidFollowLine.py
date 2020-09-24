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
        self.lm = ev3.LargeMotor('outA');  assert self.lm.connected  # left motor
        self.rm = ev3.LargeMotor('outC');  assert self.rm.connected  # right motor
        # mm = ev3.MediumMotor('outD'); assert mm.connected  # medium motor
        
        self.targetSpeed = 1000  # deg/sec, [-1000, 1000]
        self.errorMultiplier = self.targetSpeed/150 # just try to keep max speed and corner aligned...
        
        self.lightThreashold = 20 #when return values of both line sensors is smaller then threashold -> corner
        self.dt = 200 #ms
        self.stop_action = "coast"

    # Main method
    def run(self):


        # PID tuning
        Kp = 1  # proportional gain
        Ki = 0  # integral gain
        Kd = 0  # derivative gain

        integral = 0
        previous_error = 0

        # initial measurment
        target_value = 0 # left and right color sensor should return same brightness -> driving in the middle of line
        # Start the main loop
        loopCount = 0

        while not self.shut_down:
            if (self.lCs.value()< self.lightThreashold and self.rCs.value() < self.lightThreashold and loopCount>5):
                return
            loopCount+=1
            # Calculate steering using PID algorithm
            error = (self.lCs.value() - self.rCs.value()) * self.errorMultiplier
            integral += (error * self.dt)
            derivative = (error - previous_error) / self.dt

            u = (Kp * error) + (Ki * integral) + (Kd * derivative)
            speed = self.targetSpeed

            if((self.targetSpeed+abs(u))>1000):
                speed = self.targetSpeed-abs(u)
            print ("speed: {0}, speed+u: {1}, speed - u: {2}".format(speed, speed+u, speed-u))
            # run motors
            self.lm.run_timed(time_sp=self.dt*1.3, speed_sp=(speed + u), stop_action=self.stop_action)
            self.rm.run_timed(time_sp=self.dt*1.3, speed_sp=(speed - u), stop_action=self.stop_action)
            sleep(self.dt / 1000)

            previous_error = error