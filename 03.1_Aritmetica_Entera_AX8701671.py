# -*- coding: utf-8 -*-

import math
import sys

#%%
#"""
#Dado un mensaje y su alfabeto con sus frecuencias dar un código
#que representa el mensaje utilizando precisión infinita (reescalado)

#El intervalo de trabajo será: [0,R), R=2**k, k menor entero tal
#que R>4T

#T: suma total de frecuencias


def IntegerArithmeticCode(mensaje,alfabeto,frecuencias,numero_de_simbolos=1):
    codigo = ''
    n = len(mensaje)
    F = [0] * (len(frecuencias) + 1)
    for i in range(0, len(frecuencias)):
        F[i + 1] = F[i] + frecuencias[i]
    T = F[(-1)]
    k = 2 + math.ceil(math.log(T + 1, 2))
    R = 2 ** k
    R2 = 2 ** (k - 1)
    m = 0
    M = R - 1
    bits = 0    #numero de bits acumulados
    for i in range(0, n, numero_de_simbolos):
        letra = alfabeto.index(mensaje[i:i + numero_de_simbolos]) + 1
        s = M - m + 1
        M = m + math.floor(s * F[letra] / T) - 1
        m = m + math.floor(s * F[(letra - 1)] / T)
        while True:
            if m >= R / 2:
                cod = '1'
                M = 2 * M - R + 1
                m = 2 * m - R
                for b in range(bits):
                    cod += '0'

                bits = 0
                codigo += cod
            elif M < R / 2:
                cod = '0'
                M = 2 * M + 1
                m = 2 * m
                for b in range(bits):
                    cod += '1'

                bits = 0
                codigo += cod
            elif m >= R / 4 and M < 3 * R / 4:
                M = 2 * M - R2 + 1
                m = 2 * m - R2
                bits += 1
            else:
                break

    if m > R / 4:
        cod = '10'
        for b in range(bits):
            cod += '0'
    else:
        cod = '01'
        for b in range(bits):
            cod += '1'
        codigo += cod
    m_bin = bin(int(m))
    m_bin = m_bin[2:]
    m_bin = '0' * (k - len(m_bin)) + m_bin
    codigo += m_bin
    return codigo


#%%


#"""
#Dada la representación binaria del número que representa un mensaje, la
#longitud del mensaje y el alfabeto con sus frecuencias
#dar el mensaje original
#"""

def IntegerArithmeticDecode(codigo, tamanyo_mensaje, alfabeto, frecuencias):
    mensaje = ''
    F = [0] * (len(frecuencias) + 1)
    for i in range(0, len(frecuencias)):
        F[i + 1] = F[i] + frecuencias[i]
    T = F[(-1)]
    F2 = []
    letra = 1
    for i in frecuencias:
        F2.extend([letra for j in range(i)])
        letra = letra + 1
    k = 2 + math.ceil(math.log(T + 1, 2))
    R = 2 ** k
    R2 = 2 ** (k - 1)
    m = 0
    M = R - 1
    x = 0
    for i in range(k):
        x = 2 * x + int(codigo[i])
    bit = k
    while bit < len(codigo):
        s = M - m + 1
        letra = F2[math.floor(((x - m + 1) * T - 1) / s)]
        mensaje += alfabeto[(letra - 1)]
        M = m + math.floor(s * F[letra] / T) - 1
        m = m + math.floor(s * F[(letra - 1)] / T)
        while bit < len(codigo):
            if m >= R / 2:
                M = 2 * M - R + 1
                m = 2 * m - R
                x = 2 * x - R + int(codigo[bit])
                bit += 1
            else:
                if M < R / 2:
                    M = 2 * M + 1
                    m = 2 * m
                    x = 2 * x + int(codigo[bit])
                    bit += 1
                else:
                    if m >= R / 4 and M < 3 * R / 4:
                        M = 2 * M - R2 + 1
                        m = 2 * m - R2
                        x = 2 * x - R2 + int(codigo[bit])
                        bit += 1
                    else:
                        break
    return mensaje[:tamanyo_mensaje]



alfabeto=['a','b','c','d']
frecuencias=[1,10,20,300]
numero_de_simbolos=1
mensaje='ddddccaabbccaaccaabbaaddaacc'
mensaje_codificado = IntegerArithmeticCode(mensaje,alfabeto,frecuencias,numero_de_simbolos)
if(mensaje_codificado =='01011000111110000000000000000000001000010110001111000000000000000011011000000000000000000000001000010000000000000001000100010000000000010010100000010000'):
    print("OK1!")
mensaje_codificado = '0010110011101100001000100000011101110101111010110011000001101111010010101101101010011100000000111010010000110010010101001001011110111011001011111001000101100110011000011101011110110100011000010110111001011011101100100001011000001101001011001011100100010100101100001110001010101110101011001001010110011111001110100100000100011010001100001011011100101101110110001010100110001010010111000101100111001000010011100011100110111111100001100011001001010000001010001011000100000110000111011001011000101011100111011011011010001100101100100111011010000001011001010110011011110101011101111000001100001000000001001011100001111011001100011101000000010011000101000011010001010101011111010100101011001101100110110111001110100100111001101110011010110010101010011111110100011011000011001011110010011110010101111101101100101011000010110010000110001011100111100101010001001010011011000101001101100000011101011101011101001011110010110110000100111101100110101111001101110011000100010000000001110110101011000111000110110100011001000011010110101010001100111000100010000110100101110110100000000'
alfabeto = [' ', ',', '.', 'E', 'W', 'a', 'b', 'c', 'd', 'e', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y']
frecuencias = [37, 3, 2, 1, 1, 16, 4, 6, 10, 22, 1, 6, 16, 2, 11, 3, 14, 16, 4, 1, 13, 13, 17, 8, 3, 8, 3, 6]
mensaje_decodificado = IntegerArithmeticDecode(mensaje_codificado, 247,alfabeto, frecuencias)
#mensaje_decodificado = IntegerArithmeticDecode(mensaje_codificado, len(mensaje),alfabeto, frecuencias)
print("mensaje decodificado: ", mensaje_decodificado)
if(mensaje_decodificado == mensaje):
    print("DECODE OK!")

alfabeto=['aa','bb','cc','dd']
frecuencias=[1,10,20,300]
numero_de_simbolos=2
mensaje='ddddccaabbccaaccaabbaaddaacc'
if(IntegerArithmeticCode(mensaje,alfabeto,frecuencias,numero_de_simbolos) =='0011010001100000000010000000000000010101000000000001000000001011111101001010100000'):
    print("OK2!")






#%%
#'''
#Definir una función que codifique un mensaje utilizando codificación aritmética con precisión infinita
#obtenido a partir de las frecuencias de los caracteres del mensaje.

#Definir otra función que decodifique los mensajes codificados con la función
#anterior.
#'''

def EncodeArithmetic(mensaje_a_codificar,numero_de_simbolos=1):
    dictionario = dict()
    i=0
    string = ''
    while i < len(mensaje):
        j=0
        while j < numero_de_simbolos:
            string = string + mensaje[i+j]
            #print(string)
            j=j+1
        if string in dictionario:
            dictionario[string] = dictionario[string] + 1
        else:
            dictionario[string] = 1
        i = i + numero_de_simbolos
        string = ''
    #print(dictionario)
    alfabeto = []
    alfabeto = list(dictionario.keys())
    #print(alfabeto)
    frecuencias = []
    frecuencias = list(dictionario.values())
    #print(frecuencias)
    dictionario = dict()

    mensaje_codificado = ''
    n = len(mensaje)
    F = [0] * (len(frecuencias) + 1)
    for i in range(0, len(frecuencias)):
        F[i + 1] = F[i] + frecuencias[i]
    T = F[(-1)]
    k = 2 + math.ceil(math.log(T+1, 2))
    R = 2 ** k
    R2 = 2 ** (k - 1)
    m = 0
    M = R - 1
    bits = 0
    for i in range(0, n, numero_de_simbolos):
        letra = alfabeto.index(mensaje[i:i + numero_de_simbolos]) + 1
        s = M - m + 1
        M = m + math.floor(s * F[letra] / T) - 1
        m = m + math.floor(s * F[(letra - 1)] / T)
        while True:
            if m >= R / 2:
                cod = '1'
                M = 2 * M - R + 1
                m = 2 * m - R
                for b in range(bits):
                    cod += '0'
                bits = 0
                mensaje_codificado += cod
            elif M < R / 2:
                cod = '0'
                M = 2 * M + 1
                m = 2 * m
                for b in range(bits):
                    cod += '1'
                bits = 0
                mensaje_codificado += cod
            elif m >= R / 4 and M < 3 * R / 4:
                M = 2 * M - R2 + 1
                m = 2 * m - R2
                bits += 1
            else:
                break
    if m > R / 4:
        cod = '10'
        for b in range(bits):
            cod += '0'
        mensaje_codificado += cod
    else:
        cod = '01'
        for b in range(bits):
            cod += '1'
        mensaje_codificado += cod
    m_bin = bin(int(m))
    m_bin = m_bin[2:]
    m_bin = '0' * (k - len(m_bin)) + m_bin
    mensaje_codificado += m_bin
    return mensaje_codificado,alfabeto,frecuencias


def DecodeArithmetic(mensaje_codificado,tamanyo_mensaje,alfabeto,frecuencias):
    mensaje = ''
    F = [0] * (len(frecuencias) + 1)
    for i in range(0, len(frecuencias)):
        F[i + 1] = F[i] + frecuencias[i]
    T = F[(-1)]
    F2 = []
    letra = 1
    for i in frecuencias:
        F2.extend([letra for j in range(i)])
        letra = letra + 1
    k = 2 + math.ceil(math.log(T+1, 2))
    R = 2 ** k
    R2 = 2 ** (k - 1)
    m = 0
    M = R - 1
    x = 0
    for i in range(k):
        x = 2 * x + int(mensaje_codificado[i])
    bit = k
    while bit < len(mensaje_codificado):
        s = M - m + 1
        letra = F2[math.floor(((x - m + 1) * T - 1) / s)]
        mensaje += alfabeto[(letra - 1)]
        M = m + math.floor(s * F[letra] / T) - 1
        m = m + math.floor(s * F[(letra - 1)] / T)
        while bit < len(mensaje_codificado):
            if m >= R / 2:
                M = 2 * M - R + 1
                m = 2 * m - R
                x = 2 * x - R + int(mensaje_codificado[bit])
                bit += 1
            else:
                if M < R / 2:
                    M = 2 * M + 1
                    m = 2 * m
                    x = 2 * x + int(mensaje_codificado[bit])
                    bit += 1
                else:
                    if m >= R / 4 and M < 3 * R / 4:
                        M = 2 * M - R2 + 1
                        m = 2 * m - R2
                        x = 2 * x - R2 + int(mensaje_codificado[bit])
                        bit += 1
                    else:
                        break
    mensaje_decodificado = mensaje[:tamanyo_mensaje]
    return mensaje_decodificado

##%%
#'''

#Ejemplo (!El mismo mensaje se puede codificar con varios códigos¡)

#'''

lista_C=['010001110110000000001000000111111000000100010000000000001100000010001111001100001000000',
         '01000111011000000000100000011111100000010001000000000000110000001000111100110000100000000']
alfabeto=['a','b','c','d']
frecuencias=[1,10,20,300]
mensaje='dddcabccacabadac'
tamanyo_mensaje=len(mensaje)

for C in lista_C:
    mensaje_recuperado=IntegerArithmeticDecode(C,tamanyo_mensaje,alfabeto,frecuencias)
    print(mensaje==mensaje_recuperado)



#%%

#'''
#Ejemplo

#'''

mensaje='La heroica ciudad dormía la siesta. El viento Sur, caliente y perezoso, empujaba las nubes blanquecinas que se rasgaban al correr hacia el Norte. En las calles no había más ruido que el rumor estridente de los remolinos de polvo, trapos, pajas y papeles que iban de arroyo en arroyo, de acera en acera, de esquina en esquina revolando y persiguiéndose, como mariposas que se buscan y huyen y que el aire envuelve en sus pliegues invisibles. Cual turbas de pilluelos, aquellas migajas de la basura, aquellas sobras de todo se juntaban en un montón, parábanse como dormidas un momento y brincaban de nuevo sobresaltadas, dispersándose, trepando unas por las paredes hasta los cristales temblorosos de los faroles, otras hasta los carteles de papel mal pegado a las esquinas, y había pluma que llegaba a un tercer piso, y arenilla que se incrustaba para días, o para años, en la vidriera de un escaparate, agarrada a un plomo. Vetusta, la muy noble y leal ciudad, corte en lejano siglo, hacía la digestión del cocido y de la olla podrida, y descansaba oyendo entre sueños el monótono y familiar zumbido de la campana de coro, que retumbaba allá en lo alto de la esbelta torre en la Santa Basílica. La torre de la catedral, poema romántico de piedra,delicado himno, de dulces líneas de belleza muda y perenne, era obra del siglo diez y seis, aunque antes comenzada, de estilo gótico, pero, cabe decir, moderado por un instinto de prudencia y armonía que modificaba las vulgares exageraciones de esta arquitectura. La vista no se fatigaba contemplando horas y horas aquel índice de piedra que señalaba al cielo; no era una de esas torres cuya aguja se quiebra desutil, más flacas que esbeltas, amaneradas, como señoritas cursis que aprietan demasiado el corsé; era maciza sin perder nada de su espiritual grandeza, y hasta sus segundos corredores, elegante balaustrada, subía como fuerte castillo, lanzándose desde allí en pirámide de ángulo gracioso, inimitable en sus medidas y proporciones. Como haz de músculos y nervios la piedra enroscándose en la piedra trepaba a la altura, haciendo equilibrios de acróbata en el aire; y como prodigio de juegos malabares, en una punta de caliza se mantenía, cual imantada, una bola grande de bronce dorado, y encima otra más pequeña, y sobre ésta una cruz de hierro que acababa en pararrayos.'

#mensaje_codificado,alfabeto,frecuencias=EncodeArithmetic(mensaje,numero_de_simbolos=1)

#mensaje_recuperado=DecodeArithmetic(mensaje_codificado,len(mensaje),alfabeto,frecuencias)

#ratio_compresion=8*len(mensaje)/len(mensaje_codificado)
#print(ratio_compresion)

#if (mensaje!=mensaje_recuperado):
#        print('!!!!!!!!!!!!!!  ERROR !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')


mensaje_codificado = '010001110001010011000000110000001001001011110001010001100100111010101110010000101001101110010100110101111001100010111010011110110101110010001010111001000010011100010111101111111011000111110000001010010110010110111011101011011010100010110101100110010111001001010100110111100111011010101011000011101001010011100000001110100100001001001011100110111000110110100101101001110000100000000111100100011010100000110000000001111111010100010001000011111110010110011000011001110011110100111011001001111000110111101111101110010111100001111100011100010111111011010010001010101011101110011011010000010101010100110000011000101111100101110011000010101100100101100100001000011001101110110111111111110001100001100011110111111000000011101111001010110110011101010001101010000011101011101100100000100011110101001001010001011011111010111101111101110000010000101011011101111110001101011001111110010001110100101100100100110001010010110000110110111101000100100000000011111000011111010100101010100100100000101111111101000001010001011110000111010011111000101011111000100100010100100010000110000101011010001101111110111111111111111111001111110000010010110110101000001101111100010001101100100111001100100000000'

alfabeto = [' ', '(', ')', '.', '1', '8', '9', 'C', 'E', 'G', 'H', 'I', 'L', 'M', 'S', 'T', 'W', '[', ']', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y']

frecuencias = [45, 3, 3, 6, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 1, 2, 2, 9, 3, 4, 5, 29, 4, 4, 7, 14, 1, 7, 5, 18, 14, 2, 13, 10, 15, 4, 4, 4, 1, 2]

mensaje_recuperado=DecodeArithmetic(mensaje_codificado, 258, alfabeto, frecuencias)

print("MESSAGGIO:")
print(mensaje_recuperado)

#%%

#'''
#Si no tenemos en cuenta la memoria necesaria para almacenar el alfabeto y
#las frecuencias, haced una estimación de la ratio de compresión para el
#fichero "la_regenta" que encontraréis en Atenea con numero_de_simbolos=1

#Si tenemos en cuenta la memoria necesaria para almacenar el el alfabeto y
#las frecuencias, haced una estimación de la ratio de compresión.

#Repetid las estimaciones con numero_de_simbolos=2,3,...
#'''

with open ("la_regenta.txt", encoding="utf8") as myfile:
    mensaje=myfile.read()



#mensaje_codificado, alfabeto, frecuencias = EncodeArithmetic(mensaje,1)
#print(len(mensaje))
#print(len(mensaje_codificado))
#ratio_compresion=8*len(mensaje)/(len(mensaje_codificado))
#print("ratio (con n_s=1): ", ratio_compresion)  #1.8093

#mensaje_codificado, alfabeto, frecuencias = EncodeArithmetic(mensaje,2)
#ratio_compresion=8*len(mensaje)/(len(mensaje_codificado))
#print("ratio (con n_s=2): ", ratio_compresion)  #2.0371

#mensaje_codificado, alfabeto, frecuencias = EncodeArithmetic(mensaje,3)
#ratio_compresion=8*len(mensaje)/(len(mensaje_codificado))
#print("ratio (con n_s=3)", ratio_compresion)    #2.2582

#print("tenendo enn cuenta la memoria para alfabeto y frecuencias:")
#mensaje_codificado, alfabeto, frecuencias = EncodeArithmetic(mensaje,1)
#ratio_compresion=8*len(mensaje)/(len(mensaje_codificado) + sys.getsizeof(alfabeto) + sys.getsizeof(frecuencias))
#print("ratio (con n_s=1): ", ratio_compresion)  #1.8089

#mensaje_codificado, alfabeto, frecuencias = EncodeArithmetic(mensaje,2)
#ratio_compresion=8*len(mensaje)/(len(mensaje_codificado) + sys.getsizeof(alfabeto) + sys.getsizeof(frecuencias))
#print("ratio (con n_s=2): ", ratio_compresion)  #2.0295

#mensaje_codificado, alfabeto, frecuencias = EncodeArithmetic(mensaje,3)
#ratio_compresion=8*len(mensaje)/(len(mensaje_codificado) + sys.getsizeof(alfabeto) + sys.getsizeof(frecuencias))
#print("ratio (con n_s=3): ", ratio_compresion)  #2.1985










#%%

#'''
#Comparad las ratios de compresión con las obtenidas con códigos de Huffman.

#_____________|     HUFFMAN         |      ARITMETICA
# NS = 1            1.8425                  1.8093
# NS = 2            2.0858                  2.0371
# NS = 3            2.3136                  2.2582

#con tamano estructuras:
#_____________|     HUFFMAN         |      ARITMETICA
# NS = 1            1.8338                  1.8089
# NS = 2            1.9249                  2.0295
# NS = 3            1.6880                  2.1985





#'''
