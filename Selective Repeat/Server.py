import socket
from utils.Logger import Logger
from receiver.PacketHandler import PacketHandler
from receiver.ReceiverWindow import ReceiverWindow
import select

class Server:
    def __init__(self, windowSize = 8, sequenceNo = 8, serverIP = "127.0.0.1", serverPort = 1234, timeout = 30.0, senderPort = 1234, senderIP = "127.0.0.1" ):
        self.serverIP = serverIP
        self.serverPort = serverPort
        self.serverSocket = None
        self.logger = Logger("Server")
        self.timeout = timeout
        self.senderPort = senderPort
        self.senderIP = senderIP
        self.window = None
        self.sequenceNo = sequenceNo
        self.packetHandler = None
        self.windowSize = windowSize
        self.flag = 0

    def open_com(self):
        try:
            self.serverSocket = socket.socket(socket.AF_INET,
                                              socket.SOCK_DGRAM)
            self.serverSocket.bind((self.serverIP, self.serverPort))
            self.logger.info("Created an UDP socket for communication")

        except Exception as e:
            self.logger.error("Could not create UDP socket for communication with the server!")

    def run(self):
        chance = 0  # if there are more than 3 consecutive timeouts, stop receiving packets from sender
        self.window = ReceiverWindow(self.sequenceNo, self.windowSize)
        self.packetHandler = PacketHandler(self.serverSocket, self.senderIP, self.senderPort, self.serverIP,
                                           self.serverPort, self.window, self.timeout, self.logger, "Thread_Server", 0)

        while True:
            self.packetHandler.run()

            if self.packetHandler.isTransmissionDonne():
                break

    def close(self):
        self.serverSocket.close()
        self.logger.info("Server is closing")


if __name__ == '__main__':
    server = Server()
    server.open_com()
    server.run()
    server.close()