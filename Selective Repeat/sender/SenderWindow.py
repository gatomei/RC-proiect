import math
from utils.Logger import Logger
import time
from threading import Lock
from collections import OrderedDict
lock = Lock()

class SenderWindow:

    def __init__(self, sequenceN, windowSize):

        self.sequenceNoBit = sequenceN
        # secventa de numere a primului frame
        self.SeqFirst = 0
        self.logger = Logger("SenderWindow")
        self.maxSeq = math.pow(2, self.sequenceNoBit )   #fereastra are dim max jumatatate din numarul de secvente
        # secventa de numere a ultimului frame
        self.transmitWindow = OrderedDict()  # va contine timerul si daca a fost ack(true/false)
        self.expectedAck = 0
        self.nextPkt = 0  # used to iterate through packetList
        self.nextSeqNo = 0
        self.in_progress = 1

        if 0 < windowSize <= self.maxSeq/2:
            self.windowSize = windowSize
        else:
            self.logger.error("Window size should be greater than 0 and less then 2^(sequenceN-1)!")

    def getMaxSeq(self):
        return self.maxSeq

    def isEmpty(self):
        if len(self.transmitWindow) == 0:
            return True
        return False

    def insideWindow(self, pktNo):
        if pktNo in self.transmitWindow:
            return True
        return False

    def mark_ack(self, pktNo):
        with lock:
            self.transmitWindow[int(pktNo)][1] = True

    def unacked(self, pktNo):
        if pktNo in self.transmitWindow:
            return not self.transmitWindow[pktNo][1]

    def ackRecv(self, pktNo):
        with lock:
            if self.insideWindow(pktNo):
                self.transmitWindow[pktNo][0] = None  # stop timer for packet
        if pktNo == self.expectedAck:
            self.slideWindow()
            with lock:
                if len(self.transmitWindow) == 0:
                    self.expectedAck = self.nextSeqNo
                else:

                    self.expectedAck = list(self.transmitWindow.items())[0][0]  # urm ack devine capatul inferior al ferestrei

    def slideWindow(self):
        to_delete = []
        for k, v in self.transmitWindow.items():
            if v[0] == None and v[1] == True:
                to_delete.append(k)
            else:
                break
        with lock:
            for item in to_delete:
                del self.transmitWindow[item]

    def getSeqNo(self):

        with lock:
            self.transmitWindow[self.nextSeqNo] = [None, False]
        self.nextSeqNo += 1
        if self.nextSeqNo >= self.maxSeq:
            self.nextSeqNo = int(self.nextSeqNo % self.maxSeq)
        self.nextPkt += 1

    def getNextPkt(self):
        return self.nextPkt

    def startTimer(self, pktNo):  # pkt.time=timpul la momentul curent
        self.logger.info(f"On thread-{pktNo} function startTimer")
        if pktNo in self.transmitWindow:
            with lock:
                self.transmitWindow[pktNo][0] = time.time()

    def getStartTime(self, pktNo):   # va returna valoarea timpului in momentul trimiterii pachetului
       return self.transmitWindow[pktNo][0]

    def restartTimer(self, pktNo):  # pkt.time=timpul la momentul curent- in caz de nevoie de retransmitere
        if self.insideWindow(pktNo):
            self.transmitWindow[pktNo][0] = time.time()

    def stopTimer(self, pktNo):
        self.logger.info(f"On thread-{pktNo} function stopTimer")
        with lock:
            self.transmitWindow[pktNo][0] = None

    def full(self):             # in transmiterea unui nou pachet, se are in vederea dim max a ferestrei
        if len(self.transmitWindow) >= self.windowSize:
            return True
        return False

    def stopTransm(self):
        self.in_progress = 0

    def isTransmissionDone(self):
        return not self.in_progress
