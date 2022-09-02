import random as r
comandos=[
    bytearray(b'\x00\xfa\x00\x00'),
    bytearray(b'\x00\x00\xFA\x00'),
    bytearray(b'\xfa\x00\x00'),
    bytearray(b'\x00\xFA\x00'),
    bytearray(b'\x00\x00\xFA'),
    bytearray(b'\x00\xFA') ,
    bytearray(b'\xFA\x00'),
    bytearray(b'\x00'),
    bytearray(b'\xFA')
]
def aleatorio():
    N = r.randint(10,30)
    lista = []

    for _ in range(N):
        lista.append(r.randint(0,8))

    return [comandos[n] for n in lista]

