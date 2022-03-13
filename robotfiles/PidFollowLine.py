#!/usr/bin/python3
# by Jan-Ruben Schmid


from time import sleep

# Import the EV3-robot library
import ev3dev.ev3 as ev3


class LineFollower:
    # Constructor
    def __init__(self):
        self.btn = ev3.Button()
        self.shut_down = False
        # sensors
        self.lCs = ev3.ColorSensor("in1")
        assert self.lCs.connected
        self.rCs = ev3.ColorSensor("in2")
        assert self.rCs.connected
        self.lCs.mode = "COL-REFLECT"  # measure light intensity
        self.rCs.mode = "COL-REFLECT"

        # motors
        self.lm = ev3.LargeMotor("outC")
        assert self.lm.connected  # left motor
        self.rm = ev3.LargeMotor("outA")
        assert self.rm.connected  # right motor
        # mm = ev3.MediumMotor('outD'); assert mm.connected  # medium motor

        self.targetSpeed = 700  # deg/sec, [-1000, 1000]

        self.lightThreashold = 70  # 0=all black =-> will never turn
        self.stop_action = "coast"
        self.totalCanPushDistance = 920
        self.totalBackupDistance = 800

    def zrun(self, pushCan=False, runBackwards=False):
        if pushCan:
            startPosition = self.lm.position + self.rm.position
            if runBackwards:
                targetPosition = (
                    startPosition - self.totalBackupDistance
                )  # going backwards (robot design)
                print(
                    "runBackwards start: {0}, end: {1}".format(
                        startPosition, targetPosition
                    )
                )
            else:
                targetPosition = startPosition + self.totalCanPushDistance
        # P controller tuning
        Kp = 1.2  # proportional gain

        # initial measurment
        target_value = 0  # left and right color sensor should return same brightness -> driving in the middle of line
        # Start the main loop
        loopCount = 0
        if runBackwards:
            self.lm.run_forever(speed_sp=0)
            self.rm.run_forever(speed_sp=0)
            sleep(0.1)
        while not self.shut_down:
            # go forward until cross
            if (
                pushCan == False
                and self.lCs.value() + self.rCs.value() < self.lightThreashold
                and loopCount > 10
            ):
                # self.lm.run_forever(speed_sp=0)
                # self.rm.run_forever(speed_sp=0)
                # print ("Return loop count: {0} with threashold {1}".format(loopCount, self.lCs.value() + self.rCs.value()))
                return
            # else:
            # self.lightThreashold = (self.lCs.value() + self.rCs.value())*0.7

            if (
                pushCan
                and (runBackwards == False)
                and (self.lm.position + self.rm.position > targetPosition)
            ):
                return

            if (
                pushCan
                and (runBackwards == True)
                and (self.lm.position + self.rm.position < targetPosition)
            ):
                return
            loopCount += 1
            # Calculate steering using PID algorithm
            error = self.lCs.value() - self.rCs.value()

            u = Kp * error  # + (Ki * integral) + (Kd * derivative)

            if not runBackwards:
                speed = self.targetSpeed
            else:
                speed = self.targetSpeed * (-1)

            if (abs(speed) + abs(u)) > 1000:
                if speed > 0:
                    speed = speed + abs(u)
                else:
                    speed = speed - abs(u)

            # run motors
            if runBackwards == False:
                self.lm.run_forever(speed_sp=(speed - u))
                self.rm.run_forever(speed_sp=(speed + u))
            else:
                u = u / 8
                self.lm.run_forever(speed_sp=(speed + u))
                self.rm.run_forever(speed_sp=(speed - u))

    def run(self, lastPushOfCan=False):
        if not lastPushOfCan:
            self.zrun()
        else:
            self.zrun(True)  # push can forward
            self.zrun(True, True)  ##and move to target position back

    def sleep(self, time):
        self.lm.run_forever(speed_sp=0)
        self.rm.run_forever(speed_sp=0)
        sleep(time)
