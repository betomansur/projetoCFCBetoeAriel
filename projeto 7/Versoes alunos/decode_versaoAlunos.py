
#Importe todas as bibliotecas
from suaBibSignal import *
import peakutils    #alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time


#funcao para transformas intensidade acustica em dB, caso queira usar
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():

    #*****************************instruções********************************
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)   
    # algo como:
    signal = signalMeu() 
       
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    sd.default.samplerate = 44100
    sd.default.channels = 2#numCanais # o numero de canais, tipicamente são 2. Placas com dois canais. Se ocorrer problemas pode tentar com 1. No caso de 2 canais, ao gravar um audio, terá duas listas
    duration =  2# #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic
    
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes) durante a gracação. Para esse cálculo você deverá utilizar a taxa de amostragem e o tempo de gravação
    numAmostras = duration * 44100
    #faca um print na tela dizendo que a captacao comecará em n segundos. e entao 
    #use um time.sleep para a espera
    for i in range(5,0,-1):
        print(f"a captacao comecará em {i} segundos")
        time.sleep(1)
    #Ao seguir, faca um print informando que a gravacao foi inicializada
    print("gravacaco iniciada")
    #para gravar, utilize
    audio = sd.rec(int(numAmostras), 44100, channels=1)[:,0]
    sd.wait()
    print("print gravacao finalizada")


    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista, isso dependerá so seu sistema, drivers etc...
    #extraia a parte que interessa da gravação (as amostras) gravando em uma variável "dados". Isso porque a variável audio pode conter dois canais e outas informações). 
    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    t = np.linspace(0,duration,44100)
    # plot do áudio gravado (dados) vs tempo! Não plote todos os pontos, pois verá apenas uma mancha (freq altas) . 
       
    ## Calcule e plote o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signal.calcFFT(audio, 44100)
    signal.plotFFT(audio,44100)
    plt.show()
    #agora, voce tem os picos da transformada, que te informam quais sao as frequencias mais presentes no sinal. Alguns dos picos devem ser correspondentes às frequencias do DTMF!
    #Para descobrir a tecla pressionada, voce deve extrair os picos e compara-los à tabela DTMF
    #Provavelmente, se tudo deu certo, 2 picos serao PRÓXIMOS aos valores da tabela. Os demais serão picos de ruídos.

    # para extrair os picos, voce deve utilizar a funcao peakutils.indexes(,,)
    # Essa funcao possui como argumentos dois parâmetros importantes: "thres" e "min_dist".
    # "thres" determina a sensibilidade da funcao, ou seja, quao elevado tem que ser o valor do pico para de fato ser considerado um pico
    #"min_dist" é relatico tolerancia. Ele determina quao próximos 2 picos identificados podem estar, ou seja, se a funcao indentificar um pico na posicao 200, por exemplo, só identificara outro a partir do 200+min_dis. Isso evita que varios picos sejam identificados em torno do 200, uma vez que todos sejam provavelmente resultado de pequenas variações de uma unica frequencia a ser identificada.   
    # Comece com os valores:
    index = peakutils.indexes(yf, thres=0.3, min_dist=50)
    print("index de picos {}" .format(index)) #yf é o resultado da transformada de fourier

    #printe os picos encontrados! 
    # Aqui você deverá tomar o seguinte cuidado: A funcao  peakutils.indexes retorna as POSICOES dos picos. Não os valores das frequências onde ocorrem! Pense a respeito
    peaks = np.take(xf,index)
    print(peaks)
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    x_freqs = [1209,1336,1477,1633]
    y_freqs = [697,770,852,941]
    values = [[1,2,3,None],[4,5,6,None],[7,8,9,None],[None,0,None,None]]
    def findClosestX(peak):
        x = x_freqs[0]
        index = 0
        delta = abs(peak - x)
        for i in range(1,len(x_freqs)):
            freq = x_freqs[i]
            t_delta = abs(peak - freq)
            if t_delta < delta:
                delta = t_delta
                x = freq
                index = i
        return x,index,delta
            
    def findClosestY(peak):
        y = y_freqs[0]
        index = 0
        delta = abs(peak - y)
        for freq in range(1,len(y_freqs)):
            freq = y_freqs[i]
            t_delta = abs(peak-freq)
            if t_delta < delta:
                delta = t_delta
                y = freq
                index = i
        return y, index, delta
    x_peaks = []
    y_peaks = []
        
    for peak in peaks:
        x_peaks.append(findClosestX(peak))
        y_peaks.append(findClosestY(peak))
    x_peak = min(x_peaks,key=lambda peak: peak[2])
    y_peak = min(y_peaks,key=lambda peak: peak[2])
    print(x_peaks)
    print(y_peaks)

    print(f"Picos corretos indenteificados: {x_peak[0]}, {y_peak[0]}")
    print(f"numero transmitido {values[y_peak[1]][x_peak[1]]}")
    


        
    
        
    #print o valor tecla!!!
    #Se acertou, parabens! Voce construiu um sistema DTMF

    #Você pode tentar também identificar a tecla de um telefone real! Basta gravar o som emitido pelo seu celular ao pressionar uma tecla. 

      
    ## Exiba gráficos do fourier do som gravados 
    plt.show()

if __name__ == "__main__":
    main()
