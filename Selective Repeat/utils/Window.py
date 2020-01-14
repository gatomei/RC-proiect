import math
from utils.Logger import Logger


class Window:

    def __init__(self, sequenceN, windowSize):

        self.sequenceNo = sequenceN
        # secventa de numere a primului frame
        self.SeqFirst = 0
        self.packs = []
        self.logger = Logger("Window")
        self.maxSeq = math.pow(2, self.sequenceNo - 1)
        # secventa de numere a ultimului frame
        self.SeqLast = windowSize - 1
        self.window = dict()
        if windowSize < self.maxSeq and windowSize > 0:
            self.windowSize = windowSize
        else:
            self.logger.error("Window size should be greater than 0 and less then 2^(sequenceN-1)!")

    def storeRecvPkt(self, sentPack):

        if sentPack.sequenceNo != self.SeqFirst:
            self.sequenceNo = self.SeqFirst
        if sentPack not in self.packs or self.packs[sentPack.sequenceNo] != None:
            self.packs[sentPack.sequenceNo] = sentPack
            while self.sequenceNo != sentPack.sequenceNo:
                # completez cu pachetele lipsa pana ajung la pachetul receptionat
                if self.sequenceNo not in self.packs:
                    self.packs[self.sequenceNo] = None
                self.sequenceNo = self.sequenceNo + 1

                # verific daca am depasit dim max a frame-ului
                if self.sequenceNo >= self.maxSeq:
                    self.sequenceNo = self.sequenceNo % self.maxSeq


    def send(self):
        pass

    def receive(self):
        pass
