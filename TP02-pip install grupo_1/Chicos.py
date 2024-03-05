
import pandas as pd
import numpy as np
from inline_sql import sql, sql_val
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import KFold
import matplotlib.pyplot as plt

#%%

carpeta = 'C:/Users/Phone/Desktop/Source2/LaboDatos/TP02-pip install grupo_1/'
archivo = 'sign_mnist_train.csv'
datos = pd.read_csv(carpeta + archivo)

#%%   #MATRICES

A_matriz = (sql^"""
            SELECT DISTINCT *
            FROM datos
            WHERE label = 0
            """).to_numpy()
    
L_matriz = (sql^"""
            SELECT DISTINCT *
            FROM datos
            WHERE label = 11
            """).to_numpy()

muestras_AL_matriz = (sql^"""
                      SELECT *
                      FROM A
                      UNION 
                      SELECT *
                      FROM L
                      ORDER BY label ASC
                      """).to_numpy()

#%%       #DATA FRAMES 
 
A = sql^"""
    SELECT DISTINCT *
    FROM datos
    WHERE label = 0
    """
    
L = sql^"""
    SELECT DISTINCT *
    FROM datos
    WHERE label = 11
    """
    
muestras_AL = sql^"""
              SELECT *
              FROM A
              UNION 
              SELECT *
              FROM L
              """

#%%  #EJERCICIO B

numero_de_muestras = sql^"""
                    SELECT COUNT(*) as total,
                    SUM(CASE WHEN label == 0 THEN 1 ELSE 0 END) as muestras_A,
                    SUM(CASE WHEN label == 11 THEN 1 ELSE 0 END) as muestras_L
                    FROM muestras_AL
                    """
#%%  #EJERCICIO C

x = muestras_AL.iloc[:,1:]
y = muestras_AL.iloc[:,0]



x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, shuffle = True, random_state=35) 

#%%  #EJERCICIO D

x = muestras_AL.iloc[:,21:24]
y= muestras_AL.iloc[:,0]
k = 3

neigh = KNeighborsClassifier(n_neighbors = k)

neigh.fit(x,y)

print("R2 (train)", neigh.score(x,y))




#%% Ejercicio 3A)

AEIOU = sql^"""
        SELECT DISTINCT *
        FROM datos
        WHERE label = 4
        UNION
        SELECT DISTINCT *
        FROM datos
        WHERE label = 8
        UNION
        SELECT DISTINCT *
        FROM datos
        WHERE label = 13
        UNION
        SELECT DISTINCT *
        FROM datos
        WHERE label = 19
        """

x1 = AEIOU.iloc[:,1:]
y1 = AEIOU.iloc[:,0]

x1_train, x1_test, y1_train, y1_test = train_test_split(x1, y1, test_size = 0.2, shuffle = True, random_state=87)


#%% Ejercicio B)


arbol0 = DecisionTreeClassifier(criterion="gini", max_depth= 3)  

arbol0.fit(x1_train,y1_train)


arbol1 = DecisionTreeClassifier(criterion="entropy", max_depth= 3)  

arbol1.fit(x1_train,y1_train)

              
arbol2 = DecisionTreeClassifier(criterion="gini", max_depth= 5)  

arbol2.fit(x1_train,y1_train)


arbol3 = DecisionTreeClassifier(criterion="entropy", max_depth= 5)  

arbol3.fit(x1_train,y1_train)

    
arbol4 = DecisionTreeClassifier(criterion="gini", max_depth= 6)  

arbol4.fit(x1_train,y1_train)

        
arbol5 = DecisionTreeClassifier(criterion="entropy", max_depth= 6)  

arbol5.fit(x1_train,y1_train)

  
arbol6 = DecisionTreeClassifier(criterion="gini", max_depth= 8)  

arbol6.fit(x1_train,y1_train)

  
arbol7 = DecisionTreeClassifier(criterion="entropy", max_depth= 8)  

arbol7.fit(x1_train,y1_train)

 
#Data frame de los scores obtenidos

scores_arboles3 = []
scores_arboles5 = []
scores_arboles6 = []
scores_arboles8 = []

scores_arboles3.append(['gini',arbol0.score(x1_test,y1_test)])
scores_arboles3.append(['entropy',arbol1.score(x1_test,y1_test)])
scores_arboles5.append(['gini',arbol2.score(x1_test,y1_test)])
scores_arboles5.append(['entropy', arbol3.score(x1_test,y1_test)])
scores_arboles6.append(['gini', arbol4.score(x1_test,y1_test)])
scores_arboles6.append(['entropy', arbol5.score(x1_test,y1_test)])
scores_arboles8.append(['gini', arbol6.score(x1_test,y1_test)])
scores_arboles8.append(['entropy', arbol7.score(x1_test,y1_test)])

#%%

scores_arboles3 = pd.DataFrame(scores_arboles3).rename(columns = {0:'criterio',1:'Score'})
scores_arboles5 = pd.DataFrame(scores_arboles5).rename(columns = {0:'criterio',1:'Score'})
scores_arboles6 = pd.DataFrame(scores_arboles6).rename(columns = {0:'criterio',1:'Score'})
scores_arboles8 = pd.DataFrame(scores_arboles8).rename(columns = {0:'criterio',1:'Score'})

#Grafico de Score y alturas segun criterios

fig, ax = plt.subplots()
ax.bar(x = 'criterio', height = 'Score', data = scores_arboles3)

fig, ax = plt.subplots()
ax.bar(x = 'criterio', height = 'Score', data = scores_arboles5)

fig, ax = plt.subplots()
ax.bar(x = 'criterio', height = 'Score', data = scores_arboles6)

fig, ax = plt.subplots()
ax.bar(x = 'criterio', height = 'Score', data = scores_arboles8)


#%%




