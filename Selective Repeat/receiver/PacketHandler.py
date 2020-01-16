from threading import Thread
import random
from utils.Packet import Packet
from threading import Lock
lock = Lock()
import time
import select

class PacketHandler:
    def __init__(self, receiverSocket, senderIP, senderPort, receiverIP, receiverPort, window, timeout, logger , threadName, pktLossProb):
        self.receiverSocket = receiverSocket
        self.senderIP = senderIP
        self.senderPort = senderPort
        self.receiverIP = receiverIP
        self.receiverPort = receiverPort
        self.window = window
        self.timeout = timeout
        self.logger = logger
        self.threadName = threadName
        self.packet = Packet("", "", "")
        self.flag = 0
        self.pktLossProb = pktLossProb
        self.flagTransm = 0  # flag to check if I received all the packets
        self.lastPktTime=0

    def run(self):
        ready = select.select([self.receiverSocket], [], [], self.timeout)

        if not ready[0]:
            return
        try:
            packet, _ = self.receiverSocket.recvfrom(1600)
        except Exception:
            self.logger.error("Couldn't receive UDP packet!\n")
            raise Exception("Receiving UDP packet failed!\n")

        packet = packet.decode("utf-8")
        self.packet.unpack(packet)

        if self.window.alreadyReceived( self.packet.sequenceNo):
            self.flag = 1
            self.sendAck(self.packet.sequenceNo)
            self.logger.info("Packet already received! Sending again ACK for the packet with the sequence no " + self.packet.sequenceNo + ".\n")

        if not self.flag and self.window.isOutRecvWin(self.packet.sequenceNo):
            self.logger.info(f"Received packet with the sequence number {self.packet.sequenceNo} outside receipt window!\n")
            self.flag = 1

        if self.window.contain(self.packet.sequenceNo):
            self.flag = 1
            self.sendAck(self.packet.sequenceNo)
            self.logger.info("Packet already received! Sending again ACK for the packet with the sequence no " + self.packet.sequenceNo + ".\n")

        if self.simulatePktLoss():
            self.logger.info(f"Lost a packet with the sequence number {self.packet.sequenceNo}!\n")
            self.flag = 1

        if self.flag == 0:

            if len(self.window.receiptWin) < self.window.windowSize or \
                    (len(self.window.receiptWin) == self.window.windowSize and self.window.receiptWin[str(int(self.packet.sequenceNo))] == None):

                if self.packet.checkiflaspkt():
                    self.flagTransm = 1

                self.logger.info(f"On Thread {self.threadName}-Receiving packet no {int(self.packet.sequenceNo)} containing: {self.packet.data}\n")
                self.window.add(self.packet)
                self.sendAck(self.packet.sequenceNo)
                self.logger.info("Sending ACK for the packet with the sequence no " + self.packet.sequenceNo + ".\n")


        if int(self.window.getExpPkt()) == int(self.packet.sequenceNo):
            while True:
                packet = self.window.getExpectedPktAndSlide()
                if not packet:
                    break
            if(self.flagTransm and len(self.window.receiptWin)==0):
                self.lastPktTime = time.time()


    def sendAck(self, seqNo):

        packet = Packet("ack", f"{int(seqNo)}", "")
        packet = packet.pack()
        try:
            self.receiverSocket.sendto(bytes(packet, 'utf-8'), (self.senderIP, self.senderPort))
        except Exception:
            self.logger.error("Sending UDP packet failed")
            raise Exception("Sending UDP packet failed!")



    def simulatePktLoss(self):

        if random.random() < self.pktLossProb:
            return True
        return False

    def isTransmissionDonne(self):

        if self.flagTransm:
            return True
        return False

    def clearFlag(self):
        self.flag = 0















