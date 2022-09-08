# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


import sys
from urllib.request import parse_keqv_list
from enlace import *
import time
import numpy as np
from utils import *
# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM8"                  # Windows(variacao de)


def main(com1:enlace):

    #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
    #para declarar esse objeto é o nome da porta.



    # Ativa comunicacao. Inicia os threads e a comunicação seiral 
    com1.enable()
    #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
    print("----------------------------------------------------------")
    print("Comunicação aberta com sucesso! Vamos ao resto do projeto!")
    print("----------------------------------------------------------")



    print("esperando 1 byte de sacrifício")
    rxBuffer, nRx = com1.getData(1)
    time.sleep(.1)

    com1.rx.clearBuffer()
    time.sleep(.2)
    com1.sendData(b'00')
    time.sleep(1)
    getTimedData = genDataRetrieval(com1)

    handshake,_ = com1.getData(14)
    verify_packet(handshake, with_type=PacketType.HANDSHAKE)
    print("received handshake")
    time.sleep(.1)
    ack_packet = buildPacket(p_type=PacketType.ACK_HS)
    com1.sendData(ack_packet)
    packetCount = 1
    totalPackets = 1
    rxBuffer = bytearray()
    ack_data  = buildPacket(p_type=PacketType.ACK_DATA)
    while packetCount != totalPackets+1:
        try:
            head = getTimedData(10)
            payloadSize = head[1]
            packetCountRec = int.from_bytes(head[2:6],byteorder="big")
            totalPackets = int.from_bytes(head[6:],byteorder="big")
            if packetCountRec!=packetCount:
                raise InvalidPacket("wrong packet number")
           
            payload = getTimedData(payloadSize)
            eop = getTimedData(4)
            packet = head+payload+eop
            verify_packet(packet, with_type=PacketType.DATA)
            com1.sendData(ack_data)
            packetCount+=1
            rxBuffer+=payload
        except (ComTimeoutError,InvalidPacket) as error:
            print(error)
            com1.sendData(buildPacket(p_type=PacketType.NO_ACK_DATA))
            time.sleep(.1)
            com1.rx.clearBuffer()
            time.sleep(.1)
    with open("img/imgDevolvida.jpg","wb") as file:
        file.write(rxBuffer)
    com1.disable()


    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    try:
        com1 = enlace(serialName)
        main(com1)
    except KeyboardInterrupt:
        com1.disable()
        sys.exit()
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        sys.exit()
        