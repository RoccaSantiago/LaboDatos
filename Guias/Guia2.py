#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os 

frame = os.path.join("Home/Estudiante/Escritorio",'arbolado-en-espacios-verdes.csv')

df = pd.read_csv(frame)

#%%

def leer_parque(nombre_archivo, parque):
    
   a =  df["espacio_ve" == parque]
   
   print(a)
