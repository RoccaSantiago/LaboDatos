"""
Autores: 

Grupo: pip install grupo_1

"""

#Importamos las bibliotecas a usar:
    
import pandas as pd



#%%

#Abrimos y guardamos los datasets:

carpeta ="C:/Users/Phone/Desktop/Source2/LaboDatos/TP/Datasets/original/"

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

redes = pd.DataFrame(columns = ["link", "Nombre_red", "usuario_nombre"])

#%%

