# -*- coding: utf-8 -*-
"""



"""

########################################################
from scipy import misc
import scipy
import numpy as np
import time
import matplotlib.pyplot as plt
import imageio
import PIL
import pickle
import math




IMAGEPATH = r".\standard_test_images"

#%%



#%%
"""
Definir una funcion que dada una imagen
cuantize uniformemente los valores en cada bloque
"""

def Cuantizacion_uniforme_adaptativa(imagen, bits=3, n_bloque=8):
    dim = 0
    (n, m) = imagen.shape   # filas y columnas de la imagen
    imagenCodigo = []
    imagenCodigo.append(np.asarray([n, m, n_bloque, bits]))
    bloqueCodificado = np.empty((n_bloque,n_bloque), int)

    for i in range (0, n, n_bloque):
        for j in range (0, m, n_bloque):
            bloque = np.empty((n_bloque,n_bloque), int)
            bloque = imagen[i:(i+n_bloque), j:(j+n_bloque)]
            bloqueCodificado = np.empty((n_bloque,n_bloque), int)
            max = np.amax(bloque)
            #print(max)
            min = np.amin(bloque)
            #print(min)
            delta = (max - min)/(2**bits)
            for k in range(0, n_bloque):
                for l in range(0, n_bloque):
                    if (max - min) == 0:
                        bloqueCodificado[k][l] = 0
                    else:
                        bloqueCodificado[k][l] = int((((bloque[k][l])-min)/delta))
                        if (bloqueCodificado[k][l] == 2**bits):
                            bloqueCodificado[k][l] = bloqueCodificado[k][l] - 1
            imagenCodigo.append([[min, max], bloqueCodificado])

            #print(bloqueCodificado)
            #print(imagenCodigo)

#DESCOMENTAR PARA IMPRIMIR CODIGO:
    #print(imagenCodigo)

    return imagenCodigo


"""
imagen: imagen a cuantizar
bits: número de bits necesarios para cuantizar cada bloque,
      o sea que en cada bloque habrá 2**bits valores diferentes como máximo
n_bloque: se consideran bloques de tamaño n_bloque*n_bloque

imagenCodigo: es una lista de la forma
[[n,m,n_bloque,bits],[[minimo,maximo],bloqueCodificado],...,[[minimo,maximo],bloqueCodificado]]

siendo:
[n,m,n_bloque,bits] información de la imagen
  n: número de filas de la imagen
  m: número de columnas de la imagen
  n_bloque: tamaño de los bloques usados (múltiplo de n y m)
Ejemplo: [1024, 1024, 8, 3]

[[minimo,maximo],bloqueCodificado] información de cada bloque codificado
minimo: valor mínimo del bloque
maximo: valor máximo del bloque
bloqueCodificado: array de tamaño n_bloque*n_bloque que contiene en cada
  posición a que intervalo de cuantización correspondía el valor del píxel
  correspondiente en la imagen

Ejemplo: sabemos que trabajamos con bloques 8x8 y que hemos cuantizado en 2**3=8 niveles
    [[85, 150],
    Array([[4, 0, 0, 4, 7, 7, 6, 7],
           [4, 3, 1, 1, 4, 7, 7, 6],
           [6, 6, 3, 0, 0, 4, 6, 6],
           [6, 6, 5, 3, 1, 0, 3, 6],
           [6, 5, 6, 6, 4, 0, 0, 3],
           [5, 6, 6, 6, 6, 4, 2, 0],
           [6, 6, 5, 5, 6, 7, 4, 1],
           [6, 6, 5, 5, 5, 6, 6, 5]]
   El valor mínimo de los píxeles del bloque era 85 y el máximo 150, por lo
   tanto los límites de decisión son:
       [85.0, 93.25, 101.5, 109.75, 118.0, 126.25, 134.5, 142.75, 151.0]
   el valor del primer pixel (4) estaría entre 109.75<=p<118
   el valor del segundo pixel pixel (0) estaría entre 85<=p<93.25...


Importante: Trabajar con Arrays de Numpy

"""


#%%
"""
Definir una funcion que dada una imagen codificada por la función
Cuantizacion_uniforme_adaptativa() muestre la imagen

"""

def Dibuja_imagen_cuantizada(imagenCodigo):
    info = imagenCodigo.pop(0) # info[0]=n, info[1]=m, info[2]=n_bloque, info[3]=bits
    del imagenCodigo[0]
    first = 1
    bloque = imagenCodigo[0][1]
    (nb,mb) = bloque.shape
    imagenRecuperada = np.empty((nb,info[1]), int)
    row = np.empty((nb,mb), int)

    for i in range(0,len(imagenCodigo)):
        bloque = np.empty((nb,mb), int)
        bloque = imagenCodigo[i][1]
        #print(bloque)
        delta = (imagenCodigo[i][0][1] - imagenCodigo[i][0][0])/(2**info[3])
        min = imagenCodigo[i][0][0]
        #print(delta)
        bloque = np.floor(bloque*delta + min + delta/2).astype(np.uint8)
        #if i % (n/n_bloque) == 0: #nuevo bloque linea
        if i % (info[0]/info[2]) == 0:
            row = np.empty((nb,mb), int)
            row = bloque
        (nr,mr) = row.shape
        #print(n)
        #print(mr)
        if info[0] == mr: #si termino una "linea" de altitud n_bloque
            #print(row)
            if first == 1:
                imagenRecuperada = row
                first = 0
            else:
                imagenRecuperada = np.concatenate((imagenRecuperada, row), axis=0)
        else:
            row = np.concatenate((row, bloque), 1)
    imagenRecuperada = np.concatenate((imagenRecuperada, row), axis=0)

    print(imagenRecuperada.shape)
    print(imagenRecuperada)
    #plt.xticks([])
    #plt.yticks([])
    #plt.imshow(imagenRecuperada, cmap=plt.cm.gray,vmin=0, vmax=255)
    #plt.show()
    return imagenRecuperada


 #%%
"""
Aplicar vuestras funciones a las imágenes que encontraréis en la carpeta
standard_test_images hacer una estimación de la ratio de compresión
"""


import PIL
import os
from os import listdir
from os.path import isfile, join
from PIL import Image

files = [f for f in listdir(IMAGEPATH) if isfile(join(IMAGEPATH, f))]


for f in files:
    try:
        ff = os.path.join(IMAGEPATH, f)
        imagen=imageio.imread(ff)
        plt.figure(ff)
        plt.xticks([])
        plt.yticks([])
        plt.imshow(imagen, cmap=plt.cm.gray,vmin=0, vmax=255)
        plt.show()
        print("")
        print(f)
        imagenCodigo = Cuantizacion_uniforme_adaptativa(imagen, bits=3, n_bloque=8)
        imagenPIL=PIL.Image.fromarray(Dibuja_imagen_cuantizada(imagenCodigo))
        imagenPIL.save(f + '_imagen.png', 'PNG')
        print("imagen comprimida almacenada como: ", f + '_imagen.png' )
        print("mostrando imagen comprimida en nueva ventana...")
        imagenPIL.show(title="IMAGEN COMPRIMIDA")
        print("COMPRESSION RATE: ", os.path.getsize(ff)/os.path.getsize(f+'_imagen.png'))
    except Exception as e:
        pass
