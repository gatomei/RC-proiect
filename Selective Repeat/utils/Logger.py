from datetime import datetime


class Logger:
    def __init__(self, name):
        self.file = name+".log"
        self.name = name.upper()
        with open(self.file, "w") as f:
            f.write(f"{datetime.now()}, [{self.name}] [INFO], Created log file\n")

    def info(self, data):
        with open(self.file, "a") as f:
            f.write(f"{datetime.now()}, [{self.name}] [INFO], {data}\n")

    def error(self, error):
        with open(self.file, "a") as f:
            f.write(f"{datetime.now()}, [{self.name}] [ERROR], {error}\n")