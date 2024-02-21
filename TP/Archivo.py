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

links = pd.DataFrame(columns = ["codigo_sede","link","red_social"])



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
                links_nuevo.append([linea[0],link, link.split(".")[1]])
            
                
        
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

#Consultas SQL

                
ConsultaSQL1 = """
            SELECT DISTINCT pais.nombre AS País, COUNT(secciones.nombre_seccion) AS sedes, AVG(secciones_por_sede) AS secciones promedio, pais.pbi AS PBI per Cápita 2022 (U$S)
            from pais
            
            INNER JOIN secciones
            ON pais.iso3 = secciones.iso3
            
            INNER JOIN (        
                SELECT DISTINCT secciones.codigo_sede AS codigo_sede, COUNT(secciones.nombre_seccion) AS secciones_por_sede
                FROM secciones
                GROUP BY secciones.codigo_sede
                ) AS subCon
            ON subCon.codigo_sede = secciones.codigo_sede
            
            GROUP BY pais.nombre
            ORDER BY pais.nombre DES
            """

ConsultaSQL2= """
            SELECT DISTINCT region AS Región geográfica, SUM(sedesxpais.sedes_por_pais) AS Países Con SedesArgentinas, promedio_pbi_region.promedio AS Promedio PBI perCápita 2022 (U$S)
            FROM pais
            GROUP BY region

            INNER JOIN(
                SELECT DISTINCT region, AVG(pbi) AS promedio
                FROM pais
                GROUP by region
                ) AS promedio_pbi_region
            ON promedio_pbi_region.region = pais.region

            INNER JOIN(
                SELECT DISTINCT iso3, COUNT(codigo_sede) AS sedes_por_pais
                FROM sedes
                GROUP BY sedes
                ) AS sedesxpais
            ON sedesxpais.iso3 = pais.iso3
            ORDER BY Promedio PBI perCápita 2022 (U$S)    
            
            """
            
ConsultaSQL3= """
            SELECT DISTINCT pais.iso3, COUNT(redes.codigo_sede)
            FROM pais
            INNER JOIN(
                SELECT DISTINCT pais.iso3 AS iso3, links.red_Social AS redes
                FROM links 
                INNER JOIN sedes
                ON sedes.codigo_sede = links.codigo_sede
                INNER JOIN pais
                ON sedes.iso3 = pais.iso3
                ) AS redes_por_pais
            ON redes_por_pais.iso3 = pais.iso3
            """

ConsultaSQL4= """
            SELECT DISTINCT pais.nombre, sedes.codigo_sede AS sede, links.red_social AS Red Social, links.link AS URL
            FROM sedes
            INNER JOIN pais
            ON pais.iso3 = sedes.iso3
            ORDER BY pais.nombre ASC, sedes.sede_codigo ACS, links.red_social ASC,links.url ASC
            """