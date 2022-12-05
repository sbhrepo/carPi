from gpiozero import PWMOutputDevice, DigitalOutputDevice

class Motor:
    def __init__(self, PWM_PIN, IN2_PIN, IN1_PIN):
        self.PWM_PIN = PWM_PIN
        self.IN1_PIN = IN1_PIN
        self.IN2_PIN = IN2_PIN

        self.pwm_pin_mot = PWMOutputDevice (self.PWM_PIN,True, 0, 1200)
        self.cw_pin_mot = DigitalOutputDevice (self.IN1_PIN, True, 0)
        self.ccw_pin_mot = DigitalOutputDevice (self.IN2_PIN, True, 0)

    def rotateMotorCW(self, speed):
        pwm_percnt = int(speed)/100.0
        self.pwm_pin_mot.value = pwm_percnt
        self.cw_pin_mot.value = 1
        self.ccw_pin_mot.value = 0

    def rotateMotorCCW(self, speed):
        pwm_percnt = int(speed)/100.0
        self.pwm_pin_mot.value = pwm_percnt
        self.cw_pin_mot.value = 0
        self.ccw_pin_mot.value = 1

    def stopMotor(self):
        self.pwm_pin_mot.value = 0
        self.cw_pin_mot.value = 0
        self.ccw_pin_mot.value = 0

    def status(self):
        statusReport = f"  PWM_PIN ({self.PWM_PIN}) value is {self.pwm_pin_mot.value}\n"
        statusReport += f"  IN1_PIN ({self.IN1_PIN}) value is {self.cw_pin_mot.value}\n"
        statusReport += f"  IN2_PIN ({self.IN2_PIN}) value is {self.ccw_pin_mot.value}\n"
        return statusReport