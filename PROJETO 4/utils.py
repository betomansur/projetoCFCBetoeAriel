from enum import Enum
from struct import pack
from enlace import *
import time
#       0    1-2         3        4             5					6				7		  8-9     
#HEAD TYPE|  ** |TOTAL_PACKETS|PACKET_N|FILE_ID ou PAYLOADSIZE|PACKET_N_ERROR|LAST_PACKET_RECEIVED| ** | 

EOP = b"\xAA\xBB\xCC\xDD"
class PacketType(Enum):
	HANDSHAKE = 1
	ACK_HS = 2
	DATA = 3
	ACK_DATA = 4
	TIMEOUT = 5
	NO_ACK_DATA = 6



def buildPacket(payload=[],p_type=PacketType.DATA,n_packet=0,t_packets=0,file_id=0,):
	packet = buildHead(p_type,len(payload),n_packet,t_packets)
	if p_type==PacketType.DATA:
		packet+=payload#+bytearray([1,2,3])
	return packet+EOP
	
def buildHead(p_type:PacketType,payload_size=0,n_packet=0,t_packets=0):
	head = bytearray([p_type.value,0,0,t_packets])
def verify_packet(packet:bytearray,*,with_type=None):
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
				return com.getData(length)[0]
			if time.time() - date > timeout:
				raise PacketTimeoutError()
			time.sleep(.1)
	return getTimedData

