from cgitb import enable
from operator import truediv
from tkinter import Pack
from enlace import *
import time 
import numpy as np
from utils import *
import sys

serialName = "COM8"

def handshake(com:enlace,id:int):
	com.sendData(buildPacket(p_type=PacketType.HANDSHAKE))
	ack = com.getData(14,timeout=5)
	verify_packet(ack,with_type=PacketType.ACK_HS)
dataChunks = []
def checkWrongPacket(com:enlace,currCount):
    try:
        head = com.getData(10,timeout=0.2)
        verify_packet(head,with_type=PacketType.NO_ACK_DATA)
        count = head[6]
        print(f"Count corrigido para {count}")
        return True, count
    except (PacketTimeoutError,InvalidPacket):
        print("Nao recebeu T6")
        return False, currCount

def main(com: enlace):
    inicia = False
    while True:
        try:
            handshake()
            break
        except PacketTimeoutError:
            if input("Timeout waiting for ack. Try again?(Y/n)") == "n":
                raise ConnectionTimeoutError(print("Timeout waiting for ack. Aborting."))
    numPck = 1000
    count = 1

    if count > numPck:
        return True

    timer = time.time()
    while True:
        try:
            com.sendData(buildPacket(payload=dataChunks[count]))
            head = com.getData(10,timeout=5)
            #pegar dados 
            count+=1
        except PacketTimeoutError:
            if time.time() - timer > 20:
                raise ConnectionTimeoutError()
            changedCount, newCount = checkWrongPacket(com)
            if changedCount:
                count = newCount
                timer = timer.timer()
            

            


    
if __name__ == "__main__":
    try:
        com1 = enlace(serialName)
        res = main(com1)
        if res: 
            print("Transmissao realizada com sucesso")
        else: 
            print("Ocorreu um erro durante tranmissao")
    except KeyboardInterrupt:
        com1.disable()
        sys.exit()
    except ConnectionTimeoutError:
        com1.sendData(buildPacket(p_type=PacketType.TIMEOUT))
        print("Timeout. Ending comunication!")
    except Exception as erro:
        print("ops! :-\\\nAbortando.")
        print(erro)
        com1.disable()
        sys.exit()
        