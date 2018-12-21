#simple logging class, records output
import datetime

class Log:
    def __init__(self, name = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")):
        print("initializing Log")
        self.file = open("datalog/logs/" + str(name), "w+")
        self.printWrite("started log: " + str(name))
        print("done")

    def printWrite(self, line):
        self.record(line)
        print(line)

    def record(self, line):
        self.file.write(line+"\r\n")

    def __del__(self):
        print("stopping Log")
        self.printWrite("end log")
        self.file.close()
        print("done")
        
