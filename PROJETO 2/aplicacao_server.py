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

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)


def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
    
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
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
      
        #acesso aos bytes recebidos
        cmds = 0
        while True:
            sizeBuffer, nRx = com1.getData(1)
            if (sizeBuffer[0]==0):
                break
            cmds+=1
            rxBuffer, nRx = com1.getData(sizeBuffer[0])
            print(f"recebendo {rxBuffer} de {sizeBuffer[0]} bytes")
            time.sleep(.1)
        print(f"Enviando resposta, foram contados {cmds} comandos")
        com1.sendData(bytearray([cmds]))
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()