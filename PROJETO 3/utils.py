from enum import Enum
from struct import pack
from enlace import enlace
import time
#       1      2          3-6         7-10
#HEAD TYPE|PAYLOADSIZE|PACKET_N|TOTAL_PACKETS

EOP = b"\x00\xFF\x00\xFF"
class PacketType(Enum):
	HANDSHAKE = 0
	ACK_HS = 1
	DATA = 2
	ACK_DATA = 3
	NO_ACK_DATA = 4

def buildPacket(payload=[],p_type=PacketType.DATA,n_packet=0,t_packets=0):
	packet = buildHead(p_type,len(payload),n_packet,t_packets)
	if p_type==PacketType.DATA:
		packet+=payload
	return packet+EOP
	
def buildHead(p_type:PacketType,payload_size=0,n_packet=0,t_packets=0):
	return bytearray([p_type.value,payload_size])+int.to_bytes(n_packet,length=4,byteorder='big')+int.to_bytes(t_packets,length=4,byteorder='big')

def verify_packet(packet:bytearray,*,with_type=None):
	print(packet[0])
	if packet[0]>4:
		raise InvalidPacket("Invalid Packet Type")
	if packet[-4:] != EOP:
		raise InvalidPacket("Invalid EOP. Possibly wrong payload size")
	p_type = PacketType(packet[0])
	if with_type != None and with_type != p_type:
		raise InvalidPacket(f"Wrong Packet Type\nExpecting {with_type} but got {p_type}")
	return p_type


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def genDataRetrieval(com:enlace):
	def getTimedData(length=1, timeout=5):
		date = time.time()
		while True:
			buffLen = com.rx.getBufferLen()
			if buffLen>=length:
				return com.getData(length)
			if time.time() - date > 5:
				raise ComTimeoutError()
			time.sleep(.1)
	return getTimedData

class ComTimeoutError(Exception):
    pass

class InvalidPacket(Exception):
	pass