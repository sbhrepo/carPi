import os
import json

class Recorder:
    def __init__(self):
        self.setDirectory()
        self.recoeds = []

    def setDirectory(self):
        if not os.path.exists("../records"):
            os.makedirs("../records")

    def add(self, record):
        self.recoeds.append(record)

    def save(self, name):
        json_object = json.dumps(self.recoeds, indent=4)
        with open ("../records/"+name+".json", "w") as outfile:
            outfile.write(json_object)
        self.recoeds.clear()

    def getRecords(self):
        dir_list = os.listdir("../records")
        return ' '.join(dir_list)

    def deleteRecord(self, name):
        os.remove("../records/"+name)

    def renameRecord(self, oldName, newName):
        os.rename("../records/"+oldName, "../records/"+newName)
