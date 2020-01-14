import socket
from sender.SenderWindow import SenderWindow as Window
from utils.Logger import Logger
from sender.PacketHandler import PacketHandler
from utils.Packet import Packet
from sender.AckHandler import AckHandler


class Client:
    def __init__(self, filename, window_size=8, sequence_no=8, senderip="127.0.0.1", sender_port=1234, receiverip ="127.0.0.1", receive_port=1234, timeout=30.0):
        self.senderIP = senderip
        self.senderPort = sender_port
        self.senderSocket = None
        self.receiverIP = receiverip
        self.receiverPort = receive_port
        self.logger = Logger("Client")
        self.sequenceNo = sequence_no
        self.windowSize = window_size
        self.timeout = timeout
        self.window = None
        self.filename = filename

    def open_com(self):
        try:
            self.senderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.logger.info("Created an UDP socket for communication")

        except Exception as e:
            self.logger.error("Could not create UDP socket for communication with the client!")

    def run(self):

        packets = self.acceptPkts(self.filename)
        self.window = Window(self.sequenceNo, self.windowSize)
        self.logger.info("Starting transmission")

        #ackHandler = AckHandler(self.senderSocket, self.receiverIP, self.window, self.logger)   #nu se sterg
        #ackHandler.start()

        while not self.window.isEmpty() or self.window.getNextPkt() < len(packets):    # mai sunt pachete netrimise

            if self.window.full():                      # fereastra plina, asteptam sa mai primim ack
                pass
            elif not self.window.full() and self.window.getNextPkt() >= len(packets):   # am trimis toate pachetele
                pass
            else:

                packetData = packets[self.window.getNextPkt()]  # luam urm pachet spre a fi trimis
                seqNo = self.window.nextSeqNo                       # ii atribuim un nr de secv
                packet = Packet("data", str(seqNo), packetData)
                if self.checkIfLastPkt(packets):
                    packet.setFlag()
                self.window.getSeqNo()
                # marcam ca si folosit nr de secv
                pktHandler = PacketHandler(self.senderSocket, self.receiverIP, self.receiverPort, packet, self.timeout,
                                           self.window, self.logger)
                pktHandler.start()    # pornim thread pt trimiterea propriu-zisa a pachetului

        #ackHandler.join()          ## nu se sterge avem nevoie
        self.logger.info("Stopped transmission")
        self.window.stopTransm()


    def close(self):
        self.senderSocket.close()   # inchidere comm
        self.logger.info("Client is closing")

    def acceptPkts(self, filename):             # generare pachete pt un fisier
        packets = []
        with open(filename, "r") as f:
            date = f.read(50)
            while date:
                packets.append(date)
                date = f.read(50)

        return packets

    def checkIfLastPkt(self, packets):

        if self.window.getNextPkt() == len(packets) - 1:
            return True
        return False

    def getfilename(self):
        return self.filename


if __name__ == '__main__':
    client = Client('fisier.txt')
    client.open_com()
    client.run()
    client.close()
