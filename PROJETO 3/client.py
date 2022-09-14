# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np
from utils import *
import sys
# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM7"                  # Windows(variacao de)


def main(com1:enlace):
    #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
    #para declarar esse objeto é o nome da porta.
    
    
    # Ativa comunicacao. Inicia os threads e a comunicação seiral 
    com1.enable()
    getTimedData = genDataRetrieval(com1)
    #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
    print("----------------------------------------------------------")
    print("Comunicação aberta com sucesso! Vamos ao resto do projeto!")
    print("----------------------------------------------------------")

    #Envia e recebe byte de sacrifcio
    print("enviando byte de sacrificio")
    time.sleep(.2)
    com1.sendData(b'00')
    time.sleep(1)
    print("aguardando byte de sacrificio")

    try:
        getTimedData()
    except ComTimeoutError:
        print("TIMEOUT DO BYTE DO SACRIFICIO")
    time.sleep(.1)

    com1.rx.clearBuffer()
    time.sleep(.2)

    #le arquivo e o separa em pedacos que cabem no payload
    imageR = "./img/wpp.jpg"
    with open(imageR, "rb") as image: 
        data = image.read()  #https://stackoverflow.com/questions/22351254/python-script-to-convert-image-into-byte-array
    txBuffer = chunks(data,114)

    #Faz handhsake
    print("enviando handshake")
    handshakePacket = buildPacket(p_type=PacketType.HANDSHAKE)
    com1.sendData(handshakePacket);
    received_answer = False
    while not received_answer:
        try:
            print(com1.rx.getBufferLen())
            verify_packet(getTimedData(14),with_type=PacketType.ACK_HS)
            print(com1.rx.getBufferLen())
            received_answer = True
            print("ACK received. Starting data transmission.")
        except ComTimeoutError:
            if input("Timeout. No response from server. Do you want to try again?(Y/n)") == "n":
                raise Exception("Terminated due to inactive server")
                #Envia e recebe byte de sacrifcio
            print("enviando byte de sacrificio")
            time.sleep(.2)
            com1.sendData(b'00')
            try:
                getTimedData()
            except ComTimeoutError:
                print("TIMEOUT DO BYTE DO SACRIFICIO")
            time.sleep(.1)

            com1.rx.clearBuffer()
            time.sleep(.2)

            com1.sendData(handshakePacket);
    #A  A variaavel txBuffer e lazy entao o len precisa ser calculado.    
    totalPackages = len(data)//114
    if len(data)%114!=0: totalPackages+=1
    packetCount = 1
    print(f"Starting data Transmission will send {totalPackages} packages")
    for imageChunk in txBuffer:
        gotAck = False
        while not gotAck:
            try:
                # if packetCount==10:
                #     packetCount+=1
                packet = buildPacket(payload=imageChunk,n_packet=packetCount,t_packets=totalPackages)
                com1.sendData(packet)
                answer = getTimedData(14)
                verify_packet(answer,with_type=PacketType.ACK_DATA)
                gotAck = True
                packetCount+=1
            except ComTimeoutError:
                print("Timeout awaiting for server. Trying again.")
                com1.rx.clearBuffer()
            except InvalidPacket as error:
                print("Invalid answer from server. Trying again.")
                print(error)
                com1.rx.clearBuffer()


    print("finished sending data")


    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com1.disable()
        

        
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
ic