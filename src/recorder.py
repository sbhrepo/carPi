import os
import json

class Recorder:
    def __init__(self):
        self.setDirectory()
        self.records = []

    def setDirectory(self):
        if not os.path.exists("../records"):
            os.makedirs("../records")

    def add(self, record):
        self.records.append(record)

    def save(self, name):
        json_object = json.dumps(self.records, indent=4)
        with open ("../records/"+name+".json", "w") as outfile:
            outfile.write(json_object)
        self.records.clear()

    def cancel(self):                
        self.records.clear()

    def load(self, name):
        with open("../records/"+name+".json") as file:
            data = json.load(file)
        file.close()
        return data

    def getRecords(self):
        return ' '.join([".".join(f.split(".")[:-1]) for f in os.listdir("../records")])

    def deleteRecord(self, name):
        os.remove("../records/"+name+".json")

    def renameRecord(self, oldName, newName):
        os.rename("../records/"+oldName+".json", "../records/"+newName+".json")
