import time
import numpy as np
import sys, os
print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import *
serial_num = "COM7"



enlace(serial_num)

def main(com: enlace):
    ocioso = True
    if ocioso == True:
        if recebeu_msg_t1 == False:
            #sleep 1 sec
        else: 
            if e_para_mim == True:
                ocioso = False:
                #sleep 1 sec
            else:
                #sleep 1 sec
    else:
        #envia msg t2
        cont = 1
        while cont <= numPckg:
            #set timer1
            #set timer 2
            if msg_t3_recebida == True:
                if pckg_ok = False:
                    #envia msg t6
                else:
                    #envia msg t4
                    cont +=1
            else:
                while msg_t3_recebida == False:
                    #sleep 1 sec
                    if timer2 > 20:
                        ocioso = True
                        #envia msg t5
                        #encerra COM
                        print(":-(")
                    else:
                        if timer1 > 2:
                            #envia msg t4
                            #reset timer1
                            msg_t3_recebida = False
                        else:
                            msg_t3_recebida = False
        else:
            print("SUCESSO!")






    





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


