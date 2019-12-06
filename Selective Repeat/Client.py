import socket
from utils.Packet import Packet
from utils.Window import Window
from utils.Logger import Logger
import os

class Client:
    def __init__(self, windowSize = 2,sequenceNo=8,clientIP = "192.168.161.1", clientPort = 8080,serverIP="192.168.161.1",serverPort=8080):
        self.clientIP = clientIP
        self.clientPort = clientPort
        self.clientSocket = None
        self.logger = Logger("Client")
        self.sequenceNo = sequenceNo
        self.windowSize = windowSize
        self.serverIP = serverIP
        self.serverPort = serverPort
        self.dim = 45
    def open_com(self):
        try:

            self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.message = input("Message:")
            self.logger.info("Created an UDP socket for communication")

        except Exception as e:
            self.logger.error("Could not create UDP socket for communication with theclient!")

    def run(self):

            with open("fisier.txt","r") as f:
                date = f.read(self.dim)
                while date:
                    self.logger.info("Transmitting message  to the receiver")

                    self.clientSocket.sendto(bytes(date,'utf-8'),(self.serverIP, self.serverPort))
                    date = f.read(self.dim)
          #window = Window(self.sequenceNo, self.windowSize)


    def close(self):
        self.clientSocket.close()
        self.logger.info("Client is closing")


if __name__ == '__main__':
   client = Client(2,8)
   client.open_com()
   client.run()
   client.close()