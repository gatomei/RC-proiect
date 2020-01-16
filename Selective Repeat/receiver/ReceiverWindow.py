import math
from utils.Logger import Logger
from threading import Lock
from collections import OrderedDict
lock = Lock()

class ReceiverWindow:

    def __init__(self, sequenceNo , windowSize = 8 ):

        self.windowSize = windowSize
        self.expectedPkt = 0
        self.maxSeq = math.pow(2, sequenceNo)
        self.maxWindowSize = math.pow(2, sequenceNo-1)
        self.lastPkt = self.windowSize
        self.receiptWin = OrderedDict()
        self.logger = Logger("ReceiverWindow")
        self.isPckReceipt = False
        if self.windowSize > self.maxWindowSize:
            self.windowSize = self.maxWindowSize

    def getMaxSeq(self):

        return self.maxSeq

    def getExpPkt(self):

        if self.expectedPkt >= self.maxSeq:
            self.expectedPkt %= self.maxSeq
        return self.expectedPkt

    def contain(self,pktNo):

        if pktNo in self.receiptWin and self.receiptWin[pktNo]:
            return True
        return False

    def add(self, pkt):
            seqNo = int(self.expectedPkt)
            while int(seqNo) != int(pkt.sequenceNo):
                if str(seqNo) not in self.receiptWin:
                    self.receiptWin[str(seqNo)] = None
                seqNo += 1
                if seqNo >= self.maxSeq:
                    seqNo %= self.maxSeq
            self.receiptWin[str(int(pkt.sequenceNo))] = pkt
            self.logger.info(f"Receiving packet no {pkt.sequenceNo} containing: {pkt.data}\n")

    def getExpectedPktAndSlide(self):

        packet = None
        if len(self.receiptWin) > 0:
                packet = self.receiptWin[str(int(self.expectedPkt))]
                if packet:
                    self.expectedPkt += 1

                    del self.receiptWin[str(int(self.expectedPkt)-1)]
                    if self.expectedPkt >= self.maxSeq:
                        self.expectedPkt = int(self.expectedPkt % self.maxSeq)
                    self.lastPkt = self.expectedPkt + self.windowSize -1
                    if self.lastPkt >= int(self.maxSeq) :
                        self.lastPkt = int(self.lastPkt % self.maxSeq)

        return packet


    def isOutRecvWin(self, seqNo):

            if (int(self.expectedPkt) >= ( int(self.maxSeq) - self.windowSize +1 )) and (int(self.expectedPkt) <= (self.maxSeq - 1)):
                if (int(seqNo) >= self.expectedPkt) or (int(seqNo) <= self.lastPkt):
                    return False
            if int(seqNo) < int(self.expectedPkt) or int(seqNo) > int(self.lastPkt):
                return True
            return False

    def alreadyReceived(self, seqNo):

        if (int(self.expectedPkt) >= (int(self.maxSeq) - self.windowSize + 1)) and (
                int(self.expectedPkt) <= (self.maxSeq - 1)):
            if (int(seqNo) >= self.expectedPkt) or (int(seqNo) <= self.lastPkt):
                return False
        if int(seqNo) < int(self.expectedPkt) :
            return True
        return False












