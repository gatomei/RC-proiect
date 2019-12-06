import socket
from sender.SenderWindow import SenderWindow as Window
from utils.Logger import Logger
from sender.PacketHandler import PacketHandler
from utils.Packet import Packet

class Client:
    def __init__(self, windowSize=2, sequenceNo=8, clientIP="127.0.0.1", clientPort=1234, serverIP ="127.0.0.1", serverPort=1234, timeout=30.0):
        self.clientIP = clientIP
        self.clientPort = clientPort
        self.clientSocket = None
        self.serverIP = serverIP
        self.serverPort = serverPort
        self.logger = Logger("Client")
        self.sequenceNo = sequenceNo
        self.windowSize = windowSize
        self.timeout = timeout
        self.window = None

    def open_com(self):
        try:
            self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.logger.info("Created an UDP socket for communication")

        except Exception as e:
            self.logger.error("Could not create UDP socket for communication with the client!")

    def run(self, filename=""):
        packets = self.acceptPkts(filename)
        self.window = Window(self.sequenceNo, self.windowSize)
        self.logger.info("Starting transmission")

        while not self.window.isEmpty() or self.window.getNextPkt() < len(packets):    #mai sunt pachete netrimise

            if self.window.full():                      #fereastra plina, asteptam sa mai primim ack
                pass
            elif not self.window.full() and self.window.getNextPkt() >= len(packets):   #am trimis toate pachetele
                pass
            else:
                packetData = packets[self.window.getNextPkt()]      # luam urm pachet spre a fi trimis
                seqNo = self.window.nextSeqNo                       #ii atribuim un nr de secv
                packet = Packet("data", str(seqNo), packetData)
                self.window.getSeqNo()                              #marcam ca si folosit nr de secv
                pktHandler = PacketHandler(self.clientSocket, self.serverIP, self.serverPort, packet, self.timeout,
                                           self.window, self.logger)
                pktHandler.start()    # pornim thread pt trimiterea propriu-zisa a pachetului

        self.logger.info("Stopped transmission")
        # TO DO
        # create threads for sender and acknowledger


    def close(self):
        self.clientSocket.close()       #inchidere comm
        self.logger.info("Client is closing")

    def acceptPkts(self, filename):             # generare pachete pt un fisier
        packets = []
        with open(filename, "r") as f:
            date = f.read(50)
            while date:
                packets.append(date)
                date = f.read(50)

        return packets


if __name__ == '__main__':
    client = Client(8, 8)
    client.open_com()
    client.run("fisier.txt")
    client.close()

