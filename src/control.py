from gpiozero import LED

class Control():
    def __init__(self, CONTROLER, STANDBY):
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
