import socket
from utils.Logger import Logger
from receiver.PacketHandler import PacketHandler
from receiver.ReceiverWindow import ReceiverWindow
import time
from threading import Thread

class Server():
    def __init__(self, windowSize = 8, sequenceNo = 8, serverIP = "127.0.0.1", serverPort = 1235, timeout = 1, senderPort = 1234, senderIP = "127.0.0.1" ):
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
            self.serverSocket.setblocking(0)
            self.logger.info("Created an UDP socket for communication")

        except Exception as e:
            self.logger.error("Could not create UDP socket for communication with the server!")

    def run(self):
        self.window = ReceiverWindow(self.sequenceNo, self.windowSize)
        self.packetHandler = PacketHandler(self.serverSocket, self.senderIP, self.senderPort, self.serverIP,
                                           self.serverPort, self.window, self.timeout, self.logger, "Thread_Server", 0)

        while True:

            self.packetHandler.run()
            if self.packetHandler.isTransmissionDonne()and \
                    self.packetHandler.lastPktTime != 0 and \
                    ((time.time()-self.packetHandler.lastPktTime) > self.timeout):
                break

            self.packetHandler.clearFlag()

    def close(self):
        self.serverSocket.close()
        self.logger.info("Server is closing")

    def setServerIP(self, val):
        self.serverIP = val

    def setServerPort(self, val):
        self.serverPort = val

    def getServerIP(self):
        return self.serverIP

    def getServerPort(self):
        return self.serverPort


if __name__ == '__main__':
    server = Server()
    server.open_com()
    server.run()
    server.close()