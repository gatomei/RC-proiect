from threading import Thread
import time
from threading import Lock
lock = Lock()

class PacketHandler(Thread):
    def __init__(self, senderSocket, receiverIP, receiverPort, packet, timeout, window, logger, threadName="Packet"):
        Thread.__init__(self)
        self.senderSocket = senderSocket
        self.receiverIP = receiverIP
        self.receiverPort = receiverPort
        self.packet = packet
        self.timeout = timeout
        self.window = window
        self.logger = logger
        self.threadName = threadName
        self.resendNo = 0
        self.maxResendNo = 3

    def run(self):
        self.logger.info(f"On Thread {self.threadName }-Sending packet no {self.packet.sequenceNo} ")
        self.send()
        while self.window.unacked(int(self.packet.sequenceNo)) and \
                self.window.getStartTime(int(self.packet.sequenceNo)):
            timpScurs = time.time() - self.window.getStartTime(int(self.packet.sequenceNo))
            if timpScurs > self.timeout:
                if self.resendNo < self.maxResendNo:
                    self.resend()
                    self.resendNo += 1
                else:
                    self.window.mark_ack(int(self.packet.sequenceNo))
                    self.logger.error(f"On Thread {self.threadName }-Abandoned resending for packet no  {self.packet.sequenceNo} ")
                    break



        self.window.ackRecv(int(self.packet.sequenceNo))

    def send(self):
        pkt = self.packet.pack()
        self.senderSocket.sendto(bytes(pkt, 'utf-8'), (self.receiverIP, self.receiverPort))
        self.window.startTimer(int(self.packet.sequenceNo))

    def resend(self):
        self.packet.sequenceNo = str(int(self.packet.sequenceNo))
        pkt = self.packet.pack()
        self.logger.info(f"Packet no {int(self.packet.sequenceNo)} lost.Retransmitting it")
        self.senderSocket.sendto(bytes(pkt, 'utf-8'), (self.receiverIP, self.receiverPort))
        self.window.restartTimer(int(self.packet.sequenceNo))
