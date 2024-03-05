#!/usr/bin/env python
# coding: utf-8

# # Evaluación de Modelos
# 
# **Objetivo:** dada los datos de una canción (una fila en nuestro dataset) poder predecir si esta en Folklore o Evermore o es de otro álbum.
# 
# **Datos:** dataset con distintas variables de las canciones de Taylor Swift.

# In[1]:


import pandas as pd 
import utils


# #### Cargamos el dataset -- la función load_dataset limpia un poco los datos

# In[2]:


df_taylor = utils.load_dataset_taylor("taylor_album_songs.csv")
df_taylor.head()


# ### Separemos los labels y eliminamos el nombre de la canción

# In[ ]:


X = df_taylor.drop(columns = ['track_name', 'is_folklore_or_evermore'])
y = df_taylor['is_folklore_or_evermore']


# In[4]:
from sklearn.model_selection import train_test_split

# Complete aqui con su clasificador de preferencia!


X_train, X_test, y_train, y_test =  train_test_split(X, y, test_size=0.1 , shuffle=True, stratify=  y)


from sklearn.tree import DecisionTreeClassifier

arbol = DecisionTreeClassifier()

from sklearn.model_selection import cross_val_score

cross_val_score(arbol, X_train, y_train, cv = 5)


from sklearn.model_selection import KFold
kf = KFold(n_splits=2, shuffle=True)
list(kf.split(X, y))




from sklearn.model_selection import RandomizedSearchCV

hyper_params = {'criterion' : ["gini", "entropy"],
                   'max_depth' : [2,3,4,5] }

arbol = DecisionTreeClassifier()

clf = RandomizedSearchCV(arbol, hyper_params, random_state= 0, n_iter= 3)

clf.fit(X, y)

clf.best_params_

clf.best_score_

clf.score(X_test, y_test)


