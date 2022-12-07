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

    def startRecording(self, recordName):
        if self.recording != "idle":
            return f"Can't start new recording during recording\play recording."
        self.recording = "recording"
        self.action = None
        self.speed = None
        self.recordName = recordName
        return f"OK"

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
        self.recorder.cancel()
        self.timer.cancel()
        self.recording = "idle"
        return "Done."

    def playRecording(self, name):
        if self.recording != "idle":
            return f"Can't play recording during recording\play recording."
        self.recording = "playing"
        data = self.recorder.load(name)
        msg = ""
        for step in data:
            func = getattr(self, step["action"])
            msg += (func(step["speed"], step["time"])) + '\n'
        return msg

    def test(self, line):
        return f"output:[{line}]"

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
        return f"Power ON controlers"

    def powerOff(self):
        msg = self.standbyOff()
        self.controlF.powerOff()
        self.controlB.powerOff()
        #return f"{msg}\nPower OFF controlers" # unless we want to add msg in all functions from all calls including for exaple poweroff x2
        return f"Power OFF controlers"

    def standbyOn(self):
        self.controlF.standbyOn()
        self.controlB.standbyOn()
        return f"Standby on, Enable motors signal"

    def standbyOff(self):
        self.controlF.standbyOff()
        self.controlB.standbyOff()
        return f"Standby off, Disable motors signal"

    def stop(self, speed, time):
        self.motorFR.stopMotor()
        self.motorFL.stopMotor()
        self.motorBR.stopMotor()
        self.motorBL.stopMotor()
        self.recordAction("stop", 0)
        return f"STOPPED"

    def front(self, speed, time):
        self.motorFR.rotateMotorCW(speed)
        self.motorFL.rotateMotorCCW(speed)
        self.motorBR.rotateMotorCW(speed)
        self.motorBL.rotateMotorCCW(speed)
        self.recordAction("front", speed)
        return f"DRIVING FRONT at speed %{speed}"

    def back(self, speed, time):
        self.motorFR.rotateMotorCCW(speed)
        self.motorFL.rotateMotorCW(speed)
        self.motorBR.rotateMotorCCW(speed)
        self.motorBL.rotateMotorCW(speed)
        self.recordAction("back", speed)
        return f"DRIVING BACK at speed %{speed}"

    def right(self, speed, time):
        self.motorFR.rotateMotorCCW(speed)
        self.motorFL.rotateMotorCCW(speed)
        self.motorBR.rotateMotorCW(speed)
        self.motorBL.rotateMotorCW(speed)
        self.recordAction("right", speed)
        return f"DRIVING RIGHT at speed %{speed}"

    def left(self, speed, time):
        self.motorFR.rotateMotorCW(speed)
        self.motorFL.rotateMotorCW(speed)
        self.motorBR.rotateMotorCCW(speed)
        self.motorBL.rotateMotorCCW(speed)
        self.recordAction("left", speed)
        return f"DRIVING LEFT at speed %{speed}"

    def frontRight(self, speed, time):
        self.motorFR.stopMotor()
        self.motorFL.rotateMotorCCW(speed)
        self.motorBR.rotateMotorCW(speed)
        self.motorBL.stopMotor()
        self.recordAction("frontRight", speed)
        return f"DRIVING FRONT-RIGHT at speed %{speed}"

    def frontLeft(self, speed, time):
        self.motorFR.rotateMotorCW(speed)
        self.motorFL.stopMotor()
        self.motorBR.stopMotor()
        self.motorBL.rotateMotorCCW(speed)
        self.recordAction("frontLeft", speed)
        return f"DRIVING FRONT-LEFT at speed %{speed}"

    def backRight(self, speed, time):
        self.motorFR.rotateMotorCCW(speed)
        self.motorFL.stopMotor()
        self.motorBR.stopMotor()
        self.motorBL.rotateMotorCW(speed)
        self.recordAction("backRight", speed)
        return f"DRIVING BACK-RIGHT at speed %{speed}"

    def backLeft(self, speed, time):
        self.motorFR.stopMotor()
        self.motorFL.rotateMotorCW(speed)
        self.motorBR.rotateMotorCCW(speed)
        self.motorBL.stopMotor()
        self.recordAction("backLeft", speed)
        return f"DRIVING BACK-LEFT at speed %{speed}"

    def turnRight(self, speed, time):
        self.motorFR.rotateMotorCCW(speed)
        self.motorFL.rotateMotorCCW(speed)
        self.motorBR.rotateMotorCCW(speed)
        self.motorBL.rotateMotorCCW(speed)
        self.recordAction("turnRight", speed)
        return f"TURNING RIGHT at speed %{speed}"

    def turnLeft(self, speed, time):
        self.motorFR.rotateMotorCW(speed)
        self.motorFL.rotateMotorCW(speed)
        self.motorBR.rotateMotorCW(speed)
        self.motorBL.rotateMotorCW(speed)
        self.recordAction("turnLeft", speed)
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