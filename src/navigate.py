import drive
import control
import motor
import time

class Navigate(drive.Drive):
    def __init__(self):
        super().__init__()
        self.isStop = True  

    def startRoute(self, routeName, speed, timeToRun):
        self.isStop = False        
        if routeName == "BackAndForth":
            print("B&F ", routeName, " speed=", speed, " time=", timeToRun)
            while(self.isStop == False):
                self.front(speed, 0)
                counter = 0
                while(counter < timeToRun): # sleep loop to stop in middle if needed
                    counter += 1
                    time.sleep(1)
                    if self.isStop:
                        self.stop()
                        return f"Route Stopped in middle"
                print("in backand forth back")
                self.back(speed, 0)
                counter = 0
                while(counter < timeToRun): # sleep loop to stop in middle if needed
                    counter += 1
                    time.sleep(1)
                    if self.isStop:
                        self.stop()
                        return f"Route Stopped in middle"
        return f"Route {routeName} did not start"

    def stoptRoute(self):
        self.isStop = True
        return f"Stopping Route"
