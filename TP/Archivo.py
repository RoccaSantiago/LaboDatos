"""
Autores: 

Grupo: pip install grupo_1

"""

#Importamos las bibliotecas a usar:
    
import pandas as pd
import csv
from inline_sql import sql, sql_val

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
            
sedes = sql^consultaSQL


########################################################
#                         PAIS                         #
########################################################

consultaSQL = """
            SELECT DISTINCT cs.pais_iso_3 AS iso3, cs.pais_castellano AS nombre_pais, bm.pbi, cs.region_geografica AS region
            FROM datos_banco_mundial AS bm
            INNER JOIN datos_completos_sedes AS cs
            ON bm.Codigo = cs.pais_iso_3
            UNION 
            SELECT DISTINCT *
            FROM pais
            """
            
pais = sql^consultaSQL          

#################################################################################################################
                                                                                                                #
#SOLAMENTE TOMA LOS PAISES DONDE HAY SEDES. QUEREMOS TAMBIEN LOS QUE NO HAY SEDES?                              #
                                                                                                                #
#################################################################################################################



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
            
secciones = sql^consultaSQL


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

links_nuevo = pd.DataFrame(links_nuevo, columns = ["codigo_sede", "link","red_Social"])


consultaSQL = """
            SELECT DISTINCT *
            FROM links
            UNION 
            SELECT DISTINCT * 
            FROM links_nuevo
            """
            
links = sql^consultaSQL            


#%%

#Consultas SQL

subconsulta1 = sql^"""
            SELECT DISTINCT secciones.codigo_sede AS codigo_sede, COUNT(secciones.nombre_seccion) AS secciones_por_sede
            FROM secciones
            GROUP BY secciones.codigo_sede
            """
                
ConsultaSQL1 = """
            SELECT DISTINCT pais.nombre_pais AS País, COUNT(subcon.codigo_sede) AS sedes, AVG(subcon.secciones_por_sede) AS secciones_promedio, pais.pbi 
            FROM sedes
            INNER JOIN subconsulta1 AS subcon
            ON subCon.codigo_sede = sedes.codigo_sede
            
            INNER JOIN pais
            ON sedes.iso3 = pais.iso3
            GROUP BY pais.nombre_pais, pais.pbi
            ORDER BY pais.nombre_pais DESC
            """

df1 = sql^ConsultaSQL1

#%%

subconsulta21 = sql^"""
            SELECT DISTINCT region, AVG(pbi) AS promedio
            FROM pais
            GROUP by region
            """
            
subconsulta22 = sql^"""
            SELECT DISTINCT iso3, COUNT(codigo_sede) AS sedes_por_pais
            FROM sedes
            GROUP BY iso3
            """
            
ConsultaSQL2= """
            SELECT DISTINCT promedio_pbi_region.region AS Región_geográfica, COUNT(sedesxpais.sedes_por_pais) AS Países_Con_SedesArgentinas, promedio_pbi_region.promedio AS Promedio_PBI_perCápita_2022_U$S
            FROM pais
            
            INNER JOIN subconsulta21 AS promedio_pbi_region
            ON promedio_pbi_region.region = pais.region

            INNER JOIN subconsulta22 AS sedesxpais
            ON sedesxpais.iso3 = pais.iso3
            
            GROUP BY promedio_pbi_region.region,Promedio_PBI_perCápita_2022_U$S
            ORDER BY Promedio_PBI_perCápita_2022_U$S
            """

df2 = sql^ConsultaSQL2

#%%

subconsulta31 = sql^"""
            SELECT DISTINCT pais.iso3 AS iso3, links.red_Social AS redes
            FROM links 
            INNER JOIN sedes
            ON sedes.codigo_sede = links.codigo_sede
            INNER JOIN pais
            ON sedes.iso3 = pais.iso3
            """
            
ConsultaSQL3= """
            SELECT DISTINCT pais.iso3, COUNT(redes.redes)
            FROM pais
            INNER JOIN subconsulta31 AS redes
            ON redes.iso3 = pais.iso3
            GROUP BY pais.iso3
            """
df3 = sql^ConsultaSQL3
            
#%%

ConsultaSQL4= """
            SELECT DISTINCT pais.nombre_pais AS Paises, sedes.codigo_sede AS sede, links.red_social AS Red_Social, links.link AS URL
            FROM sedes
            INNER JOIN links
            ON sedes.codigo_sede = links.codigo_sede
            
            INNER JOIN pais
            ON sedes.iso3 = pais.iso3
            
            ORDER BY pais ASC, sede ASC, Red_Social ASC,URL ASC
            """
df4 = sql^ConsultaSQL4