# -*- coding: utf-8 -*-
"""

"""

import numpy as np
import scipy
import imageio
import math
import scipy.fftpack



import matplotlib.pyplot as plt






#Matrices de cuantización, estándares y otras
#"""


Q_Luminance=np.array([
[16 ,11, 10, 16,  24,  40,  51,  61],
[12, 12, 14, 19,  26,  58,  60,  55],
[14, 13, 16, 24,  40,  57,  69,  56],
[14, 17, 22, 29,  51,  87,  80,  62],
[18, 22, 37, 56,  68, 109, 103,  77],
[24, 35, 55, 64,  81, 104, 113,  92],
[49, 64, 78, 87, 103, 121, 120, 101],
[72, 92, 95, 98, 112, 100, 103, 99]])

Q_Chrominance=np.array([
[17, 18, 24, 47, 99, 99, 99, 99],
[18, 21, 26, 66, 99, 99, 99, 99],
[24, 26, 56, 99, 99, 99, 99, 99],
[47, 66, 99, 99, 99, 99, 99, 99],
[99, 99, 99, 99, 99, 99, 99, 99],
[99, 99, 99, 99, 99, 99, 99, 99],
[99, 99, 99, 99, 99, 99, 99, 99],
[99, 99, 99, 99, 99, 99, 99, 99]])

def Q_matrix(r=1):
    m=np.zeros((8,8))
    for i in range(8):
        for j in range(8):
            m[i,j]=(1+i+j)*r
    return m
#%%
#"""
#Implementar la DCT (Discrete Cosine Transform)
#y su inversa para bloques NxN (podéis utilizar si quereis el paquete scipy.fftpack)

#dct_bloque(p,N)
#idct_bloque(p,N)

#p bloque NxN
#
#"""
def dct_bloque(p):
    return scipy.fftpack.dct(scipy.fftpack.dct(p.T, norm='ortho').T, norm='ortho')

def idct_bloque(p):
    return scipy.fftpack.idct(scipy.fftpack.idct(p.T, norm='ortho').T, norm='ortho')

#%%
#"""
#Reproducir los bloques base de la transformación para los casos N=4,8
#Ver imágenes adjuntas.
#"""

#%%
#"""
#Implementar la función jpeg_gris(imagen_gray) que:
#1. dibuje el resultado de aplicar la DCT y la cuantización
#(y sus inversas) a la imagen de grises 'imagen_gray'

#2. haga una estimación de la ratio de compresión
#según los coeficientes nulos de la transformación:
#(#coeficientes/#coeficientes no nulos).

#3. haga una estimación del error
#Sigma=np.sqrt(sum(sum((imagen_gray-imagen_jpeg)**2)))/np.sqrt(sum(sum((imagen_gray)**2)))


#"""

def jpeg_gris(imagen_gray):
    nulos = 0
    (n,m) = imagen_gray.shape
    bloque = np.empty((8,8))
    imagendct = imagen_gray
    matrix = Q_matrix()
    print(imagen_gray)
    print(matrix)
    for i in range (0, n, 8):
        for j in range (0, m, 8):
            bloque = np.empty((8,8))
            bloque = imagen_gray[i:(i+8), j:(j+8)]
            bloqueCodificado = dct_bloque(bloque)
            #if i==0 and j==0:
            #    print(bloqueCodificado)
            imagendct[i:(i+8), j:(j+8)] = bloqueCodificado/matrix + 0.5
            #print(imagendct[i:(i+8), j:(j+8)])
    #print(imagendct)
    for i in range (0,n):
        for j in range(0, m):
            if imagendct[i][j] != 0:
                nulos = nulos + 1

    print ("ratio compresión: ",(n*m)/nulos)
    imagen_final = np.empty((n,m), int)
    for i in range (0, n, 8):
        for j in range (0, m , 8):
            bloque = np.empty((8,8))
            bloqueDec = np.empty((8,8))
            bloque = imagendct[i:(i+8), j:(j+8)]

            bloqueDec = np.multiply(bloque,matrix)
            #print(bloqueDec)
            bloqueDec = idct_bloque(bloqueDec)
            #print("IDCT: ")
            #print(bloqueDec)
            imagen_final[i:(i+8), j:(j+8)] = bloqueDec
            #print(imagen_final[i:(i+8), j:(j+8)])
    sum = 0
    sum2 = 0
    for i in range(0,n):
        for i in range(0,m):
            sum = sum + (imagen_gray[i][j] - imagen_final[i][j])**2
            sum2 = sum2 + (imagen_gray[i][j])**2
    print("error: ", np.sqrt(sum)/np.sqrt(sum2))
    return imagen_final.astype(np.int32)

#%%
#"""
#Implementar la función jpeg_color(imagen_color) que:
#1. dibuje el resultado de aplicar la DCT y la cuantización
#(y sus inversas) a la imagen RGB 'imagen_color'

#2. haga una estimación de la ratio de compresión
#según los coeficientes nulos de la transformación:
#(#coeficientes/#coeficientes no nulos).

#3. haga una estimación del error para cada una de las componentes RGB
#Sigma=np.sqrt(sum(sum((imagen_color-imagen_jpeg)**2)))/np.sqrt(sum(sum((imagen_color)**2)))

#"""

def jpeg_color(imagen_color):
    #imagen_color = imagen_color.Image.open()
    nulos = 0
    (n,m,c) = imagen_color.shape
    bloque = np.empty((8,8,c))
    imagendct = imagen_color
    #print("init: ")
    #print(imagendct)
    for i in range (0, n, 8):
        for j in range (0, m, 8):
            for k in range (0,c):
                bloque = np.empty((8,8,c))
                bloque = imagen_color[i:(i+8), j:(j+8),k]
                bloqueCodificado = dct_bloque(bloque)
                if k == 0:
                    #print("lum")
                    imagendct[i:(i+8), j:(j+8), k] = bloqueCodificado/Q_Luminance + 0.5
                else:
                    imagendct[i:(i+8), j:(j+8), k] = bloqueCodificado/Q_Chrominance + 0.5

    for k in range (0,c):
        for i in range (0,n):
            for j in range(0, m):
                if imagendct[i][j][k] != 0:
                    nulos = nulos + 1
    #print(nulos)
    #print(n*m*c)
    #print((n*m*c)/nulos)
    print ("ratio compresión: ",(n*m*c)/nulos)
    imagen_final = np.empty((n, m, c), int)
    for i in range(0,n,8):
        for j in range (0, m, 8):
            for k in range (0, c):
                bloque = np.empty((8,8,c))
                bloqueDec = np.empty((8,8,c))
                bloque = imagendct[i:(i+8), j:(j+8), k]
                if k == 0:
                    bloqueDec = np.multiply(bloque, Q_Luminance)
                else:
                    bloqueDec = np.multiply(bloque, Q_Chrominance)
                #print(bloqueDec)
                bloqueDec = idct_bloque(bloqueDec)
                #print("IDCT: ")
                #print(bloqueDec)
                imagen_final[i:(i+8), j:(j+8),k] = bloqueDec
                #print(imagen_final[i:(i+8), j:(j+8)])
    #print("final: ")
    #print(imagen_final)
    sum = 0
    sum2 = 0
    print(imagen_final.shape)
    for i in range(0,n):
        for j in range(0,m):
            for k in range (0, c):
                sum = (sum + (imagen_color[i][j][k] - imagen_final[i][j][k])**2).astype(np.uint32)
                sum2 = (sum2 + (imagen_color[i][j][k])**2).astype(np.uint32)
    print("error: ", np.sqrt(sum)/np.sqrt(sum2))
    return imagen_final.astype(np.int32)

#%%
#"""
#--------------------------------------------------------------------------
#Imagen de GRISES

#--------------------------------------------------------------------------
#"""


### .astype es para que lo lea como enteros de 32 bits, si no se
### pone lo lee como entero positivo sin signo de 8 bits uint8 y por ejemplo al
### restar 128 puede devolver un valor positivo mayor que 128
import PIL
from PIL import Image
import time
from scipy import misc

mandril_gray=imageio.imread('mandril_gray.png').astype(np.int32)

start= time.clock()
mandril_jpeg=jpeg_gris(mandril_gray).astype(int)
end= time.clock()
imageio.imwrite('mandril_jpeg.jpeg', mandril_jpeg)
print("imagen guardada como: mandril_jpeg.jpeg ")
print("tiempo",(end-start))

#%%
#"""
#--------------------------------------------------------------------------
#Imagen COLOR
#--------------------------------------------------------------------------
#"""

#mandril_color=imageio.imread('./mandril_color.png').astype(np.int32)
#print(mandril_color)
mandril_color = np.array(Image.open('mandril_color.png').convert('YCbCr')).astype(np.int32)
#print(mandril_color[:,:,0])     #Y
#print(mandril_color[:,:,1])     #Cb
#print(mandril_color[:,:,2])     #Cr
start= time.clock()
mandril_jpeg2=jpeg_color(mandril_color)
end= time.clock()
print("MANDRIL")
print(mandril_jpeg2)

im = Image.fromarray(mandril_jpeg2, 'YCbCr')
im = im.convert('RGB')
imageio.imwrite('mandril_color_jpeg.jpeg', im)
print("imagen guardada como: mandril_color_jpeg.jpeg ")
print("tiempo",(end-start))
