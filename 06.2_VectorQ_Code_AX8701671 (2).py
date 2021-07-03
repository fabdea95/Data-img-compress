# -*- coding: utf-8 -*-

########################################################
from scipy import misc
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
import matplotlib._color_data as mcd

import pickle


import random

import time
import scipy.ndimage
from scipy.cluster.vq import vq, kmeans, whiten
import imageio
import PIL

#plt.ion()

#%%
#ingresar la ruta de la carpeta de las imagenes aquí:
IMAGEPATH = r".\standard_test_images"
#%%


#%%
"""

IMPORTANTE:

K-means clustering and vector quantization

http://docs.scipy.org/doc/scipy/reference/cluster.vq.html

Podéis usar las funciones implementadas, en particular vq y kmeans



"""
#%%

imagen=imageio.imread('./standard_test_images/jetplane.png')
# imagen=imageio.imread('../standard_test_images/mandril_gray.png')
# imagen=imageio.imread('../standard_test_images/crosses.png')
# imagen=imageio.imread('../standard_test_images/circles.png')
# imagen=imageio.imread('../standard_test_images/cameraman.png')
# imagen=imageio.imread('../standard_test_images/walkbridge.png')
#imagen = misc.ascent()

(n,m)=imagen.shape # filas y columnas de la imagen
n_bloque=8


#%%
"""
Definir una funcion que dada una imagen
la cuantize vectorialmente usando K-means
"""

def Cuantizacion_vectorial_KMeans(imagen, entradas_diccionario=2**8, n_bloque=8):
    (n, m) = imagen.shape
    imagenCodigo = []
    imagenCodigo.append(np.asarray([n, m, n_bloque]))
    Diccionario = []
    index = 0
    for i in range (0, n, n_bloque):
        for j in range (0, m, n_bloque):
            Diccionario.append(np.ravel(np.asarray(imagen[i:(i+n_bloque), j:(j+n_bloque)]))) #per ora ogni blocco è una riga

    #print(len(Diccionario))

    Dic = np.stack(Diccionario, axis=0)
    #print(Diccionario[0])
    #print(imagen[0:(n_bloque), 0:(n_bloque)])

    #print(Dic.shape)
    #print(Dic[0])
    #imagenCodigo.append(Diccionario)

    codebook, dist = kmeans(Dic.astype(float), entradas_diccionario)
    #print("CODEBOOK:")
    #print(codebook)
    #print(codebook.shape)
    imagenCodigo.append((codebook).astype(np.uint8))
    print("DISTORTION: ", dist)
    (indices, dist) = vq(Dic, codebook)
    #print(codebook, dist)
    #print(indices, dist)
    imagenCodigo.append(indices)
    return imagenCodigo



"""
imagen: imagen a cuantizar
entradas_diccionario: número máximo de entradas del diccionario usado para
       codificar.
n_bloque: Las entradas del diccionario serán bloques de la imagen de
       tamaño n_bloque*n_bloque

imagenCodigo: es una lista de la forma
[[n,m,n_bloque],Diccionario,indices]

siendo:
[n,m,n_bloque] información de la imagen
  n: número de filas de la imagen
  m: número de columnas de la imagen
  n_bloque: tamaño de los bloques usados (múltiplo de n y m)
Ejemplo: [1024, 1024, 8]

Diccionario: lista de arrays cuyos elementos son bloques de la imagen se
     usan como diccionario para cuantizar vectorialmente la imagen
Ejemplo:
    [
    array([[173, 172, 172, 171, 171, 171, 171, 172],
       [173, 172, 172, 172, 171, 171, 171, 171],
       [172, 172, 172, 172, 171, 171, 170, 170],
       [172, 172, 171, 171, 171, 171, 170, 169],
       [172, 171, 171, 171, 171, 171, 170, 169],
       [171, 171, 170, 170, 170, 170, 170, 169],
       [171, 171, 170, 170, 170, 170, 169, 169],
       [171, 171, 171, 170, 170, 169, 169, 169]], dtype=uint8),
    array([[132, 131, 128, 122, 118, 117, 121, 124],
       [129, 132, 132, 128, 122, 119, 118, 119],
       [122, 128, 133, 133, 128, 123, 119, 116],
       [115, 121, 128, 131, 132, 130, 124, 119],
       [114, 117, 122, 126, 131, 134, 131, 126],
       [109, 114, 118, 122, 127, 133, 135, 132],
       [ 91, 102, 113, 117, 121, 127, 132, 133],
       [ 70,  89, 107, 114, 115, 120, 127, 131]], dtype=uint8)
...]

indices: array que contiene los índices de los elementos del diccionario
    por los que hay que sustituir los bloques de la imagen
Ejemplo: array([14, 124, 22, ...,55, 55, 356], dtype=int32)]
    Al reconstruir la imagen el primer bloque se sustituirá por el bloque 14
    del diccionario, el segundo se sustituirá por el bloque 124 del
    diccionario,..., el último se substituirá por el bloque 356 del
    diccionario.


Importante: Trabajar con Arrays de Numpy

"""


#%%
"""
Definir una funcion que dada una imagen codificada por la función
Cuantizacion_vectorial_KMeans muestre la imagen codificada.
cuantize uniformemente los valores en cada bloque

"""

def Dibuja_imagen_cuantizada_KMeans(imagenCodigo):
    info = imagenCodigo.pop(0) # info[0]=n, info[1]=m, info[2]=n_bloque
    first = 1
    #print(imagenCodigo[0][imagenCodigo[1][0]])
    #print(imagenCodigo[0][0])
    bloque = imagenCodigo[0][imagenCodigo[1][0]].reshape(info[2],info[2])
    #print("bloq")
    #print(bloque)
    (nb,mb) = bloque.shape
    imagenRecuperada = np.empty((nb,info[1]), int)
    row = np.empty((nb,mb), int)
    #print("first bloque: ")
    #print((imagenCodigo[0][imagenCodigo[1][0]]).reshape(info[2],info[2]))
    for i in range (0, len(imagenCodigo[1])):

        bloque = np.empty((nb,mb), int)
        bloque = (imagenCodigo[0][imagenCodigo[1][i]]).reshape(info[2],info[2])
        (nr,mr) = row.shape
        #if i % (n/n_bloque) == 0: #nuevo bloque linea
        if i % (info[0]/info[2]) == 0:
            row = np.empty((nb,mb), int)
        row = bloque
        (nr,mr) = row.shape
        #print(row.shape)
        if info[1] == mr: #si termino una "linea" de altitud n_bloque
            #print(row)
            if first == 1:
                imagenRecuperada = row
                first = 0
            else:
                imagenRecuperada = np.concatenate((imagenRecuperada, row), axis=0)
        else:
            row = np.concatenate((row, bloque), 1)
    return imagenRecuperada

 #%%
"""
Aplicar vuestras funciones a las imágenes que encontraréis en la carpeta
standard_test_images hacer una estimación de la ratio de compresión
"""

#print(imagen)

#%%
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
#%%
"""
Algunas sugerencias que os pueden ser útiles
"""

# Divido todos los píxeles de la imagen por q
# a continuación redondeo todos los píxeles
# a continuación sumo 1/2 a todos los píxeles de la imagen
# a continuación convierto los valores de todos los píxeles en enteros de 8 bits sin signo
# por último múltiplico todos los píxeles de la imagen por q

bits=3
#=2**(bits)
#imagen2=((np.floor(imagen/q)+1/2).astype(np.uint8))*q

# dibujo la imagen cuanzizada resultante

#fig=plt.figure()
#fig.suptitle('Bloques: '+str(bits)+' bits/píxel')
#plt.xticks([])
#plt.yticks([])
#plt.imshow(imagen, cmap=plt.cm.gray,vmin=0, vmax=255)
#plt.show()


# Lectura y escritura de objetos

#import pickle

#fichero='QScalar'

#with  open(fichero+'_dump.pickle', 'wb') as file:
#    pickle.dump(imagenCodigo, file)


#with open(fichero, 'rb') as file:
#    imagenLeidaCodificada=pickle.load(file)


# Convertir un array en imagen, mostrarla y guardarla en formato png.
# La calidad por defecto con que el ecosistema python (ipython, jupyter,...)
# muestra las imágenes no hace justicia ni a las imágenes originales ni a
# las obtenidas tras la cuantización.

import PIL
import os
from os import listdir
from os.path import isfile, join


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
        imagenCodigo = Cuantizacion_vectorial_KMeans(imagen)
        imagenRecuperada = Dibuja_imagen_cuantizada_KMeans(imagenCodigo)
        imagenPIL=PIL.Image.fromarray(imagenRecuperada)
        #imagenPIL.show()
        imagenPIL.save(f + '_imagen.jpeg', 'JPEG')
        print("imagen comprimida almacenada como: ", f + '_imagen.jpeg' )
        print("mostrando imagen comprimida en nueva ventana...")
        imagenPIL.show(title="IMAGEN COMPRIMIDA")
        print("COMPRESSION RATE: ", os.path.getsize(ff)/os.path.getsize(f+'_imagen.jpeg'))
    except Exception as e:
        pass
