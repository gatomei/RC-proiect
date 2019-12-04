import math
from utils.Logger import Logger


class SenderWindow:

    def __init__(self, sequenceN, windowSize):

        self.sequenceNoBit = sequenceN
        # secventa de numere a primului frame
        self.SeqFirst = 0
        self.logger = Logger("SenderWindow")
        self.maxSeq = math.pow(2, self.sequenceNoBit - 1)   #fereastra are dim max jumatatate din numarul de secvente
        # secventa de numere a ultimului frame
        self.transmitWindow = dict()  # va contine timerul si daca a fost ack(true/false)
        self.expectedAck = 0
        self.nextPkt = 0  # used to iterate through packetList
        self.nextSeqNo = 0

        if windowSize < self.maxSeq and windowSize > 0:
            self.windowSize = windowSize
        else:
            self.logger.error("Window size should be greater than 0 and less then 2^(sequenceN-1)!")

    def isEmpty(self):
        if len(self.transmitWindow) == 0:
            return True
        return False

    def insideWindow(self, pktNo):
        if pktNo in self.transmitWindow:
            return True
        return False

    def ackRecv(self, pktNo):
        if self.insideWindow(pktNo):
            self.transmitWindow[pktNo][0] = None #stop timer for packet
        if pktNo == self.expectedAck:
            self.slideWindow()
            if len(self.transmitWindow) == 0:
                self.expectedAck = self.nextSeqNo
            else:
                self.expectedAck = self.transmitWindow.items()[0][0]  # urm ack devine capatul inferior al ferestrei

    def slideWindow(self):
        for k, v in self.transmitWindow.items():
            if v[0] == None and v[1] == True:
                del self.transmitWindow[k]
            else:
                break

    def getSeqNo(self):
        self.transmitWindow[self.nextSeqNo] = [None, False]
        self.nextSeqNo += 1
        if self.nextSeqNo >= self.maxSeq:
            self.nextSeqNo %= self.maxSeq
        self.nextPkt += 1

