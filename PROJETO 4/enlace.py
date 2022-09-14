#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Camada de Enlace
####################################################

# Importa pacote de tempo
import time
# Interface Física
from interfaceFisica import fisica

# enlace Tx e Rx



from enlaceRx import RX
from enlaceTx import TX
class PacketTimeoutError(Exception):
    pass
class ConnectionTimeoutError(Exception):
    pass

class InvalidPacket(Exception):
	pass
class enlace(object):
    
    def __init__(self, name):
        self.fisica      = fisica(name)
        self.rx          = RX(self.fisica)
        self.tx          = TX(self.fisica)
        self.connected   = False

    def enable(self):
        self.fisica.open()
        self.rx.threadStart()
        self.tx.threadStart()

    def disable(self):
        self.rx.threadKill()
        self.tx.threadKill()
        time.sleep(1)
        self.fisica.close()

    def sendData(self, data):
        self.tx.sendBuffer(data)
        
    def getData(self, size,timeout=0):
        if timeout==0:
            return self.rx.getNData(size)

        date = time.time()
        while True:
            buffLen = self.rx.getBufferLen()
            if buffLen>=size:
                return self.rx.getNData(size)
            if time.time() - date > timeout:
                raise PacketTimeoutError()
            time.sleep(.1)
        
