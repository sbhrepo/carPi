import time

class StopWatch:
    def __init__(self):
        self.startTime = None
        self.stopTime = None

    def convert(sec):
        mins = sec // 60
        sec = sec % 60
        hours = mins // 60
        mins = mins % 60
        f"Time Lapsed = {int(hours)}:{int(mins)}:{sec}"

    def start(self):
        self.startTime = time.time()

    def stop(self):
        self.stopTime = time.time()
        self.timeLapsed = self.stopTime - self.startTime
        self.startTime = None
        self.endTime = None
        return self.timeLapsed

    def elapsed(self):
        return time.time() - self.startTime

    def cancel(self):                
        self.startTime = None
        self.stopTime = None