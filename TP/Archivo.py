"""
Autores: 

Grupo: pip install grupo_1

"""

#Importamos las bibliotecas a usar:
    
import pandas as pd
import csv
#from inline_sql import sql, sql_val

# https://miro.com/welcomeonboard/b0FPNDI0SXNJUXNrQ3dTbnhzYWtMeGttV0h4TmQzQTBreEtYZDdyWEtYQWRUZXJDbUNQOU9Yc0tkUG1CeGtOZHwzMDc0NDU3MzYxNDg1ODk2Nzk3fDI=?share_link_id=441943217891

#%%

#Abrimos y guardamos los datasets:

carpeta ="C:/Users/Phone/Desktop/Source2/LaboDatos/TP/Datasets/new/"

datos_banco_mundial = pd.read_csv(carpeta + "Datos_Banco_Mundial.csv")

datos_basicos_sedes = pd.read_csv(carpeta + "Datos_Basicos_Sedes.csv")

datos_completos_sedes = pd.read_csv(carpeta + "Datos_Completos_Sedes.csv")

datos_Secciones_Sedes = pd.read_csv(carpeta + "Datos_Secciones_Sedes.csv")

#%%

#Creamos el dataframe vacio representando nuestro modelo relacional:
    
pais = pd.DataFrame(columns = ["iso3", "nombre_pais", "pbi", "region"])

sedes = pd.DataFrame(columns = ["codigo_sede", "nombre_sede", "iso3"])

secciones = pd.DataFrame(columns = ["codigo_sede","nombre_seccion"])

links = pd.DataFrame(columns = ["codigo_sede","link"])



#%%

#Importamos los datos a traves de consultas de SQL:

#PREGUNTARPREGUNTAR#PREGUNTARPREGUNTAR#PREGUNTARPREGUNTAR#PREGUNTARPREGUNTAR#PREGUNTARPREGUNTAR#PREGUNTARPREGUNTAR#PREGUNTARPREGUNTAR#PREGUNTARPREGUNTAR#PREGUNTARPREGUNTAR    

#COMENTAMOS QUE HACE CADA CONSULTA SQL?

#PREGUNTARPREGUNTAR#PREGUNTARPREGUNTAR#PREGUNTARPREGUNTAR#PREGUNTARPREGUNTAR#PREGUNTARPREGUNTAR#PREGUNTARPREGUNTAR#PREGUNTARPREGUNTAR#PREGUNTARPREGUNTAR#PREGUNTARPREGUNTAR



    
########################################################
#                        SEDES                         #
########################################################

consultaSQL = """
            SELECT DISTINCT sede_id AS codigo_sede, sede_desc_castellano AS nombre_sede, pais_iso_3 AS iso3
            FROM datos_completos_sedes
            UNION 
            SELECT DISTINCT *
            FROM sedes
            """
            
#sedes = sql^consultaSQL


########################################################
#                         PAIS                         #
########################################################

consultaSQL = """
            SELECT DISTINCT cs.iso3, cs.pais_castellano AS nombre_pais, bm.pbi, cs.region_geografica AS region
            FROM datos_banco_mundial AS bm
            INNER JOIN datos_completos_sedes AS cs
            ON bm.iso3 = cs.iso3
            UNION 
            SELECT DISTINCT *
            FROM pais
            """
            
#pais = sql^consultaSQL          

      
########################################################
#                      SECCIONES                       #
########################################################

consultaSQL = """
            SELECT DISTINCT sede_id AS codigo_sede, sede_desc_castellano AS nombre_seccion
            FROM datos_Secciones_Sedes
            UNION 
            SELECT DISTINCT *
            FROM secciones
            """
            
#secciones = sql^consultaSQL


########################################################
#                        LINKS                         # 
########################################################         

archivo = open(carpeta + "Datos_Completos_Sedes.csv", encoding = "utf8")

filas = csv.reader(archivo)

#Sacamos el encabezado para poder iterar los datos
next(filas) 


links_nuevo = []

for linea in filas:
    if linea[5] != None:
        links_linea = linea[5].split(" // ")
        for link in links_linea:
            if link != " " and link != "":
                links_nuevo.append([linea[0],link])
        
archivo.close()

links_nuevo = pd.DataFrame(links_nuevo, columns = ["codigo_sede", "link"])

consultaSQL = """
            SELECT DISTINCT *
            FROM links
            UNION 
            SELECT DISTINCT *
            FROM links_nuevo
            """
            
#links = sql^consultaSQL            


#%%

    