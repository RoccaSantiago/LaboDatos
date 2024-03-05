#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Materia: Laboratorio de datos - FCEyN - UBA
Clase  : Clase Visualizacion. Script clase.
Autor  : Pablo Turjanski
Fecha  : 2024-01-04
Descripcion: Mis primeros graficos
"""

# Importamos bibliotecas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt # Para graficar series multiples
from   matplotlib import ticker   # Para agregar separador de miles
import seaborn as sns           # Para graficar histograma


# from matplotlib import rcParams # Para modificar el tipo de letra
#%%
def main():
#%%
    # Carpeta donde se encuentran los archivos a utilizar
    carpeta = "C:/Users/Phone/Desktop/Source2/LaboDatos/TP02-pip install grupo_1/"
    

    # # # # # # # # # # # # # # # # # # # # # # # # 
    # #   Zoo
    # # # # # # # # # # # # # # # # # # # # # # # # 



    # Cargamos dataset del zoo
    zoo= pd.read_csv(carpeta+"zoo.csv")    

    # Genera el grafico de asistencia al zoo en funcion al mes (grafico por defecto)
    plt.bar(data=zoo, x='Mes', height='Asistencia')

    
    # Genera el grafico de asistencia al zoo en funcion al mes (mejorando la informacion mostrada)
    fig, ax = plt.subplots()    # plt.subplots() es una función que devuelve una tupla que contiene 
                                # i)  el objeto correspondiente a una figura
                                # ii) el objeto correspondiente a sus ejes
                                # 
                                # Contar con fig es útil si quiere cambiar los atributos a nivel de figura o guardar 
                                # la figura como un archivo de imagen más adelante, por ejemplo con 
                                # fig.savefig('yourfilename.png')
    
    
    plt.rcParams['font.family'] = 'sans-serif'                 # Modifica el tipo de letra utilizado
    ax.bar(data=zoo, 
           x='Mes', 
           height='Asistencia'
          )
    ax.set_title('Asistencia mensual al zoo ')                    # Agrega el titulo en el margen superior
    ax.set_xlabel('Mes', fontsize='medium')                       # Agrega una etiqueta sobre el eje x
    ax.set_ylabel('Cantidad de asistentes', fontsize='medium')    # Agrega una etiqueta sobre el eje y
    ax.set_ylim(0, 25000)                                         # Asigna rango al eje y

    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}")); # Agrega separador de miles

          #%%       
    
    # # # # # # # # # # # # # # # # # # # # # # # # 
    # #   Snow
    # # # # # # # # # # # # # # # # # # # # # # # # 

    # Cargamos dataset snow
    snow= pd.read_csv(carpeta+"snow.csv")    

    # Genera el grafico que relaciona el promedio de nevadas en funcion del promedio 
    # de las temperaturas mínimas (grafico por defecto)
    plt.scatter(data = snow, x='PromedioTempMinima', y='PromedioNevadas')


    # Genera el grafico que relaciona el promdio de nevadas en funcion del promedio 
    # de las temperaturas mínimas (mejorando la informacion mostrada)
    fig, ax = plt.subplots()
    
    plt.rcParams['font.family'] = 'sans-serif'           
    ax.scatter(data = snow, 
                x='PromedioTempMinima', 
                y='PromedioNevadas',
                s=8                         # Tamano de los puntos
               )

    ax.set_title('Promedio de Nevadas vs. Promedio de Temperaturas Mínimas \n para 51 Ciudades de USA')
    ax.set_xlabel('Promedio de Temperaturas Mínimas (ºC)', fontsize='medium')                       
    ax.set_ylabel('Promedio de Nevadas (pulgadas)', fontsize='medium')    
    ax.set_xlim( 0,  26)
    ax.set_ylim(-2, 120)

#%%

    # # # # # # # # # # # # # # # # # # # # # # # # 
    # #   Airport
    # # # # # # # # # # # # # # # # # # # # # # # # 

    # Cargamos dataset airport
    airport= pd.read_csv(carpeta+"airport.csv")    

    # Genera el grafico que relaciona tres variables en simultaneo (grafico por defecto)
    plt.scatter(data=airport, x='WaitTime', y='ParkingCost', s='AnnualEnplanements')
    

    # Genera el grafico que relaciona tres variables en simultaneo (mejorando la informacion mostrada)
    fig, ax = plt.subplots()
    
    plt.rcParams['font.family'] = 'sans-serif'           

    tamanoBurbuja = 30  # Cuanto queremos amplificar a la burbuja
    
    ax.scatter(data=airport, x='WaitTime', y='ParkingCost', s=airport['AnnualEnplanements']*tamanoBurbuja)

    ax.set_title('Relación entre tres variables')
    ax.set_xlabel('Tiempo de espera TSA (min)', fontsize='medium')                       
    ax.set_ylabel('Tarifa de estacionamiento más económica (por día)', fontsize='medium')    
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 25)
    

    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.2f}"));   # Agrega separador de decimales
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("$ {x:,.2f}")); # Agrega separador de decimales y signo $
    
    # remueve la variable remporal tamanoBuebuja que ya no utilizaremos
    del(tamanoBurbuja)

#%%
    # # # # # # # # # # # # # # # # # # # # # # # # 
    # #   Cheetah
    # # # # # # # # # # # # # # # # # # # # # # # # 

    # Cargamos dataset Cheetah
    cheetah= pd.read_csv(carpeta+"cheetah.csv")    

    # Genera el grafico de la serie temporal (grafico por defecto)
    plt.scatter(data=cheetah, x='Anio', y='Ventas')

    # Genera el grafico de la serie temporal (mejorando la informacion mostrada)
    fig, ax = plt.subplots()
    
    plt.rcParams['font.family'] = 'sans-serif'           

    ax.plot('Anio', 'Ventas', data=cheetah, marker="o")

    ax.set_title('Ventas de la compañía Cheetah Sports')
    ax.set_xlabel('Año', fontsize='medium')                       
    ax.set_ylabel('Ventas (millones de $)', fontsize='medium')    
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 250)
    

#%%
    # # # # # # # # # # # # # # # # # # # # # # # # 
    # #   CheetahRegion
    # # # # # # # # # # # # # # # # # # # # # # # # 

    # Cargamos dataset CheetahRegion
    cheetahRegion= pd.read_csv(carpeta+"cheetahRegion.csv")    

    # Genera el grafico de ambas series temporales (grafico por defecto)
    fig, ax = plt.subplots()
    ax.plot('Anio', 'regionEste' , data=cheetahRegion)
    ax.plot('Anio', 'regionOeste', data=cheetahRegion)

    # Genera el grafico de ambas series temporales (mejorando la informacion mostrada)
    fig, ax = plt.subplots()
    
    plt.rcParams['font.family'] = 'sans-serif'           
    
    # Grafica la serie regionEste 
    ax.plot('Anio', 'regionEste', data=cheetahRegion, 
            marker='.',                             # Tipo de punto (redondo, triángulo, cuadrado, etc.)
            linestyle='-',                          # Tipo de linea (solida, punteada, etc.)
            linewidth=0.5,                          # Ancho de linea 
            label='Región Este',                    # Etiqueta que va a mostrar en la leyenda
            )

    # Grafica la serie regionOeste
    ax.plot('Anio', 'regionOeste', data=cheetahRegion, 
            marker='.',                             # Tipo de punto (redondo, triángulo, cuadrado, etc.)
            linestyle='-',                          # Tipo de linea (solida, punteada, etc.)
            linewidth=0.5,                          # Ancho de linea 
            label='Región Oeste'                    # Etiqueta que va a mostrar en la leyenda
            )
    
    # Agrega titulo, etiquetas a los ejes y limita el rango de valores de los ejes
    ax.set_title('Ventas de la compañía Cheetah Sports según región')
    ax.set_xlabel('Año')
    ax.set_ylabel('Ventas (millones de $)')
    ax.set_xlim(0,12)
    ax.set_ylim(0,140)
    
    # Muestra la leyenda
    ax.legend()

#%%    

    # # # # # # # # # # # # # # # # # # # # # # # # 
    # #   Cheetah
    # # # # # # # # # # # # # # # # # # # # # # # # 

    # Cargamos dataset Cheetah
    cheetah= pd.read_csv(carpeta+"cheetah.csv")    

    # Genera el grafico de barras de las ventas mensuales (grafico por defecto)
    fig, ax = plt.subplots()

    ax.bar(data=cheetah, x='Anio', height='Ventas')


    # Genera el grafico de barras de las ventas mensuales (mejorando la informacion mostrada)
    fig, ax = plt.subplots()
    
    plt.rcParams['font.family'] = 'sans-serif'           
    plt.rcParams['axes.spines.left']  = False       # Remueve linea derecha  del recuadro
    
    ax.bar(data=cheetah, x='Anio', height='Ventas')
           
    ax.set_title('Ventas de la compañía Cheetah Sports')
    ax.set_xlabel('Año', fontsize='medium')                       
    ax.set_ylabel('Ventas (millones de $)', fontsize='medium')    
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 250)

    ax.set_xticks(range(1,11,1))                            # Muestra todos los ticks del eje x
    ax.set_yticks([])                                       # Remueve los ticks del eje y
    ax.bar_label(ax.containers[0], fontsize=8)              # Agrega la etiqueta a cada barra



#%%

    # # # # # # # # # # # # # # # # # # # # # # # # 
    # #   CheetahRegion
    # # # # # # # # # # # # # # # # # # # # # # # # 

    # Cargamos dataset CheetahRegion
    cheetahRegion= pd.read_csv(carpeta+"cheetahRegion.csv")    


    # Genera el grafico de barras de ambas series temporales (grafico por defecto)
    fig, ax = plt.subplots()

    ax = cheetahRegion.plot(x='Anio', y=['regionEste', 'regionOeste'], kind='bar')
    

    # Genera el grafico de barras de ambas series temporales (mejorando la informacion mostrada)
    fig, ax = plt.subplots()
    
    plt.rcParams['font.family'] = 'sans-serif'           
    plt.rcParams['axes.spines.left']  = True       # Incorpora linea derecha del recuadro

    ax = cheetahRegion.plot(x='Anio', 
                            y=['regionEste', 'regionOeste'], 
                            kind='bar',
                            label=['Region Este', 'Region Oeste'])   # Agrega etiquetas a la serie
    
    ax.set_title('Ventas de la compañía Cheetah Sports según región')
    ax.set_xlabel('Año')
    ax.set_ylabel('Ventas (millones de $)')
    ax.set_xlim(-1,10)
    ax.set_ylim(0,140)
    


#%%
    # # # # # # # # # # # # # # # # # # # # # # # # 
    # #   CheetahRegion
    # # # # # # # # # # # # # # # # # # # # # # # # 

    # Cargamos dataset CheetahRegion
    cheetahRegion= pd.read_csv(carpeta+"cheetahRegion.csv")    

    # Genera el grafico de barras apiladas de ambas series temporales (mejorando la informacion mostrada)
    fig, ax = plt.subplots()

    # Grafica la serie regionEste 
    ax.bar(cheetahRegion['Anio'], cheetahRegion['regionEste'] , label='Region Este' )
    # Grafica la serie regionOeste
    ax.bar(cheetahRegion['Anio'], cheetahRegion['regionOeste'], bottom=cheetahRegion['regionEste'], label='Region Oeste')

    # Agrega titulo, etiquetas a los ejes y limita el rango de valores de los ejes
    ax.set_title('Ventas de la compañía Cheetah Sports según región')
    ax.set_xlabel('Año')
    ax.set_ylabel('Ventas (millones de $)')
    ax.set_xlim(0,10.9)
    ax.set_ylim(0,250)
    ax.set_xticks(range(1,11,1))    # Muestra todos los ticks del eje x

    plt.legend()                    # Muestra la leyenda
    
#%%

    # # # # # # # # # # # # # # # # # # # # # # # # 
    # #   votacionGeneral
    # # # # # # # # # # # # # # # # # # # # # # # # 

    # Cargamos dataset CheetahRegion
    votacionGeneral= pd.read_csv(carpeta+"votacionGeneral.csv")    

    # Genera el grafico de torta (grafico por defecto)
    fig, ax = plt.subplots()

    ax.pie(data=votacionGeneral, x='Porcentaje')


    # Genera el grafico de barras torta (mejorando la informacion mostrada)
    fig, ax = plt.subplots()
    
    plt.rcParams['font.family'] = 'sans-serif'           
    plt.rcParams['axes.spines.left']  = False       # Remueve linea derecha  del recuadro
    plt.rcParams['font.size'] = 9.0
    ax.pie(data=votacionGeneral, 
           x='Porcentaje', 
           labels='Alias',          # Etiquetas
           autopct='%1.2f%%',       # porcentajes
           colors=['dodgerblue',
                   'purple',
                   'gold',
                   'slateblue',
                   'orangered'],
           shadow = True,
           counterclock = True, 
           explode = (0.1,0,0,0,0)
           )
    
