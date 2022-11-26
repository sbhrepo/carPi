from gpiozero import PWMOutputDevice, DigitalOutputDevice, LED
from time import sleep

### BT6612FNG - 1
### power up/down the drive controler ###
controler1 = LED(26)
### StandBy on/off ###
standby1 = LED(5)

### BT6612FNG - 2
controler2 = LED(18)
standby2 = LED(12)


### MOTOR FR - Front Right ###
# GPIO 6 is used for Generating Software PWM
# GPIO 13 & GPIO 19 are used for Motor control pins as per schematic 
PWM_PIN_MOT1 = 6
IN1_PIN_MOT1 = 13
IN2_PIN_MOT1 = 19
# PWMOutputDevice takes  BCM_PIN number
fr_pwm_pin_mot1 = PWMOutputDevice (PWM_PIN_MOT1,True, 0, 1200)
# DigitalOutputDevice take
fr_cw_pin_mot1 = DigitalOutputDevice (IN1_PIN_MOT1, True, 0)
fr_ccw_pin_mot1 = DigitalOutputDevice (IN2_PIN_MOT1, True, 0)

def frRotateMotorCW(speed):
    pwm_percnt = int(speed)/100.0
    fr_pwm_pin_mot1.value = pwm_percnt
    fr_cw_pin_mot1.value = 1
    fr_ccw_pin_mot1.value = 0

def frRotateMotorCCW(speed):
    pwm_percnt = int(speed)/100.0
    fr_pwm_pin_mot1.value = pwm_percnt
    fr_cw_pin_mot1.value = 0
    fr_ccw_pin_mot1.value = 1

def frStopMotor():
    fr_cw_pin_mot1.value = 0
    fr_ccw_pin_mot1.value = 0
    fr_pwm_pin_mot1.value = 0



### MOTOR FL - Front Left ###
# GPIO 16 is used for Generating Software PWM
# GPIO 20 & GPIO 21 are used for Motor control pins as per schematic
PWM_PIN_MOT2 = 16
IN1_PIN_MOT2 = 20
IN2_PIN_MOT2 = 21
# PWMOutputDevice takes  BCM_PIN number
fl_pwm_pin_mot2 = PWMOutputDevice (PWM_PIN_MOT2,True, 0, 1200)
# DigitalOutputDevice take
fl_cw_pin_mot2 = DigitalOutputDevice (IN1_PIN_MOT2, True, 0)
fl_ccw_pin_mot2 = DigitalOutputDevice (IN2_PIN_MOT2, True, 0)

def flRotateMotorCW(speed):
    pwm_percnt = int(speed)/100.0
    fl_pwm_pin_mot2.value = pwm_percnt
    fl_cw_pin_mot2.value = 1
    fl_ccw_pin_mot2.value = 0

def flRotateMotorCCW(speed):
    pwm_percnt = int(speed)/100.0
    fl_pwm_pin_mot2.value = pwm_percnt
    fl_cw_pin_mot2.value = 0
    fl_ccw_pin_mot2.value = 1

def flStopMotor():
    fl_cw_pin_mot2.value = 0
    fl_ccw_pin_mot2.value = 0
    fl_pwm_pin_mot2.value = 0



### MOTOR BR - Back Right ###
# GPIO 23 is used for Generating Software PWM
# GPIO 24 & GPIO 25 are used for Motor control pins as per schematic
PWM_PIN_MOT3 = 23
IN1_PIN_MOT3 = 24
IN2_PIN_MOT3 = 25
# PWMOutputDevice takes  BCM_PIN number
br_pwm_pin_mot3 = PWMOutputDevice (PWM_PIN_MOT3,True, 0, 1200)
# DigitalOutputDevice take
br_cw_pin_mot3 = DigitalOutputDevice (IN1_PIN_MOT3, True, 0)
br_ccw_pin_mot3 = DigitalOutputDevice (IN2_PIN_MOT3, True, 0)

def brRotateMotorCW(speed):
    pwm_percnt = int(speed)/100.0
    br_pwm_pin_mot3.value = pwm_percnt
    br_cw_pin_mot3.value = 1
    br_ccw_pin_mot3.value = 0

def brRotateMotorCCW(speed):
    pwm_percnt = int(speed)/100.0
    br_pwm_pin_mot3.value = pwm_percnt
    br_cw_pin_mot3.value = 0
    br_ccw_pin_mot3.value = 1

def brStopMotor():
    br_cw_pin_mot3.value = 0
    br_ccw_pin_mot3.value = 0
    br_pwm_pin_mot3.value = 0



### MOTOR BL - Back Left ###
# GPIO 17 is used for Generating Software PWM
# GPIO 27 & GPIO 22 are used for Motor control pins as per schematic
PWM_PIN_MOT4 = 17
IN1_PIN_MOT4 = 27
IN2_PIN_MOT4 = 22
# PWMOutputDevice takes  BCM_PIN number
bl_pwm_pin_mot4 = PWMOutputDevice (PWM_PIN_MOT4, True, 0, 1200)
# DigitalOutputDevice take
bl_cw_pin_mot4 = DigitalOutputDevice (IN1_PIN_MOT4, True, 0)
bl_ccw_pin_mot4 = DigitalOutputDevice (IN2_PIN_MOT4, True, 0)

def blRotateMotorCW(speed):
    pwm_percnt = int(speed)/100.0
    bl_pwm_pin_mot4.value = pwm_percnt
    bl_cw_pin_mot4.value = 1
    bl_ccw_pin_mot4.value = 0

def blRotateMotorCCW(speed):
    pwm_percnt = int(speed)/100.0
    bl_pwm_pin_mot4.value = pwm_percnt
    bl_cw_pin_mot4.value = 0
    bl_ccw_pin_mot4.value = 1

def blStopMotor():
    bl_cw_pin_mot4.value = 0
    bl_ccw_pin_mot4.value = 0
    bl_pwm_pin_mot4.value = 0



def drive(direction, speed):
    if direction.lower() == "start":
       controler1.on()
       controler2.on()
       return f"Power UP drive controler"
    elif direction.lower() == "end":
       controler1.off()
       controler2.off()
       return f"Power DOWN drive controler"
    elif direction.lower() == "standbyon":
       standby1.on()
       standby2.on()
       return f"Standby on"
    elif direction.lower() == "standbyoff":
       standby1.off()
       standby2.off()
       return f"Standby off"
    elif direction.lower() == "stop":
       frStopMotor()
       flStopMotor()
       brStopMotor()
       blStopMotor()
       return f"STOP {speed}"
    elif direction.lower() == "f": # Front
       frRotateMotorCCW(speed)
       flRotateMotorCW(speed)
       brRotateMotorCCW(speed)
       blRotateMotorCW(speed)
       return f"DRIVE FRONT at speed %{speed}"
    elif direction.lower() == "b": # Back
       frRotateMotorCW(speed)
       flRotateMotorCCW(speed)
       brRotateMotorCW(speed)
       blRotateMotorCCW(speed)
       return f"DRIVE BACK at speed %{speed}"
    elif direction.lower() == "r": # Right
       frRotateMotorCW(speed)
       flRotateMotorCW(speed)
       brRotateMotorCCW(speed)
       blRotateMotorCCW(speed)
       return f"DRIVE RIGHT at speed %{speed}"
    elif direction.lower() == "l": # Left
       frRotateMotorCCW(speed)
       flRotateMotorCCW(speed)
       brRotateMotorCW(speed)
       blRotateMotorCW(speed)
       return f"DRIVE LEFT at speed %{speed}"
    elif direction.lower() == "fr": # Front-Right
       frStopMotor()
       flRotateMotorCW(speed)
       brRotateMotorCCW(speed)
       blStopMotor()
       return f"DRIVE FRONT-RIGHT at speed %{speed}"
    elif direction.lower() == "fl": # Front-Left
       frRotateMotorCCW(speed)
       flStopMotor()
       brStopMotor()
       blRotateMotorCW(speed)
       return f"DRIVE FRONT-LEFT at speed %{speed}"
    elif direction.lower() == "br": # Back-Right
       frRotateMotorCW(speed)
       flStopMotor()
       brStopMotor()
       blRotateMotorCCW(speed)
       return f"DRIVE BACK-RIGHT at speed %{speed}"
    elif direction.lower() == "bl": # Back-Left
       frStopMotor()
       flRotateMotorCCW(speed)
       brRotateMotorCW(speed)
       blStopMotor()
       return f"DRIVE BACK-LEFT at speed %{speed}"
    elif direction.lower() == "right": # turn to the right
       frRotateMotorCW(speed)
       flRotateMotorCW(speed)
       brRotateMotorCW(speed)
       blRotateMotorCW(speed)
       return f"TURN RIGHT at speed %{speed}"
    elif direction.lower() == "left": # turn to the left
       frRotateMotorCCW(speed)
       flRotateMotorCCW(speed)
       brRotateMotorCCW(speed)
       blRotateMotorCCW(speed)
       return f"TURN LEFT at speed %{speed}"
    else:
       return "Not a valid command"
