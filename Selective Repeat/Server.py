import socket
from utils.Packet import Packet
from utils.Logger import Logger

class Server:
    def __init__(self, serverIP = "127.0.0.1", serverPort = 8081):
        self.serverIP = serverIP
        self.serverPort = serverPort
        self.serverSocket = None
        self.logger = Logger("Server")

    def open_com(self):
        try:
            self.serverSocket = socket.socket(socket.AF_INET,
                                              socket.SOCK_DGRAM)
            self.serverSocket.bind((self.serverIP, self.serverPort))
            self.logger.info("Created an UDP socket for communication")

        except Exception as e:
            self.logger.error("Could not create UDP socket for communication with the server!")

    def run(self):
        while True:
            recvPacket, _ = self.serverSocket.recvfrom(1024)
            packet = Packet("","","")
            recvPacket = recvPacket.decode("utf-8")
            packet.unpack(recvPacket)
            self.logger.info(f"Received {packet.packetType}, no.{packet.sequenceNo} containing {packet.data}")
            print(f"I received {packet.packetType}, no {packet.sequenceNo} containing {packet.data}")

    def close(self):
        self.serverSocket.close()
        self.logger.info("Server is closing")


if __name__ == '__main__':
    server = Server()
    server.open_com()
    server.run()
    server.close()
