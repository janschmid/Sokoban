#!/usr/bin/env python3

from Directions import Turn
from PidFollowLine import LineFollower


class ReadInDirection:
    def findorientation(self, input):
        turndir = ""
        if input.lower() == "u" and (self.orientation == "l"):
            turndir = "right"
            self.orientation = "u"
        elif input.lower() == "u" and (self.orientation == "r"):
            turndir = "left"
            self.orientation = "u"
        elif input.lower() == "l" and (self.orientation == "u"):
            turndir = "left"
            self.orientation = "l"
        elif input.lower() == "l" and (self.orientation == "d"):
            turndir = "right"
            self.orientation = "l"
        elif input.lower() == "r" and (self.orientation == "u"):
            turndir = "right"
            self.orientation = "r"
        elif input.lower() == "r" and (self.orientation == "d"):
            turndir = "left"
            self.orientation = "r"
        elif input.lower() == "d" and (self.orientation == "l"):
            turndir = "left"
            self.orientation = "d"
        elif input.lower() == "d" and (self.orientation == "r"):
            turndir = "right"
            self.orientation = "d"
        elif input.lower() == "d" and (self.orientation == "u"):
            turndir = "spin"
            self.orientation = "d"
        elif input.lower() == "u" and (self.orientation == "d"):
            turndir = "spin"
            self.orientation = "u"
        elif input.lower() == "r" and (self.orientation == "l"):
            turndir = "spin"
            self.orientation = "r"
        elif input.lower() == "l" and (self.orientation == "r"):
            turndir = "spin"
            self.orientation = "l"
        return turndir

    # Constructor
    def __init__(self):
        charlist = []
        self.MoveList = []
        self.ExecutionList = []
        self.f = open("Sokoban_Moves.txt", "r")
        ch = self.f.read(1)
        while ch:
            charlist.append(ch)
            ch = self.f.read(1)

        charlist.append("End")
        self.orientation = "l"
        for i in range(len(charlist)):
            if charlist[i] == "End":
                break
            if charlist[i].lower() == self.orientation:
                self.ExecutionList.append("Straight")
            else:
                self.ExecutionList.append(self.findorientation(charlist[i]))
            if charlist[i].isupper():
                if charlist[i + 1] != charlist[i]:
                    self.ExecutionList.append("LastPush")
        self.ExecutionList.append("End")
        self.i = 0
        self.lineFollower = LineFollower()
        self.directions = Turn()
        for item in self.ExecutionList:
            print("{0}\n", item)

    # Main method
    def run(self):

        if self.ExecutionList[self.i] == "End":
            return False

        if self.ExecutionList[self.i] == "LastPush":
            self.lineFollower.run(True)
            print("LastPush")
        elif (self.ExecutionList[self.i] == "left") or (
            self.ExecutionList[self.i] == "right"
        ):
            if self.i > 0:
                if self.ExecutionList[self.i - 1] == "LastPush":
                    self.directions.TurnDebug(self.ExecutionList[self.i], True)
                else:
                    self.directions.TurnDebug(self.ExecutionList[self.i], False)
            else:
                self.directions.TurnDebug(self.ExecutionList[self.i], False)
            self.lineFollower.run(False)
            print("Turn")
        elif self.ExecutionList[self.i] == "spin":
            self.directions.TurnAround()
            self.lineFollower.run(False)
            # self.lineFollower.sleep(0.3)
        else:  # Straight
            self.lineFollower.run(False)
            print("Straight")

        self.i += 1
        return True
