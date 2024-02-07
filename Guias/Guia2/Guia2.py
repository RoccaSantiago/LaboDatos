#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#archivo = 'arbolado-en-espacios-verdes.csv'
import csv


#%%

def leer_parque(archivo, parque):
    
    with open(archivo, encoding='utf-8') as f:
        filas = csv.reader(f)
        headers = next(filas) 
        i = 0
        res = []
        for fila in filas:
            if fila[10] == parque:
                arbol = {}
                for i in range(len(headers)):              
                    if headers[i] == "espacio_ve":
                        continue
                    else:
                        arbol[headers[i]] = fila[i]
                res.append(arbol)
                arbol = {}
        return res
       

#print(len(leer_parque('arbolado-en-espacios-verdes.csv',"GENERAL PAZ")))

#%%

def especies(lista):
    conjunto = set()
    for arbol in range(len(lista)):
        conjunto.add(lista[arbol]["nombre_com"])
    return conjunto

#print(especies(leer_parque('arbolado-en-espacios-verdes.csv',"GENERAL PAZ")))

#%%

def contar_ejemplares(lista):
    res = {}
    for especie in (especies(lista)):
        cantidad = 0
        for arbol in lista:
            if arbol["nombre_com"] == especie:
                cantidad+=1
        res[especie] = cantidad
        cantidad = 0
    return res


#print(contar_ejemplares(leer_parque('arbolado-en-espacios-verdes.csv',"GENERAL PAZ")))

#%%

def obtener_alturas(arboles, especie):
    res = []
    for arbol in arboles:
        if arbol["nombre_com"] == especie:
            res.append(float(arbol["altura_tot"]))
    return res
            
#print(obtener_alturas(leer_parque('arbolado-en-espacios-verdes.csv',"GENERAL PAZ"), "Eucalipto"))

#%%

def obtener_inclinacion(arboles, especie):
    res = []
    for arbol in arboles:
        if arbol["nombre_com"] == especie:
            res.append(float(arbol["inclinacio"]))
    return res
#%%

def especimen_mas_inclinado(arboles):
     especimenes = especies(arboles)
     mayor_inclinacion = 0
     mayor_especie = ""
     for especie in especimenes:
         inclinaciones = obtener_inclinacion(arboles, especie)
         for inclinacion in inclinaciones:
             if inclinacion > mayor_inclinacion:
                 mayor_inclinacion = inclinacion
                 mayor_especie = especie
     return mayor_especie
             

#print(especimen_mas_inclinado(leer_parque('arbolado-en-espacios-verdes.csv',"CENTENARIO")))        
         
         

#%%

def especie_promedio_mas_inclinada(arboles):
     especimenes = especies(arboles)
     mayor_inclinacion = 0
     mayor_especie = ""
     for especie1 in especimenes:
         inclinaciones = obtener_inclinacion(arboles, especie1)
         suma = 0
         for inclinacion in inclinaciones:
             suma = suma + inclinacion
         a = suma / len(inclinaciones)
         if a > mayor_inclinacion:
             mayor_inclinacion = a
             mayor_especie = especie1
     return("La especie de mayor inclinacion es " + mayor_especie + " con " + mayor_inclinacion)
      
print(especimen_mas_inclinado(leer_parque('arbolado-en-espacios-verdes.csv'," ANDES, LOS")))  
 