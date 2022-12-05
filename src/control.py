from gpiozero import LED

class Control():
    def __init__(self, CONTROLER, STANDBY):
        self.CONTROLER_PIN = CONTROLER
        self.STANDBY_PIN = STANDBY
        self.CONTROLER = LED(CONTROLER)
        self.STANDBY = LED(STANDBY)

    def powerOn(self):
        self.CONTROLER.on()

    def powerOff(self):
        self.CONTROLER.off()

    def standbyOn(self):
        self.STANDBY.on()

    def standbyOff(self):
        self.STANDBY.off()

    def status(self):
        statusReport = f"  CONTROLER power ({self.CONTROLER_PIN}) value is {self.CONTROLER.value}\n"
        statusReport += f"  STANDBY ({self.STANDBY_PIN}) value is {self.STANDBY.value}\n"
        return statusReport