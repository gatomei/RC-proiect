from threading import Thread
import select
import random

class AckHandler(Thread):

    def __init__(self,
                 senderSocket,   ## sa stim de pe ce socket asculta
                 receiverIP,    ## sa stim de la ce IP asteptam ack
                 window,
                 logger,
                 timeout=10,
                 ackLossProbability=0.05,
                 threadName="ACKHandler",
                 messageSize=1600):
        Thread.__init__(self)
        self.senderSocket = senderSocket
        self.receiverIP = receiverIP
        self.window = window
        self.logger = logger
        self.timeout = timeout
        self.ackLossProbability = ackLossProbability
        self.threadName = threadName
        self.messageSize = messageSize


    def run(self):
        self.logger.info(f"On thraed {self.threadName}-started ")
        while not self.window.isTransmissionDone():
            if self.window.isEmpty():
                continue
            ready = select.select([self.senderSocket], [], [], self.timeout)        ## ascultam sa vedem daca primim mesaje

            if not ready[0]:
                continue
            try:
                recvAck, receiverAddress = self.senderSocket.recvfrom(self.messageSize)
            except Exception as e:
                self.logger.error(f"On thread {self.threadName}-Could not receive UDP packet")
                raise Exception("Receiving UDP packet failed")

            if receiverAddress[0]!= self.receiverIP:
                continue

            recvAck = recvAck.unpack()
            if recvAck.packetType == "ack" and \
                    not self.window.insideWindow(recvAck.sequenceNo):
                self.logger.info(f"On thread {self.threadName} - Received packet out of window")
                continue

            if self.simulate_ack_loss():
                self.logger.info(f"On thread {self.threadName}-Lost packet no {recvAck.sequenceNo}")
            self.logger.info(f"On thread {self.threadName}- Received ack with number {recvAck.sequenceNo}")
            self.window.mark_acked(recvAck.sequenceNo)

        self.logger.info(f"On thread {self.threadName}-stopped ")

    def simulate_ack_loss(self):

        if random.random() < self.ackLossProbability:
            return True
        return False
