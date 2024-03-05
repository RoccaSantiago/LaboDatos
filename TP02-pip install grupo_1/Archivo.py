#Importamos las bibliotecas
import pandas as pd
import numpy as np
from inline_sql import sql, sql_val
from sklearn.utils import shuffle
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV,train_test_split
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

#%%1

carpeta = 'C:/Users/Phone/Desktop/Source2/LaboDatos/TP02-pip install grupo_1/'

datos = pd.read_csv(carpeta + 'sign_mnist_train.csv')

#%%2   DataFrames de A y L

#Generamos los dataframes con consultas SQL
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
#Generamos un dataframe con las As y Ls
muestras_AL = pd.concat([A,L])
    
#%%3

#Definimos una funcion para imprimir cuantas imagenes se quiera de cualquier letra
def imprimirImagenes(filas,columnas,letra):
    
    #Realizamos un abecedario para poder determinar a partir del label de que letra se trata
    abecedario = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y'}
    
    #Tomamos un dataFrame de la letra deseada
    letras = sql^"""
            SELECT DISTINCT *
            FROM datos
            WHERE label = $letra
            """
    #Sacamos los labels
    letras =  letras.drop(columns = ['label']).values       
    
    #Generamos el grafico
    fig, ax =  plt.subplots(columnas,filas)
    
    #Imprimos las imagenes para cada fila y columna
    for fila in range(0,filas):
        for columna in range(0,columnas):
            ax[fila][columna].tick_params(left = False, right = False , labelleft = False , labelbottom = False, bottom = False)
            ax[fila][columna].imshow(letras[fila+columna].reshape(28,28), cmap = "gray")
    
    #Titulo
    fig.suptitle('Imagenes de la letra '+ abecedario[letra], fontsize=14)
    
    #Guardamos la imagen
    plt.savefig(carpeta + 'Graficos/Manos/' +abecedario[letra] + '_' + str(filas) + 'x'+str(columnas)+'.png',bbox_inches='tight', dpi = 200)
    

#Imprimimos 5 imagenes la L
imprimirImagenes(5,5,11)

#Imprimimos 5 imagenes la A
imprimirImagenes(5,5,0)

#%%

#Cantidad de As y Ls

Cantidades = sql^"""
            SELECT DISTINCT (CASE WHEN label = 0 THEN 'Letras A' ELSE 'Letras L' END) as Letra, count(label)/(SELECT SUM(label) FROM muestras_AL AS caux1) AS proporcion
            FROM muestras_AL
            GROUP BY label
            """
#Generamos el grafico de tarta
fig, ax = plt.subplots()
ax.pie(data = Cantidades, x = 'proporcion',labels='Letra', autopct='%1.1f%%',startangle=90,shadow=True,colors = ["#73A4CA", "#2E5B88"])

#Titulo
ax.set_title('Proporcion de As y Ls en muestras de As y Ls')

del ax,fig,Cantidades

#%% 5 Busqueda de pixeles relevantes y no relevantes

fig,ax = plt.subplots(1,2)

Superposicion_A = A.groupby('label').sum().values.reshape(28,28)
Superposicion_L = L.groupby('label').sum().values.reshape(28,28)

# A-L
ax[0].imshow(Superposicion_A - Superposicion_L , cmap = 'gray')

#L-A
ax[1].imshow(Superposicion_L - Superposicion_A, cmap = 'gray')

#Titulo
fig.suptitle('Restas entre superposiciones de todas las L y todas las A', fontsize=14)

#Guardamos la imagen
plt.savefig(carpeta + 'Graficos/Superposiciones.png',bbox_inches='tight', dpi = 200)

del ax,fig
#%% Marcado de Areas de interes para tomar pixeles relevantes

fig,ax = plt.subplots(1,2)

Superposicion_A = A.groupby('label').sum().values.reshape(28,28)
Superposicion_L = L.groupby('label').sum().values.reshape(28,28)

# A-L
ax[0].imshow(Superposicion_A - Superposicion_L , cmap = 'gray')

#L-A
ax[1].imshow(Superposicion_L - Superposicion_A, cmap = 'gray')

#Marcadores 
for i in range(0,2):
    circulo = patches.Circle((14.5, 17), 3, color='red', alpha=0.2)
    ax[i].add_patch(circulo)
    circulo = patches.Circle((19, 10), 2.6, color='red', alpha=0.2)
    ax[i].add_patch(circulo)
    circulo = patches.Circle((8, 18), 1.7, color='red', alpha=0.2)
    ax[i].add_patch(circulo)
    circulo = patches.Circle((23, 14), 1.7, color='red', alpha=0.2)
    ax[i].add_patch(circulo)


#Titulo
fig.suptitle('Areas de interes para tomar pixeles relevantes', fontsize=14)

#Guardamos la imagen
plt.savefig(carpeta + 'Graficos/AreasDeInteres.png',bbox_inches='tight', dpi = 200)

del ax,fig,A,L,Superposicion_A,Superposicion_L,i,circulo
#%%

#Guardamos las muestras
x = muestras_AL.drop(columns = ['label'])
y = muestras_AL[['label']]

#Las separamos para entrenamiento y testeo
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state=1) 

del x,y,muestras_AL

#%%  MODELO DE N PIXELES AUTOMATICO

#Definimos una funcion la cual tome pixeles de la A y la L, y devuelve el score:
def ModeloNPixelesAuto(pixeles):
    
    #Hacemos que sea una lista el set
    pixeles = list(pixeles)
    
    #Seteamos los nombres de los labels correctamente
    for i in range(len(pixeles)):
        pixeles[i] = 'pixel'+ str(pixeles[i])
    
    #Guardamos las muestras con los atributos especificos
    x_trainEspe = x_train[pixeles]
    x_testEspe = x_test[pixeles]

    #Establecemos los hiperparametros
    hyper_params = {'n_neighbors' : range(1,11)}

    #Generamos el modelo
    modelo_Al = KNeighborsClassifier()

    #Seteamos el modelo con los mejores parametros en base a la exactitud
    AL = GridSearchCV(modelo_Al, hyper_params, scoring='accuracy')

    #Entreanmos el modelo con los mejores atributos (Usamos el .ravel() para evitar warnings de conversion)
    AL.fit(x_trainEspe,y_train.values.ravel())

    #Evaluamos el score con nuestra muestra test
    return [AL.score(x_testEspe,y_test), AL.best_params_]
    
#%% Set de 3 pixeles

pixeles3 = []

#Set de pixeles importantantes tomados a partir de la seccion 5
PixRelevantes1 = ModeloNPixelesAuto(set([491,492,518]))
pixeles3.append(['PixRelevantes1',PixRelevantes1[0],PixRelevantes1[1]['n_neighbors']])

PixRelevantes2 = ModeloNPixelesAuto(set([301,274,246]))
pixeles3.append(['PixRelevantes2',PixRelevantes2[0],PixRelevantes2[1]['n_neighbors']])

#Set de pixeles no importantes tomados a partir de la seccion 5
PixNoRelevantes1 = ModeloNPixelesAuto(set([283,784,10]))
pixeles3.append(['PixNoRelevantes1',PixNoRelevantes1[0],PixNoRelevantes1[1]['n_neighbors']])

PixNoRelevantes2 = ModeloNPixelesAuto(set([1,420,28]))
pixeles3.append(['PixNoRelevantes2',PixNoRelevantes2[0],PixNoRelevantes2[1]['n_neighbors']])


#Pixeles Aleatorios
for i in range(1,3):
    
    #Set de pixeles aleatorios
    set_aleatorio = set()
    
    #Seteamos la seed de random
    random.seed(i*random.randint(1,100))
    
    #Agregamos 3 pixeles al set
    while len(set_aleatorio)<3:
        set_aleatorio.add(random.randint(1, 728))
    
    #llamamos la funcion
    pixAleatorios = ModeloNPixelesAuto(set_aleatorio)
    pixeles3.append(['pixAleatorios'+str(i),pixAleatorios[0],pixAleatorios[1]['n_neighbors']])

del PixRelevantes1,PixRelevantes2,PixNoRelevantes1,PixNoRelevantes2,set_aleatorio,pixAleatorios,i

#%% Set de 3 pixeles graficos 

#Pasamos a pixeles3 a un dataframe (todos poseen el mismo valor de kvecinos)
pixeles3 = pd.DataFrame(pixeles3).rename(columns = {0:'Nombre',1:'Exactitud',2:'Kvecinos'})

#Generamos el grafico
fig, ax = plt.subplots()
ax.bar(x = 'Nombre', height = 'Exactitud', data = pixeles3)

#Titulo
ax.set_title('Comparacion de exactitud en set de 3 pixeles con Kvecinos Automatico')

#Eje x
plt.xticks(rotation=40, ha='right',fontsize="small")

#Eje y
ax.set_ylim(0.7, 1)   

#Guardamos la imagen
plt.savefig(carpeta + 'Graficos/ComparacionDeSetsDe3PixelesAuto.png',bbox_inches='tight', dpi = 200)

del pixeles3,ax,fig

#%% Set de n pixeles aleatorios
#Repetimos el experimento 4 veces para obtener distintos sets de n pixeles aleatorios

npixeles = [[],[],[],[]]

for i in range(0,4):
    NPixeles = set()
    random.seed(i)
    for atributos in range(1,11):
        while len(NPixeles)<atributos:
            NPixeles.add(random.randint(1, 728))  
            resultados = ModeloNPixelesAuto(NPixeles)
            npixeles[i].append([atributos, resultados[0],resultados[1]])
            
del NPixeles,i,atributos,resultados

#%% Graficos de N pixeles aleatorios
      
#Generamos el grafico
fig, ax = plt.subplots()

# Ancho de las barras
ancho = 0.2  

for i in range(0, 4):
    #Generamos el dataframe con los datos de cada Set
    dataframe = pd.DataFrame(npixeles[i]).rename(columns={0: 'Atributos', 1: 'Score', 2: 'Vecinos'})
    
    #Seteamos la posicion de cada barra
    posicionesx = np.arange(len(dataframe)) + i * ancho
    
    #Ploteamos grada grafico en la figura
    ax.bar(posicionesx, height=dataframe['Score'], width=ancho, label= f'Set Aleatorio {i + 1}')

#Eje x
ax.set_xlabel('Cantidad de Pixeles')
ax.set_xticks(np.arange(len(dataframe)) + ancho * 1.5)
ax.set_xticklabels(dataframe['Atributos'])


#Eje y
ax.set_ylabel('Score')
ax.set_yticks([0,0.10,0.20,0.30,0.40,0.50,0.60,0.70,0.80,0.90,1])


#Titulo
ax.set_title('Score vs. Atributos para N Pixeles Aleatorios con mejop cantidad de vecinos')

#Leyenda
ax.legend(loc='lower right', fontsize=9.5)

#Guardamos la imagen
plt.savefig(carpeta + 'Graficos/ComparacionDeAtributosConKAutomatico.png',bbox_inches='tight', dpi = 200)

del i,fig,ax,dataframe,posicionesx,npixeles,ancho

#%% Modelo de N pixeles No automatico

#Generamos una funcion que evaulua un modelo KNN con pixeles y un k especificos
def ModeloNPixelesNA(pixeles, k):
    
    #Hacemos que sea una lista el set
    pixeles = list(pixeles)
    
    #Seteamos los nombres de los labels correctamente
    for i in range(len(pixeles)):
        pixeles[i] = 'pixel'+ str(pixeles[i])
    
    #Guardamos las muestras con los atributos especificos
    x_trainEspe = x_train[pixeles]
    x_testEspe = x_test[pixeles]

    #Generamos el modelo
    AL = KNeighborsClassifier(n_neighbors=k)

    #Entreanmos el modelo con los mejores atributos (Usamos el .ravel() para evitar warnings de conversion)
    AL.fit(x_trainEspe,y_train.values.ravel())

    #Evaluamos el score con nuestra muestra test
    return [AL.score(x_testEspe,y_test)]

#%% Sets de 3 pixeles con funcion no automatica

#Creamos la variable que guarde los datos de la funcion no automatica
pixeles3NA = [[],[],[]]


for k in range(1,11):
    #Tomamos los sets de pixeles de 3 y evaluamos para una serie de k distintos 
    PixRelevantes1 = ModeloNPixelesNA(set([301,274,246]), k)
    pixeles3NA[0].append([PixRelevantes1[0],k])


    #Set de pixeles no importantes tomados a partir de la seccion 5
    PixNoRelevantes1 = ModeloNPixelesNA(set([283,784,10]),k)
    pixeles3NA[1].append([PixNoRelevantes1[0],k])

    #Set de pixeles aleatorios
    set_aleatorio = set()
    
    #Seteamos la seed de random
    random.seed(12)
    
    #Agregamos 3 pixeles al set
    while len(set_aleatorio)<3:
        set_aleatorio.add(random.randint(1, 728))
    
    #llamamos la funcion
    pixAleatorios = ModeloNPixelesNA(set_aleatorio,k)
    pixeles3NA[2].append([pixAleatorios[0],k])

    
del PixRelevantes1,PixNoRelevantes1,set_aleatorio,pixAleatorios,k

#%% Graficos de Set de 3 pixeles no automaticos

for i in range(0,3):
    pixeles3NA[i] = pd.DataFrame(pixeles3NA[i]).rename(columns={0:'score',1:'k'})

fig, ax = plt.subplots()

ax.plot('k','score', data= pixeles3NA[0] ,
        marker='.',                             
        linestyle='-',                          
        linewidth=0.5,                          
        label='Pixeles Relevantes',                    
        )

ax.plot('k','score', data= pixeles3NA[1],
        marker='.',                             
        linestyle='-',                          
        linewidth=0.5,                          
        label='Pixeles No relevantes',                    
        )

ax.plot('k','score', data= pixeles3NA[2],
        marker='.',                             
        linestyle='-',                          
        linewidth=0.5,                          
        label='Pixeles Aleatorios',                    
        )

#Eje X
ax.set_xlabel('Cantidad de Vecinos')
ax.set_xticks(range(1,11))

#Eje y
ax.set_ylabel('Score')
ax.set_yticks([0.75,0.80,0.85,0.90,0.95,1])

#Titulo
ax.set_title('Cantidad de Vecinos vs. Score')

#Leyenda
ax.legend(loc='center right', bbox_to_anchor=(1.1, 0.65),fontsize=9)

#Grilla
plt.grid(linestyle='--', linewidth=0.5, axis = 'y')

#Guardamos la imagen
plt.savefig(carpeta + 'Graficos/ComparacionDeKyScore.png',bbox_inches='tight', dpi = 200)

del ax,fig,i
#%% Realizamos 4 modelos con sets de atributos aleatorios y distintos ks

npixeles = [[],[],[],[]]

#Repetimos el modelo con 4 sets aleatorios
for i in range(0,4):
    
    #Creamos els set y cambiamos la semilla de aleateoridad
    NPixeles = set()
    random.seed(i)
    
    #Evaluamos el set para los 10 atributos
    for atributos in range(1,11):
        
        #Agregamos al set los atributos
        while len(NPixeles)<atributos:
            NPixeles.add(random.randint(1, 728))  
        
        #Para cada n atributos evaluamos para 10 valores de k
        for k in range(1,11):
            resultados = ModeloNPixelesNA(NPixeles,k)
            npixeles[i].append([atributos, resultados[0],k])


#%% Graficamos esta ultima seccion por separado

#Pasamos los datos a dataframes
for i in range(0,4):
    npixeles[i] = pd.DataFrame(npixeles[i]).rename(columns={0:'atributos',1:'score',2:'k'})

#Generamos los graficos separados

marcadores = {0:'o',1:'^',2:'p',3:'X'}
colores = {0:'blue',1:'orange',2:'green',3:'red'}

for i in range(0,4):
    fig = plt.figure(figsize=(15, 15))
    ax = fig.add_subplot(projection='3d')
    ax.scatter(xs = 'atributos', ys ='k', data= npixeles[i], marker = marcadores[i], zs = 'score', label = 'set '+ str(i+1),s=150, color = colores[i])
    
    #Primer Grafico:
        
    #Eje x
    ax.set_xlabel('Cantidad de Atributos',fontsize =15)
    ax.set_xticks(range(1,11))
    ax.xaxis.labelpad = 20
    
    
    #Eje y
    ax.set_ylabel('Cantidad de vecinos',fontsize = 15)
    ax.set_yticks(range(1,11))
    ax.yaxis.labelpad = 20
    
    #Eje z
    ax.set_zlabel('Score',fontsize=15)
    ax.zaxis.labelpad = 20
    ax.set_zlim(0.5,1)


    #Titulo
    ax.set_title('Cantidad de vecinos vs. Cantidad de atributos vs. Score',fontsize= 30)

    #Leyenda
    ax.legend(loc = 'lower right',fontsize= 20)
    
    #Vista
    ax.view_init(elev=20, azim=45)
    
    #Guardamos en una imagen
    plt.savefig(carpeta + 'Graficos/Grafico3D/Separados/General/Grafico'+str(i+1)+'.png',bbox_inches='tight', dpi = 200)
    
    #Segundo Grafico:
    
    #Vista    
    ax.view_init(elev=0, azim=90)
    
    #Eje y
    ax.set_ylabel(' ',fontsize = 15)
    ax.set_yticks([])
    
    #Titulo
    ax.set_title('Cantidad de Atributos vs. Score',fontsize= 30)
    
    #Guardamos en una imagen
    plt.savefig(carpeta + 'Graficos/Grafico3D/Separados/ScoreVSAtributos/Grafico'+str(i+1)+'.png',bbox_inches='tight', dpi = 200)
    
    #Tercer grafico
    
    #Vista
    ax.view_init(elev=0, azim=0)
    
    #Eje x
    ax.set_xlabel('',fontsize = 15)
    ax.set_xticks([])
    
    #Eje y
    ax.set_ylabel('Cantidad de vecinos',fontsize = 15)
    ax.set_yticks(range(1,11))
    
    #Guardamos en una imagen
    plt.savefig(carpeta + 'Graficos/Grafico3D/Separados/ScoreVSVecinos/Grafico'+str(i+1)+'.png',bbox_inches='tight', dpi = 200)
    

#%% Graficamos estos anteriores juntos

fig = plt.figure(figsize=(15, 15))
ax = fig.add_subplot(projection='3d')
ax.scatter(xs = 'atributos', ys ='k', data= npixeles[0], marker = marcadores[0], zs = 'score', label = 'set '+ str(1),s=150, color = colores[0])
ax.scatter(xs = 'atributos', ys ='k', data= npixeles[1], marker = marcadores[1], zs = 'score', label = 'set '+ str(2),s=150, color = colores[1])
ax.scatter(xs = 'atributos', ys ='k', data= npixeles[2], marker = marcadores[2], zs = 'score', label = 'set '+ str(3),s=150, color = colores[2])
ax.scatter(xs = 'atributos', ys ='k', data= npixeles[3], marker = marcadores[3], zs = 'score', label = 'set '+ str(4),s=150, color = colores[3])
#Primer Grafico:
    
#Eje x
ax.set_xlabel('Cantidad de Atributos',fontsize =15)
ax.set_xticks(range(1,11))
ax.xaxis.labelpad = 20


#Eje y
ax.set_ylabel('Cantidad de vecinos',fontsize = 15)
ax.set_yticks(range(1,11))
ax.yaxis.labelpad = 20

#Eje z
ax.set_zlabel('Score',fontsize=15)
ax.zaxis.labelpad = 20
ax.set_zlim(0.5,1)


#Titulo
ax.set_title('Cantidad de vecinos vs. Cantidad de atributos vs. Score',fontsize= 30)

#Leyenda
ax.legend(loc = 'lower right',fontsize= 20)

#Vista
ax.view_init(elev=20, azim=45)


#Guardamos en una imagen
plt.show()
plt.savefig(carpeta + 'Graficos/Grafico3D/Juntos/General/Grafico.png',bbox_inches='tight', dpi = 200)

#Segundo Grafico:

#Vista    
ax.view_init(elev=0, azim=90)

#Eje y
ax.set_ylabel(' ',fontsize = 15)
ax.set_yticks([])

#Titulo
ax.set_title('Cantidad de Atributos vs. Score',fontsize= 30)

#Guardamos en una imagen
plt.show()
plt.savefig(carpeta + 'Graficos/Grafico3D/Juntos/ScoreVSAtributos/Grafico.png',bbox_inches='tight', dpi = 200)

#Tercer grafico

#Vista
ax.view_init(elev=0, azim=0)

#Eje x
ax.set_xlabel('',fontsize = 15)
ax.set_xticks([])

#Eje y
ax.set_ylabel('Cantidad de vecinos',fontsize = 15)
ax.set_yticks(range(1,11))

#Guardamos en una imagen
plt.savefig(carpeta + 'Graficos/Grafico3D/Juntos/ScoreVSVecinos/Grafico.png',bbox_inches='tight', dpi = 200)

del ax,fig,colores,atributos,marcadores,npixeles

