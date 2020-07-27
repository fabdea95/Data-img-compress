import math
import numpy as np
import matplotlib.pyplot as plt


#'''
#Dada una lista p, decidir si es una distribución de probabilidad (ddp)
#0<=p[i]<=1, sum(p[i])=1.
#'''
def es_ddp(p,tolerancia=10**(-5)):
    somma = 0
    resp = True
    for i in range(0,len(p)):
        if p[i] > 1 :
            resp = False
            return risp
        else:
            somma = somma + p[i]
            if somma > 1 :
                resp = False
                return resp
    return resp



#'''
#Dado un código C y una ddp p, hallar la longitud media del código.
#'''

def LongitudMedia(C,p):
    l=0
    for i in range(0, len(p)) :
        l=l+len(C[i])*p[i]
    return l

#'''
#Dada una ddp p, hallar su entropía.
#'''
def H1(p):
    entr=0.0
    for i in range(0,len(p)):
        if p[i] != 0:
            entr = entr + p[i]*math.log2(1/p[i])
    return entr

#'''
#Dada una lista de frecuencias n, hallar su entropía.
#'''

def H2(n):
    suma = sum(n)
    entr=0
    for i in range(0,len(n)):
        if n[i] != 0:
            p = n[i]/suma
            entr = entr +p*math.log2((1/p))
    return entr


#Ejamples:
C=['001','101','11','0001','000000001','0001','0000000000']
p=[0.5,0.1,0.1,0.1,0.1,0.1,0]
n=[5,2,1,1,1]
p = [0.26, 0.082, 0.233, 0.082, 0.342]
p = [0.1956, 0.2717, 0.1522, 0.1847, 0.1956]
print("ANSWER")
print(H1(p))
print(H2(n))
print(LongitudMedia(C,p))



#'''
#Dibujar H([p,1-p])
#'''
print(es_ddp(p))
