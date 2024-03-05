"""
Autores: Rocca Santiago, Agustin Moguilevsky y Martin Pina

Grupo: pip install grupo_1

Descripcion: En este archivo se encuentran todas las herramientas y algoritmos necesarios para llevar el trabajo practico a cabo. Creación de los data frames, importación de datos a los mismos, consultas SQL, entre otras funcionalidades.

"""

#Importamos las bibliotecas que usaremos:
    
import pandas as pd
import numpy as np
from matplotlib import ticker   
from matplotlib import rcParams 
import matplotlib.pyplot as plt 
import seaborn as sns
from inline_sql import sql, sql_val
import csv

#%%

#Abrimos y guardamos los datasets:

#Puede generarse error al abrir el directorio por '~', en tal caso cambiar '~' por el directorio correspondiente.

carpeta = "~/TP01-pip install grupo_1/"

datos_banco_mundial = pd.read_csv(carpeta + "Tablas Originales/pais_pbi.csv")

datos_basicos_sedes = pd.read_csv(carpeta + "Tablas Originales/lista-sedes.csv")

datos_completos_sedes = pd.read_csv(carpeta + "Tablas Originales/lista-sedes-completo.csv")

datos_Secciones_Sedes = pd.read_csv(carpeta + "Tablas Originales/lista-secciones.csv")

#%%

#Creamos el dataframe vacio representando nuestro modelo relacional:

pais = pd.DataFrame(columns = ["iso3", "pais", "pbi"])

sedes = pd.DataFrame(columns = ["codigo", "sede", "iso3"])

secciones = pd.DataFrame(columns = ["codigo","seccion"])

links = pd.DataFrame(columns = ["codigo","link","red"])

regiones = pd.DataFrame(columns = ["iso3","region"])

#%%

#Para cada una de las siguientes consultas, tomamos los atributos que nos interesan para cada dataframe y los unimos con los dataframes vacios

########################################################
#                        SEDES                         #
########################################################

consultaSQL = """
            SELECT DISTINCT sede_id AS codigo, sede_desc_castellano AS sede, pais_iso_3 AS iso3
            FROM datos_completos_sedes
            UNION 
            SELECT DISTINCT *
            FROM sedes
            """
            
sedes = sql^consultaSQL


########################################################
#                         PAIS                         #
########################################################

consultaSQL = """
            SELECT DISTINCT bm.codigo AS iso3, bm.Pais AS pais, bm.pbi
            FROM datos_banco_mundial AS bm
            UNION 
            SELECT DISTINCT *
            FROM pais
            """
    
pais = sql^consultaSQL          


########################################################
#                      SECCIONES                       #
########################################################

consultaSQL = """
            SELECT DISTINCT sede_id AS codigo, sede_desc_castellano AS seccion
            FROM datos_Secciones_Sedes
            UNION 
            SELECT DISTINCT *
            FROM secciones
            """
            
secciones = sql^consultaSQL


########################################################
#                        LINKS                         # 
########################################################         

#Descomponemos los links, para obtener el dato red social
archivo = open(carpeta + "Tablas Originales/lista-sedes-completo.csv", encoding = "utf8")

filas = csv.reader(archivo)

#Sacamos el encabezado para poder iterar los datos
next(filas) 


links_totales = []

for linea in filas:
    if linea[5] != None:
        links_linea = linea[5].split(" // ")
        for link in links_linea:
            if link != " " and link != "":
                #Agregamos a link_nuevo la lista [sede_actual,nlink,nred]
                links_totales.append([linea[0],link, link.split(".")[1]]) 
            
archivo.close()

#Generamos un dataframe nuevo con los codigos de las sedes, links y los nombres de la red de cada link
links_totales = pd.DataFrame(links_totales, columns = ["codigo", "link","red"])


consultaSQL = """
            SELECT DISTINCT *
            FROM links
            UNION 
            SELECT DISTINCT * 
            FROM links_totales
            """
            
links = sql^consultaSQL            


########################################################
#                     REGIONES                         # 
########################################################  

consultaSQL = """
            SELECT DISTINCT dcs.pais_iso_3 AS iso3, region_geografica AS region
            FROM datos_completos_sedes AS dcs
            UNION
            SELECT DISTINCT *
            FROM regiones
            """
            
regiones = sql^consultaSQL            

#%%
#Exportamos las tablas limpias:
    
pais.to_csv(carpeta + 'Tablas Limpias/pais.csv', index=False)

sedes.to_csv(carpeta + 'Tablas Limpias/sedes.csv', index=False)

secciones.to_csv(carpeta + 'Tablas Limpias/secciones.csv', index=False)

links.to_csv(carpeta + 'Tablas Limpias/links.csv', index=False)

regiones.to_csv(carpeta + 'Tablas Limpias/regiones.csv', index=False)

#%%

########################################################
#                     Consulta1                        # 
########################################################

#Obetenemos un df tal que poseea todos los iso3 los cuales no tengan una sede Argentinan
subconsulta11 = sql^"""
            SELECT DISTINCT pais.iso3 AS iso3
            FROM pais
            EXCEPT 
            SELECT DISTINCT sedes.iso3
            FROM sedes
            """
            
#A partir del df subconsulta11, generamos uno nuevo donde tenga el formato final de la consulta pero tieniendo en sedes y secciones_promedio 0
subconsulta12 = sql^"""
            SELECT DISTINCT pais.pais, 0 as sedes, 0 AS secciones_promedio, pais.pbi
            FROM subconsulta11 AS sub12
            INNER JOIN pais
            ON pais.iso3 = sub12.iso3
            """

#Producimos un df el cual poseea la cantidad de secciones que tiene cada sede            
subconsulta13 = sql^"""
            SELECT DISTINCT secciones.codigo AS codigo, COUNT(secciones.seccion) AS secciones_por_sede
            FROM secciones
            GROUP BY secciones.codigo
            """

#Creamos un df para obtener cuantas sedes tiene cada pais
subconsulta14 = sql^"""
            SELECT DISTINCT iso3, COUNT(codigo) AS sedes
            FROM sedes
            GROUP BY iso3
            """
#Usando la subconsulta13 calculamos el pormedio de secciones que tiene cada sede por pais.          
subconsulta15 = sql^"""
            SELECT DISTINCT iso3, AVG(sub13.secciones_por_sede) AS secciones_promedio
            FROM subconsulta13 AS sub13
            
            INNER JOIN sedes
            ON sub13.codigo = sedes.codigo
            GROUP BY iso3
            """
#Finalmente generamos un df el cual use los datos de las subconsultas 14 y 15 para que se encuentre en el formato final y lo unimos con el df de la subconsulta 12. Luego lo ordenamos por cantidad de sedes descendentemento y alfebeticamente por pais.
ConsultaSQL1 = """
            SELECT DISTINCT pais.pais AS Pais, sub14.sedes, sub15.secciones_promedio AS Secciones_Promedio, pais.pbi AS 'PBI_per_Capita_2022_U$S'
            FROM subconsulta15 AS sub15
            
            INNER JOIN pais
            ON pais.iso3 = sub15.iso3
            
            INNER JOIN subconsulta14 AS sub14
            ON sub14.iso3 = sub15.iso3
            
            UNION 
            
            SELECT DISTINCT *
            FROM subconsulta12
            
            ORDER BY sedes DESC, pais ASC 
            """
            
#Guardamos el dataframe generado por Consulta1 y lo exportamos en un archivo .csv
Consulta1 = sql^ConsultaSQL1

Consulta1.to_csv(carpeta + 'Consultas/consulta_1.csv', index=False)

#%%

########################################################
#                     Consulta2                        # 
########################################################

#Obtenemos en un dataframe el pormedio de pbi de cada region
subconsulta21 = sql^"""
            SELECT DISTINCT region, AVG(pbi) AS promedio
            FROM regiones
            INNER JOIN pais
            ON pais.iso3 = regiones.iso3
            GROUP by region
            """
#Generamos la consulta a traves de la subconsulta21, a partir de contar cuantos paises tiene cada region y producir el formato final de la consultavb , ordenando por el promedio de pbi de manera descendente
ConsultaSQL2= """
            SELECT DISTINCT regiones.region AS  Region_geografica, COUNT(regiones.iso3) AS Paises_con_Sedes_Argentinas, promedios.promedio AS promedio_pbi
            FROM regiones
            
            INNER JOIN subconsulta21 AS promedios
            ON regiones.region = promedios.region
            
            GROUP BY regiones.region,promedios.promedio
            ORDER BY promedio_pbi DESC
            """

#Guardamos el dataframe generado por Consulta2 y lo exportamos en un archivo .csv
Consulta2 = sql^ConsultaSQL2

Consulta2.to_csv(carpeta + 'Consultas/consulta_2.csv', index=False)

#%%

########################################################
#                     Consulta3                        # 
########################################################

#En un dataframe colocamos los iso3s de los paises con las redes sociales que tengan cada sede que se encuentra en tal pais
subconsulta31 = sql^"""
            SELECT DISTINCT pais.iso3 AS iso3, links.red AS redes
            FROM links 
            INNER JOIN sedes
            ON sedes.codigo = links.codigo
            INNER JOIN pais
            ON sedes.iso3 = pais.iso3
            """

#Contamos cada red sociales, lo agrupamos por pais
ConsultaSQL3= """
            SELECT DISTINCT pais.pais, COUNT(redes.redes) AS cantidad_redes
            FROM pais
            LEFT OUTER JOIN subconsulta31 AS redes
            ON redes.iso3 = pais.iso3
            GROUP BY pais.pais
            ORDER BY cantidad_redes DESC, pais.pais
            """
            
#Guardamos el dataframe generado por Consulta3 y lo exportamos en un archivo .csv
Consulta3 = sql^ConsultaSQL3


Consulta3.to_csv(carpeta + 'Consultas/consulta_3.csv', index=False)
            
#%%

########################################################
#                     Consulta4                        # 
########################################################

#Extraemos los datos de nuestros dataframes para generar la consulta para luego ordernarlo por pais, sede,red y url ascendentemente
ConsultaSQL4= """
            SELECT DISTINCT pais.pais AS Paises, sedes.codigo AS sede, links.red AS red, links.link AS URL
            FROM sedes
            INNER JOIN links
            ON sedes.codigo = links.codigo
            
            INNER JOIN pais
            ON sedes.iso3 = pais.iso3
            
            ORDER BY pais ASC, sede ASC, red ASC,URL ASC
            """
Consulta4 = sql^ConsultaSQL4

#Guardamos el dataframe generado por Consulta4 y lo exportamos en un archivo .csv
Consulta4.to_csv(carpeta + 'Consultas/consulta_4.csv', index=False)

#%%

########################################################
#                     Grafico1                         # 
########################################################

#Producimos el dataframe con los datos de nuestro grafico
grafico1 = sql^"""
            SELECT DISTINCT region, SUM(sedes) AS Paises_con_Sedes_Argentinas  
            FROM Consulta1
            
            INNER JOIN pais
            ON pais.pais = Consulta1.Pais
            
            INNER JOIN regiones
            ON pais.iso3 = regiones.iso3
            
            GROUP BY region
            ORDER BY Paises_con_Sedes_Argentinas DESC, region DESC
            """
            

        
#Creamos el grafico
fig1, ax1 = plt.subplots()
ax1.bar(data=grafico1, x='region' , height='Paises_con_Sedes_Argentinas')

#Titulo
ax1.set_title('Sedes Argentinas por region')

#Eje x
ax1.set_xlabel('Regiones Geograficas', fontsize='medium')                       
ax1.set_ylabel('Numero de sedes Argentinas', fontsize='medium') 
ax1.set_xlim(-0.7, 8.5)   

#Eje y 
ax1.set_ylim(0, 42)

ax1.bar_label(ax1.containers[0], fontsize=8)  

plt.rcParams['axes.spines.left']  = True
   
plt.xticks(rotation=40, ha='right',fontsize="small")

#Ajustamos la figura al grafico
fig1.set_size_inches(10, 8)

#Guardamos el grafico en un .png. Para todos los graficos usaremos las caracteristicas bbox_inches='tight' y  dpi = 1000. Las cuales hacen que la imagen se ajuste al recuadro del grafico y aumente la calidad del mismo respectivamente.
plt.savefig(carpeta + 'Graficos/Grafico1.png', bbox_inches='tight', dpi = 1000)

#%%

########################################################
#                     Grafico2                         # 
########################################################

#Producimos el dataframe con los datos de nuestro grafico
grafico2aux = sql^"""
        SELECT pais, region, pbi
        FROM regiones
        
        INNER JOIN pais
        ON pais.iso3 = regiones.iso3
        """

#Ordenamos por la mediana
medianas = pd.DataFrame(grafico2aux.groupby('region')['pbi'].median().reset_index())


grafico2 =sql^"""
    SELECT DISTINCT medianas.region, grafico2aux.pbi AS pbi, medianas.pbi AS mediana
    FROM grafico2aux
    
    INNER JOIN medianas
    ON grafico2aux.region = medianas.region 
    
    ORDER BY mediana ASC
    """

#Generamos el boxplot
fig2, ax2 = plt.subplots()
ax2 = sns.boxplot(x="pbi",y="region",data = grafico2)

#Eje y
ax2.set_ylim(-0.7,8.5)
plt.ylabel('Regiones Geograficas')

#Titulo
ax2.set_title('Distribucion de PBI por region')

#Eje x
ax2.set_xlim(0, 109000)
plt.xlabel('PBI\'s Promedios (U$S)')
ax2.xaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
plt.xticks(rotation=0, ha='center',fontsize="small")

#Cuadrícula 
plt.grid(linestyle='-', linewidth=0.5,axis = 'x')

#Guardamos el grafico en un .png
plt.savefig(carpeta + 'Graficos/Grafico2.png', bbox_inches='tight', dpi = 1000)

#%%

########################################################
#                     Grafico3                         # 
########################################################

#Producimos el dataframe con los datos de nuestro grafico
grafico3 = sql^"""
        SELECT DISTINCT pais, sedes, PBI_per_Capita_2022_U$S
        FROM Consulta1
        ORDER BY sedes
        """
#Generamos el scatter
fig3, ax3 = plt.subplots()
ax3.scatter(data=grafico3,x = 'sedes', s = 4, y= 'PBI_per_Capita_2022_U$S')

#Titulo
ax3.set_title('Cantidad de sedes Argentinas por pais VS PBI per Cápita 2022 por pais')

#Eje x
ax3.set_xlim(-0.3,11.3)
ax3.set_xticks(range(0,12,1)) 
plt.xlabel('Cantidad de sedes')

#Eje y
ax3.set_yscale('log')
ax3.set_ylim(0,255000)
ax3.set_yticks([250,500,1000,2250,5000,12000,25000,50000,100000,200000]) 
ax3.yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
plt.ylabel('PBI per Capita 2022 (U$S)')


#Cuadricula
plt.grid(linestyle='--', linewidth=0.5)

#Guardamos el grafico en un .png
plt.savefig(carpeta + 'Graficos/Grafico3.png',bbox_inches='tight', dpi = 1000)

#%%

########################################################
#                     Grafico4                         # 
########################################################

#Obtenemos los datos del grafico3
grafico4 = grafico3

#Generamos el boxplot
fig4, ax4 = plt.subplots()
ax4 = sns.boxplot(data = grafico4, x = 'sedes', y = 'PBI_per_Capita_2022_U$S',showmeans=True)

#Titulo
ax4.set_title('Distribucion de PBI por cantidad de sedes')

#Eje x
ax3.set_xlim(-0.3,11.3)
ax3.set_xticks(range(0,12,1)) 
plt.xlabel('Cantidad de sedes')
           
#Eje y
ax4.set_yscale('log')
ax4.set_ylim(0,260000)
ax4.set_yticks([250,500,1000,2250,5000,12000,25000,50000,100000,200000]) 
ax4.yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
plt.ylabel('PBI per Capita 2022 (U$S)')

#Cuadricula
plt.grid(linestyle='--', linewidth=0.5, axis = 'y')

#Guardamos el grafico en un .png
plt.savefig(carpeta + 'Graficos/Grafico4.png',bbox_inches='tight', dpi = 1000)

#%%

########################################################
#                     Grafico5                         # 
########################################################

#Obtenemos los datos del grafico3
grafico5aux = sql^"""
        SELECT sedes, COUNT(Pais) AS paises
        FROM grafico3
        GROUP BY sedes
        """
        
#Calculamos las medianas
medianas5 = pd.DataFrame(grafico3.groupby('sedes')['PBI_per_Capita_2022_U$S'].median().reset_index())

#Agrupamos los datos
grafico5 = sql^"""
        SELECT g5aux.sedes, g5aux.paises, medianas5.PBI_per_Capita_2022_U$S AS mediana
        FROM grafico5aux AS g5aux
        INNER JOIN medianas5
        ON medianas5.sedes = g5aux.sedes
        """

#Generamos el scatter plot        
fig5, ax5 = plt.subplots()
ax5.scatter(data=grafico5,x = 'sedes', s = grafico5['paises']*10, y= 'mediana')

#Titulo
ax5.set_title('Relacion entre cantidad de paises, medianas de PBI y cantidad de Sedes')

#Eje x
ax5.set_xlim(-0.6,11.3)
ax5.set_xticks(range(0,12,1)) 
plt.xlabel('Cantidad de sedes')

#Eje y
ax5.set_yscale('log')
ax5.set_ylim(0,100000)
ax5.set_yticks([2250,5000,12000,25000,50000,100000]) 
ax5.yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
plt.ylabel('Mediana de PBI per Capita 2022 (U$S)')

#Cuadricula
plt.grid(linestyle='--', linewidth=0.5)

#Guardamos el grafico en un .png
plt.savefig(carpeta + 'Graficos/Grafico5.png',bbox_inches='tight', dpi = 1000)

