
#importe as bibliotecas
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

#funções a serem utilizadas
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)



dic_freq = {0:[1336,941], 1:[1209,697] ,2:[1336,697], 3:[1477,697],4: [1209,770], 5:[1336,770], 6:[1477,770], 7:[1209,852], 8:[1336,852], 9: [1477,852], "X": [1209,941], "#": [1477,941],"A":[1633,697], "B": [1633,770], "C": [1633,852], "D": [1633,941]}

def main():
    try:
        num = int(input("Qual numero entre 0 a 9?"))
        if num > 9 or num < 0: 
            raise Exception()
    except:
        print("Numero invalido")
    freqs = dic_freq[num]

    t = np.linspace(0,2,44100*2)
    sins = []
    for freq in freqs:
        sins.append(np.sin(2*np.pi*freq*t))
    
    signal = sum(sins)
    

    #********************************************instruções*********************************************** 
    # seu objetivo aqui é gerar duas senoides. Cada uma com frequencia corresposndente à tecla pressionada
    # então inicialmente peça ao usuário para digitar uma tecla do teclado numérico DTMF
    # agora, voce tem que gerar, por alguns segundos, suficiente para a outra aplicação gravar o audio, duas senoides com as frequencias corresposndentes à tecla pressionada, segundo a tabela DTMF
    # Essas senoides tem que ter taxa de amostragem de 44100 amostras por segundo, entao voce tera que gerar uma lista de tempo correspondente a isso e entao gerar as senoides
    # Lembre-se que a senoide pode ser construída com A*sin(2*pi*f*t)
    # O tamanho da lista tempo estará associada à duração do som. A intensidade é controlada pela constante A (amplitude da senoide). Construa com amplitude 1.
    # Some as senoides. A soma será o sinal a ser emitido.
    # Utilize a funcao da biblioteca sounddevice para reproduzir o som. Entenda seus argumento.
    # Grave o som com seu celular ou qualquer outro microfone. Cuidado, algumas placas de som não gravam sons gerados por elas mesmas. (Isso evita microfonia).
    
    # construa o gráfico do sinal emitido e o gráfico da transformada de Fourier. Cuidado. Como as frequencias sao relativamente altas, voce deve plotar apenas alguns pontos (alguns periodos) para conseguirmos ver o sinal
    

    print("Inicializando encoder")
    print("Aguardando usuário")
    print("Gerando Tons base")
    print("Executando as senoides (emitindo o som)")
    print("Gerando Tom referente ao símbolo : {}".format(num))
    sd.play(signal, 44100)
    # Exibe gráficos
    plt.show()
    # aguarda fsim do audio
    sd.wait()
    plt.figure()
    plt.plot(t[:500], signal[:500])
    plt.xticks()
    plt.title('Signal')

    signalMeu().plotFFT(signal, 44100)
    plt.show()

    

if __name__ == "__main__":
    main()
