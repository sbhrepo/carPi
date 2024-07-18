import time
import control
import motor
import stopwatch
import recorder

class Drive:
    def __init__(self):
        self.controlF = control.Control(26, 5)
        self.controlB = control.Control(18, 12)
        self.motorFR = motor.Motor(6, 13, 19)
        self.motorFL = motor.Motor(21, 20, 16)
        self.motorBR = motor.Motor(23, 24, 25)
        self.motorBL = motor.Motor(17, 27, 22)
        self.timer = stopwatch.StopWatch()
        self.recorder = recorder.Recorder()
        self.recording = "idle"
        self.lastAction = "stop"
        self.lastSpeed = 0

    def startRecording(self, recordName):
        if self.recording != "idle":
            return f"Can't start new recording during recording\play recording."
        self.recording = "recording"
        self.action = None
        self.speed = None
        self.recordName = recordName
        return "OK"

    def stopRecording(self):
        if self.recording != "recording":
            return f"There are no recording in progress."
        if self.action != None and self.speed != None:
            self.recorder.add({"action":self.action, "time":round(self.timer.stop()), "speed":self.speed})
            self.recorder.save(self.recordName)
        self.recording = "idle"
        return "Done."

    def cancelRecording(self):
        if self.recording == "idle":
            return f"There are no recording in progress."
        self.cancel = True
        self.recorder.cancel()
        self.timer.cancel()
        self.recording = "idle"
        return "Done."

    def deleteRecording(self, name):
        if self.recording != "idle":
            return f"Can't delete recording during recording\play recording."
        self.recorder.deleteRecord(name)
        return "Done."

    def renameRecording(self, oldName, newName):
        if self.recording != "idle":
            return f"Can't rename recording during recording\play recording."
        self.recorder.renameRecord(oldName, newName)
        return "Done."

    def playRecording(self, name, repeats):
        if self.recording != "idle":
            return f"Can't play recording during recording\play recording."
        self.recording = "playing"
        self.cancel = False
        data = self.recorder.load(name)
        for repeat in range (int(repeats)):
            for step in data:
                func = getattr(self, step["action"])
                func(step["speed"], step["time"])
                t_end = time.time() + step["time"]
                while time.time() < t_end:
                    time.sleep(1)
                    if self.cancel == True:
                        self.recording = "idle"
                        self.stop(0,0)
                        return f"play recording canceled [{name}]"
        self.recording = "idle"
        self.stop(0,0)
        return f"play recording ended [{name}]"

    def recordAction(self, action, speed):
        if self.recording != "recording":
            return
        if self.action != None and self.speed != None:
            self.recorder.add({"action":self.action, "time":round(self.timer.stop()), "speed":self.speed})
        self.action = action
        self.speed = speed
        self.timer.start()

    def powerOn(self):
        self.controlF.powerOn()
        self.controlB.powerOn()
        msg = self.standbyOn()
        #return f"Power ON controlers\n{msg}"
        return "Power ON controlers"

    def powerOff(self):
        msg = self.standbyOff()
        self.controlF.powerOff()
        self.controlB.powerOff()
        #return f"{msg}\nPower OFF controlers" # unless we want to add msg in all functions from all calls including for exaple poweroff x2
        return "Power OFF controlers"

    def standbyOn(self):
        self.controlF.standbyOn()
        self.controlB.standbyOn()
        return "Standby on, Enable motors signal"

    def standbyOff(self):
        self.controlF.standbyOff()
        self.controlB.standbyOff()
        return "Standby off, Disable motors signal"

    def stop(self, speed, time):
        self.motorFR.stopMotor()
        self.motorFL.stopMotor()
        self.motorBR.stopMotor()
        self.motorBL.stopMotor()
        self.recordAction("stop", 0)
        self.lastAction = "stop"
        self.lastSpeed = speed
        return "STOPPED"

    def front(self, speed, time):
        self.motorFR.rotateMotorCW(speed)
        self.motorFL.rotateMotorCCW(speed)
        self.motorBR.rotateMotorCW(speed)
        self.motorBL.rotateMotorCCW(speed)
        self.recordAction("front", speed)
        self.lastAction = "front"
        self.lastSpeed = speed
        return f"DRIVING FRONT at speed %{speed}"

    def back(self, speed, time):
        self.motorFR.rotateMotorCCW(speed)
        self.motorFL.rotateMotorCW(speed)
        self.motorBR.rotateMotorCCW(speed)
        self.motorBL.rotateMotorCW(speed)
        self.recordAction("back", speed)
        self.lastAction = "back"
        self.lastSpeed = speed
        return f"DRIVING BACK at speed %{speed}"

    def right(self, speed, time):
        self.motorFR.rotateMotorCCW(speed)
        self.motorFL.rotateMotorCCW(speed)
        self.motorBR.rotateMotorCW(speed)
        self.motorBL.rotateMotorCW(speed)
        self.recordAction("right", speed)
        self.lastAction = "right"
        self.lastSpeed = speed
        return f"DRIVING RIGHT at speed %{speed}"

    def left(self, speed, time):
        self.motorFR.rotateMotorCW(speed)
        self.motorFL.rotateMotorCW(speed)
        self.motorBR.rotateMotorCCW(speed)
        self.motorBL.rotateMotorCCW(speed)
        self.recordAction("left", speed)
        self.lastAction = "left"
        self.lastSpeed = speed
        return f"DRIVING LEFT at speed %{speed}"

    def frontRight(self, speed, time):
        self.motorFR.stopMotor()
        self.motorFL.rotateMotorCCW(speed)
        self.motorBR.rotateMotorCW(speed)
        self.motorBL.stopMotor()
        self.recordAction("frontRight", speed)
        self.lastAction = "frontRight"
        self.lastSpeed = speed
        return f"DRIVING FRONT-RIGHT at speed %{speed}"

    def frontLeft(self, speed, time):
        self.motorFR.rotateMotorCW(speed)
        self.motorFL.stopMotor()
        self.motorBR.stopMotor()
        self.motorBL.rotateMotorCCW(speed)
        self.recordAction("frontLeft", speed)
        self.lastAction = "frontLeft"
        self.lastSpeed = speed
        return f"DRIVING FRONT-LEFT at speed %{speed}"

    def backRight(self, speed, time):
        self.motorFR.rotateMotorCCW(speed)
        self.motorFL.stopMotor()
        self.motorBR.stopMotor()
        self.motorBL.rotateMotorCW(speed)
        self.recordAction("backRight", speed)
        self.lastAction = "backRight"
        self.lastSpeed = speed
        return f"DRIVING BACK-RIGHT at speed %{speed}"

    def backLeft(self, speed, time):
        self.motorFR.stopMotor()
        self.motorFL.rotateMotorCW(speed)
        self.motorBR.rotateMotorCCW(speed)
        self.motorBL.stopMotor()
        self.recordAction("backLeft", speed)
        self.lastAction = "backLeft"
        self.lastSpeed = speed
        return f"DRIVING BACK-LEFT at speed %{speed}"

    def turnRight(self, speed, turn_time):
        self.motorFR.rotateMotorCCW(speed)
        self.motorFL.rotateMotorCCW(speed)
        self.motorBR.rotateMotorCCW(speed)
        self.motorBL.rotateMotorCCW(speed)
        self.recordAction("turnRight", speed)
        if turn_time > 0:
            time.sleep(turn_time)
            # we are recording the last action and speed, and in play mode it will play twice (one from recording and one from last action)
            func = getattr(self, self.lastAction)
            func(self.lastSpeed, 0)
        return f"TURNING RIGHT at speed %{speed}"

    def turnLeft(self, speed, turn_time):
        self.motorFR.rotateMotorCW(speed)
        self.motorFL.rotateMotorCW(speed)
        self.motorBR.rotateMotorCW(speed)
        self.motorBL.rotateMotorCW(speed)
        self.recordAction("turnLeft", speed)
        if turn_time > 0:
            time.sleep(turn_time)
            # we are recording the last action and speed, and in play mode it will play twice (one from recording and one from last action)
            func = getattr(self, self.lastAction)
            func(self.lastSpeed, 0)
        return f"TURNING LEFT at speed %{speed}"

    def status(self):
        statusReport = f"control front:\n"
        statusReport += self.controlF.status()
        statusReport += f"Motor front-right:\n"
        statusReport += self.motorFL.status()
        statusReport += f"Motor front-left:\n"
        statusReport += self.motorFL.status()

        statusReport += f"control back:\n"
        statusReport += self.controlB.status()
        statusReport += f"Motor back-right:\n"
        statusReport += self.motorBR.status()
        statusReport += f"Motor back-left:\n"
        statusReport += self.motorBL.status()
        return statusReport