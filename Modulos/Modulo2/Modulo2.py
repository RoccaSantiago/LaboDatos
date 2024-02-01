#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import numpy as np
import csv
import os
import pandas as pd


#%%

#Ejercicio de clase

def geromgosoopt(palabra):
    vocales = ["a","e","i","o","u"]
    res = ""
    for c in palabra:
        res += c
        if c in vocales:
            res += "p" + c
    return res

def geringosolista(lista):
    res = {}
    for c in lista:
        res[c] = geromgosoopt(c)
    return res

#print(geringosolista(["hola","bola", "tartamudo"]))

#%%

#f = open("datame.txt", "rt")

#data = f.read()

#print(data)

#f.close()

#with open("datame.txt","rt") as f:
    #data = f.read 
    
#%%

#with open("cronograma_sugerido.csv", "rt") as file:
    #for line in file:
        #datos_linea = line.split(",")
        #print(datos_linea[1])
        
#%% 

#EJercicios de clase

def tiradaGenerala():
    res = []
    for i in range(0,6):
        res.append(random.randint(1, 6))
    return res

#print(tiradaGenerala())

def estaEstudiante():
    f = open("datame.txt", "rt")
    data = f.read()
    f.close()
    a = data.split("\n")
    
    for line in a:
        if "estudiante" in line:
            print(line)

#estaEstudiante()

def listaDeMaterias():
    with open("cronograma_sugerido.csv", "rt") as file:
        for line in file:
            datos_linea = line.split(",")
            print(datos_linea[1])
            

#listaDeMaterias()

def cuantasPorHacer(n):
    res = 0
    with open("cronograma_sugerido.csv", "rt") as file:
        for line in file:
            datos_linea = line.split(",")
            if (datos_linea[0]=="Cuatrimestre"):
                #print("asaaaaa")
                continue
                
            else:
                #print(datos_linea[0])
                if int(datos_linea[0]) == n:
                    res+=1
    return res

#cuantasPorHacer(5)

def materias_cuatrimestre(nombre, n):
    res = []
    f = open(nombre)
    filas = csv.reader(f)
    next(filas)
    for fila in filas:
        materia = {}
        if fila[0] == n:
            materia["Cuatrimestre"] = fila[0]
            materia["Asignatura"] = fila[1]
            materia["correlativas"] = fila[2]
            res.append(materia)
            materia = {}
    return res

#materias_cuatrimestre(cronograma_sugerido.csv, 3)
    
#%%

def ejerciciovector():
    return np.arrange(17)
    
#print(ejerciciovector())

def ejerciciolinespace():
    return np.linspace(0, 16)
    
#print(ejerciciolinespace())

def pisarlosnumeros(matriz,e):
    for fila in range(len(matriz)):
        for columna in range(len(matriz[fila])):
            if matriz[fila][columna]== e:
                matriz[fila][columna] = -1
    return matriz

#%%

archivo = 'arbolado-en-espacios-verdes.csv'
fname = os.path.join(r"C:\Users\Phone\Desktop\LaboDatos\Modulos\Modulo2", archivo)
df = pd.read_csv(fname)

#print(df.head())


dfJacaranda= df[df['nombre_com'] == "Jacarandá"].copy()
dfPaloBorracho = df[df['nombre_com'] == "Palo borracho"].copy()

#print((dfJacaranda['nombre_com'] == 'Jacarandá').sum())
#print((dfPaloBorracho['nombre_com'] == 'Palo borracho').sum())

#PREGUNTAR PREGUNTAR PREGUNTAR PREGUNTAR PREGUNTAR PREGUNTAR PREGUNTAR PREGUNTAR PREGUNTAR PREGUNTAR PREGUNTAR PREGUNTAR PREGUNTAR PREGUNTAR PREGUNTAR PREGUNTAR 
#VPREGUNTAR PREGUNTAR PREGUNTAR PREGUNTAR PREGUNTAR PREGUNTAR PREGUNTAR PREGUNTAR PREGUNTAR PREGUNTAR 
#PREGUNTAR PREGUNTAR PREGUNTAR PREGUNTAR PREGUNTAR PREGUNTAR PREGUNTAR PREGUNTAR PREGUNTAR PREGUNTAR 
#Como hago para imprimir no mas las filas que yo quiera, tipo el minimo, promedio, cantidad, el heather y el maximo
#hay que usar iloc pero no me dejar sumar los strings para imprimir

#print(dfJacaranda[['altura_tot', 'diametro']].describe())
#print(dfPaloBorracho[['altura_tot', 'diametro']].describe())

def cantidadArboles(parque):
    return (df["espacio_ve"] == parque).sum()

#print(cantidadArboles("GENERAL PAZ"))



def cantidadArbolesNativos(parque):
    return ((df['espacio_ve'] == parque) & (df['origen'] == 'Nativo/Autóctono'))
    
#print(cantidadArbolesNativos("PUEYRREDON"))
        


#%%

archivo1 = 'arbolado-en-espacios-verdes1.csv'
fname1 = os.path.join(r"C:\Users\Phone\Desktop\LaboDatos\Modulos\Modulo2", archivo1)
df1 = pd.read_csv(fname1)

df2 = df1[['nombre_cientifico', 'ancho_acera', 'diametro_altura_pecho', 'altura_arbol']].copy()
data_arboles_veredas = df2['nombre_cientifico'].value_counts()

#print(data_arboles_veredas.head(10)) 




