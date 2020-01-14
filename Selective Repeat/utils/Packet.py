pkt_type2bin = {'ack': '0', 'data': '1'}
pkt_bin2type = {'0': 'ack', '1': 'data'}


class Packet:
    def __init__(self, packettype="", sequenceno="", data=""):
        self.packetType = packettype
        self.sequenceNo = sequenceno
        self.data = data
        self.flag = '0'

    def pack(self):

        pkt_type = pkt_type2bin.get(self.packetType)
        if int(self.sequenceNo) < 100:
            if int(self.sequenceNo) < 10:
                self.sequenceNo = '0' + self.sequenceNo
            self.sequenceNo = '0' + self.sequenceNo
        raw_packet = pkt_type + self.sequenceNo + self.data + self.flag

        return raw_packet

    def unpack(self, raw_packet):

        self.packetType = pkt_bin2type.get(raw_packet[0])
        self.sequenceNo = raw_packet[1:4]
        self.data = raw_packet[4:-1]
        self.flag = raw_packet[-1]

    def setFlag(self):

        self.flag = '1'

    def checkIfLastPkt(self):

        if int(self.flag):
            return True
        return False
