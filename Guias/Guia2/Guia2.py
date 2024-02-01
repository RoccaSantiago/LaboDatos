#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os 

archivo = 'arbolado-en-espacios-verdes.csv'



#%%

def leer_parque(nombre_archivo, parque):
    
   frame = os.path.join(r"C:\Users\Phone\Desktop\LaboDatos\Guias\Guia2" , archivo)
   
   df = pd.read_csv(frame)
   
   res = []
   
   dfParque = df[df["espacio_ve"] == parque]
   for i in dfParque:
       arbol = {}
       datos = {}
       arbol[idArbol] = datos
       
       
