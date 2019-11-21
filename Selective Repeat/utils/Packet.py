pkt_type2bin = {'ack': '0', 'data': '1'}
pkt_bin2type = {'0': 'ack', '1': 'data'}


class Packet:
    def __init__(self, packettype="", sequenceno="", data=""):
        self.packetType = packettype
        self.sequenceNo = sequenceno
        self.data = data

    def pack(self):
        pkt_type = pkt_type2bin.get(self.packetType)
        raw_packet = pkt_type + self.sequenceNo + self.data
        return raw_packet

    def unpack(self, raw_packet):
        self.packetType = pkt_bin2type.get(raw_packet[0])
        self.sequenceNo = raw_packet[1:2]
        self.data = raw_packet[2:]
