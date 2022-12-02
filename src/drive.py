import control
import motor

class Drive():
    def __init__(self):
        self.controlF = control.Control(26, 5)
        self.controlB = control.Control(18, 12)
        self.motorFR = motor.Motor(6, 13, 19)
        self.motorFL = motor.Motor(21, 20, 16)
        self.motorBR = motor.Motor(23, 24, 25)
        self.motorBL = motor.Motor(17, 27, 22)

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

    def stop(self):
        self.motorFR.stopMotor()
        self.motorFL.stopMotor()
        self.motorBR.stopMotor()
        self.motorBL.stopMotor()
        return f"STOPPED"

    def front(self, speed, time):
        self.motorFR.rotateMotorCCW(speed)
        self.motorFL.rotateMotorCW(speed)
        self.motorBR.rotateMotorCCW(speed)
        self.motorBL.rotateMotorCW(speed)
        return f"DRIVING FRONT at speed %{speed}"

    def back(self, speed, time):
        self.motorFR.rotateMotorCW(speed)
        self.motorFL.rotateMotorCCW(speed)
        self.motorBR.rotateMotorCW(speed)
        self.motorBL.rotateMotorCCW(speed)
        return f"DRIVING BACK at speed %{speed}"

    def right(self, speed, time):
        self.motorFR.rotateMotorCW(speed)
        self.motorFL.rotateMotorCW(speed)
        self.motorBR.rotateMotorCCW(speed)
        self.motorBL.rotateMotorCCW(speed)
        return f"DRIVING RIGHT at speed %{speed}"

    def left(self, speed, time):
        self.motorFR.rotateMotorCCW(speed)
        self.motorFL.rotateMotorCCW(speed)
        self.motorBR.rotateMotorCW(speed)
        self.motorBL.rotateMotorCW(speed)
        return f"DRIVING LEFT at speed %{speed}"

    def frontRight(self, speed, time):
        self.motorFR.stopMotor()
        self.motorFL.rotateMotorCW(speed)
        self.motorBR.rotateMotorCCW(speed)
        self.motorBL.stopMotor()
        return f"DRIVING FRONT-RIGHT at speed %{speed}"

    def frontLeft(self, speed, time):
        self.motorFR.rotateMotorCCW(speed)
        self.motorFL.stopMotor()
        self.motorBR.stopMotor()
        self.motorBL.rotateMotorCW(speed)
        return f"DRIVING FRONT-LEFT at speed %{speed}"

    def backRight(self, speed, time):
        self.motorFR.rotateMotorCW(speed)
        self.motorFL.stopMotor()
        self.motorBR.stopMotor()
        self.motorBL.rotateMotorCCW(speed)
        return f"DRIVING BACK-RIGHT at speed %{speed}"

    def backLeft(self, speed, time):
        self.motorFR.stopMotor()
        self.motorFL.rotateMotorCCW(speed)
        self.motorBR.rotateMotorCW(speed)
        self.motorBL.stopMotor()
        return f"DRIVING BACK-LEFT at speed %{speed}"

    def turnRight(self, speed, time):
        self.motorFR.rotateMotorCW(speed)
        self.motorFL.rotateMotorCW(speed)
        self.motorBR.rotateMotorCW(speed)
        self.motorBL.rotateMotorCW(speed)
        return f"TURNING RIGHT at speed %{speed}"

    def turnLeft(self, speed, time):
        self.motorFR.rotateMotorCCW(speed)
        self.motorFL.rotateMotorCCW(speed)
        self.motorBR.rotateMotorCCW(speed)
        self.motorBL.rotateMotorCCW(speed)
        return f"TURNING LEFT at speed %{speed}"
