from threading import Thread
import random
from utils.Packet import Packet
from threading import Lock
lock = Lock()

class PacketHandler:
    def __init__(self, receiverSocket, senderIP, senderPort, receiverIP, receiverPort, window, timeout, logger ,threadName, pktLossProb):
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

    def run(self):

        try:
            packet, _ = self.receiverSocket.recvfrom(1600)
        except Exception:
            self.logger.info("Couldn't receive UDP packet!\n")
            raise Exception("Receiving UDP packet failed!\n")

        packet = packet.decode("utf-8")
        self.packet.unpack(packet)

        if self.window.isOutRecvWin(self.packet.sequenceNo):
           self.logger.info(f"Received packet with the sequence number {self.packet.sequenceNo} outside receipt window!\n")
           self.flag = 1

        if self.window.contain(self.packet.sequenceNo):
            self.logger.info(f"This packet with the sequnce number {self.packet.sequenceNo} was already received!\n")
            self.flag = 1

        if self.simulatePktLoss():
            self.logger.info(f"Lost a packet with the sequence number {self.packet.sequenceNo}!\n")
            self.flag = 1

        if self.flag == 0:
            self.logger.info(f"On Thread {self.threadName}-Receiving packet no {self.packet.sequenceNo} containing: {self.packet.data}\n")\

            if len(self.window.receiptWin) < self.window.windowSize-1 or \
                    (self.window.receiptWin == self.window.windowSize and self.window.receiptWin[str(self.packet.sequenceNo)] == None):
                if self.packet.checkIfLastPkt():
                    self.flagTransm = 1
                self.window.add(self.packet)

        if int(self.window.getExpPkt()) == int(self.packet.sequenceNo):
            while True:
                packet = self.window.getExpectedPktAndSlide()
                if packet:
                    print(f"I received {packet.packetType}, no {packet.sequenceNo} containing {packet.data}")
                else:
                    break

    def simulatePktLoss(self):

        if random.random() < self.pktLossProb:
            return True
        return False

    def isTransmissionDonne(self):

        if self.flagTransm:
            return True
        return False















