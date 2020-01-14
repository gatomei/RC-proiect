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

    def run(self):
        self.logger.info(f"On Thread {self.threadName }-Sending packet no {self.packet.sequenceNo} ")
        self.send()
        while self.window.unacked(int(self.packet.sequenceNo)) and \
                self.window.getStartTime(int(self.packet.sequenceNo)):
            timpScurs = time.time() - self.window.getStartTime(int(self.packet.sequenceNo))
            if timpScurs > self.timeout:
                self.logger.info(f"Packet no {self.packet.sequenceNo} lost.Retransmitting it")
                self.send()
                self.window.restartTimer(int(self.packet.sequenceNo))
            self.window.mark_ack(int(self.packet.sequenceNo))

        self.window.stopTimer(int(self.packet.sequenceNo))
        self.window.ackRecv(int(self.packet.sequenceNo))



    def send(self):
        pkt = self.packet.pack()
        self.senderSocket.sendto(bytes(pkt, 'utf-8'), (self.receiverIP, self.receiverPort))
        self.window.startTimer(int(self.packet.sequenceNo))

