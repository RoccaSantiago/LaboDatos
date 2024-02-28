# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 17:19:29 2024

@author: Wicher
"""

import pandas as pd 
import numpy as np
import matplotlib as plt
from inline_sql import sql, sql_val

#%%

carpeta = "C:/Users/Phone/Desktop/Source2/LaboDatos/TP02-pip install grupo_1/"

datos = pd.read_csv(carpeta + "sign_mnist_train.csv")


#%%

A = (sql^"""
    SELECT ALL *
    FROM datos
    WHERE label = 0
    """).to_numpy()

for i in range(0,24):
    plt.pyplot.imshow(np.reshape(A[i,1:], (28, 28)))

#%%


