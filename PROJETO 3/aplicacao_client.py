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
from aleatorio import aleatorio
import sys
# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)


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

            
        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(1)
        com1.getData(1)
        time.sleep(.1)

        com1.rx.clearBuffer()
        time.sleep(.2)




        cmds = aleatorio()
        nCmds = len(cmds)
        print(f"Iniciando envio de {nCmds} comandos")
        for cmd in cmds:
            print(f"Enviando comando {cmd} de {len(cmd)} bytes")
            data = bytearray([len(cmd)])+cmd
            com1.sendData(np.asarray(data))
            time.sleep(.1)
        com1.sendData(bytearray([0]))
        currTime = time.time()
    
        while True:
            if (time.time()- currTime)>5:
                print("TIMEOUT. Resposta do server nao obtida")
                pergunta = input(str("Deve continuar?(S/N)"))
                if pergunta == "N":
                    break
                else:
                    
            if (com1.rx.getBufferLen()>0):
                buffRx,nRx = com1.getData(1)
                print(f"O server recebeu {buffRx[0]} comandos")
                print(f"Este numero esta {'correto' if buffRx[0]==nCmds else 'incorreto'}")
                break
            time.sleep(.2)

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        sys.exit()
        
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()