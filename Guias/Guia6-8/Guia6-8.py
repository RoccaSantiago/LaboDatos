
import pandas as pd
from inline_sql import sql

#%%

carpeta = "C:/Users/Phone/Desktop/Source2/LaboDatos/Guias/Guia6-8/"

casos      = pd.read_csv(carpeta+"casos.csv")    
departamento = pd.read_csv(carpeta+"departamento.csv")    
grupoetario   = pd.read_csv(carpeta+"grupoetario.csv")    
provincia    = pd.read_csv(carpeta+"provincia.csv")
tipoevento = pd.read_csv(carpeta+"tipoevento.csv")    

#%%

def imprimirEjercicio(dataframeResultadoDeConsultaSQL):

    print("# Salida:")
    print("# -------")
    print(dataframeResultadoDeConsultaSQL)

#%%

# ====================================================================
# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
#=====================================================================

#%%

#a)

consultaSQL = """
                SELECT ALL descripcion 
                FROM departamento
              """

imprimirEjercicio(sql^consultaSQL)

#%%

#b)

consultaSQL = """
               SELECT DISTINCT descripcion
               FROM departamento
              """

imprimirEjercicio(sql^consultaSQL)

#%%

#c)

consultaSQL = """
               SELECT ALL id,descripcion
               FROM departamento
              """

imprimirEjercicio(sql^consultaSQL)

#%%

#d)

consultaSQL = """
               SELECT ALL *
               FROM departamento
              """

imprimirEjercicio(sql^consultaSQL)

#%%

#e)

consultaSQL = """
               SELECT ALL id AS codigo_depto, descripcion AS nombre_depto
               FROM departamento
              """

imprimirEjercicio(sql^consultaSQL)

#%%

#f)

consultaSQL = """
               SELECT ALl *
               FROM departamento
               WHERE id_provincia = 54
              """

imprimirEjercicio(sql^consultaSQL)

#%%

#g)

consultaSQL = """
               SELECT ALl *
               FROM departamento
               WHERE id_provincia = 54 OR id_provincia = 78 OR id_provincia = 86
              """

imprimirEjercicio(sql^consultaSQL)

#%%

#h)

consultaSQL = """
               SELECT ALl *
               FROM departamento
               WHERE id_provincia >= 50 AND id_provincia <= 59
              """

imprimirEjercicio(sql^consultaSQL)

#%%

# ====================================================================
# BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
#=====================================================================

#%%

#a)

consultaSQL = """
               SELECT DISTINCT  depto.id, depto.descripcion, pro.descripcion
               FROM departamento AS depto
               INNER JOIN provincia AS pro
               ON pro.id = depto.id_provincia
              """

imprimirEjercicio(sql^consultaSQL)

#%%

#b)

consultaSQL = """
               SELECT DISTINCT  depto.id, depto.descripcion, pro.descripcion
               FROM departamento AS depto
               INNER JOIN provincia AS pro
               ON pro.id = depto.id_provincia
              """

imprimirEjercicio(sql^consultaSQL)

#%%

#b)

consultaSQL = """
               SELECT DISTINCT  depto.id, depto.descripcion, pro.descripcion
               FROM departamento AS depto
               INNER JOIN provincia AS pro
               ON pro.id = depto.id_provincia
               HAVING pro.descripcion = 'Chaco'
              """

imprimirEjercicio(sql^consultaSQL)

#%%

#c)

consultaSQL0 = """
               SELECT DISTINCT  depto.id, depto.descripcion, pro.descripcion
               FROM departamento AS depto
               INNER JOIN provincia AS pro
               ON pro.id = depto.id_provincia
               HAVING pro.descripcion = 'Buenos Aires'
              """

consultaSQL = """
               SELECT DISTINCT  depto.id, depto.descripcion, depto.descripcion
               FROM consultaSQL0 AS depto
               INNER JOIN casos 
               ON casos.id_depto = depto.id
               HAVING cantidad > 10
              """
            

imprimirEjercicio(sql^consultaSQL)

#%%

# ====================================================================
# CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
#=====================================================================

#%%

#a)

consultaSQL = """
               SELECT DISTINCT  depto.id, depto.descripcion
               FROM departamento AS depto
               OUTER JOIN casos
               ON depto.id = casos.id_depto
               HAVING casos = 0
              """

imprimirEjercicio(sql^consultaSQL)

#%%

#b)

consultaSQL = """
               SELECT DISTINCT  even.id, even.descripcion
               FROM tipoevento AS even
               OUTER JOIN casos
               ON casos.id_tipoevento = even.id
               HAVING casos = 0
              """

imprimirEjercicio(sql^consultaSQL)

#%%

# ====================================================================
# DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD
#=====================================================================

#%%

#a)

consultaSQL = """
               SELECT DISTINCT  COUNT(*) AS Ncasos
               FROM casos
              """

imprimirEjercicio(sql^consultaSQL)

#%%

#b)

consultaSQL = """
               SELECT DISTINCT  id_tipoevento, anio, COUNT(*) AS casos
               FROM casos
               GROUP BY anio, id_tipoevento
               ORDER BY id_tipoevento ASC, anio ASC 
              """

imprimirEjercicio(sql^consultaSQL)

#%%

#c)

consultaSQL = """
               SELECT DISTINCT  id_tipoevento, anio, SUM(casos) AS casos
               FROM casos
               GROUP BY id_tipoevento, anio
               HAVING anio = 2019
               ORDER BY id_tipoevento ASC
              """

imprimirEjercicio(sql^consultaSQL)

#%%

#d)

consultaSQL = """
               SELECT DISTINCT id_provincia, SUM(casos)
               FROM departamento
               GROUP BY id_provinca
               ORDER BY id_provincia ASC
              """

imprimirEjercicio(sql^consultaSQL)

#%%

#e)

# Listar los departamentos con menos cantidad de casos en el año 2019.

#Cuando deja de tener la menor cantidad? Osea ORDER BY?

consultaSQL = """
              SELECT DISTINCT id_departamento, MIN(cantidad)
               FROM casos
               ORDER BY id_departamento
               HAVING anio = 2019
              """

imprimirEjercicio(sql^consultaSQL)

#%%

#f)

# Listar los departamentos con más cantidad de casos en el año 2020
#Cuando deja de tener la mayor cantidad? Osea ORDER BY?
consultaSQL = """
              SELECT DISTINCT id_departamento, MAX(cantidad)
               FROM casos
               ORDER BY id_departamento
               HAVING anio = 2020
              """

imprimirEjercicio(sql^consultaSQL)

#%%

#g)

consultaSQL = """
               SELECT DISTINCT id_provincia, anio, AVG(cantidad) 
               FROM casos
               GROUP BY id_provincia, anio
              """

imprimirEjercicio(sql^consultaSQL)

#%%

#i)

consultaSQL = """
               SELECT DISTINCT SUM(cantidad) AS total, MAX(cantidad) AS maximo, MIN(cantidad) AS minimo, AVG(cantidad) AS promedio
               FROM casos
               GROUP BY id_provincia, anio
               HAVING id_provincia = 6 AND anio = 2019
              """

imprimirEjercicio(sql^consultaSQL)

#%%

#j)

consultaSQL = """
               SELECT DISTINCT SUM(cantidad) AS total, MAX(cantidad) AS maximo, MIN(cantidad) AS minimo, AVG(cantidad) AS promedio
               FROM casos>1000
               WHERE cantidad 
               GROUP BY id_provincia, anio
               HAVING id_provincia = 6 AND anio = 2019
              """

imprimirEjercicio(sql^consultaSQL)

#%%

#j)

consultaSQL = """
               SELECT DISTINCT SUM(cantidad) AS total, MAX(cantidad) AS maximo, MIN(cantidad) AS minimo, AVG(cantidad) AS promedio
               FROM casos
               WHERE cantidad>1000
               GROUP BY id_provincia, anio
               HAVING id_provincia = 6 AND anio = 2019
              """

imprimirEjercicio(sql^consultaSQL)

#%%

#l)

consultaSQL = """
               SELECT DISTINCT id_provincia,id_departamento, AVG(cantidad)
               FROM casos
               WHERE anio = 2019 OR anio=2020
               GROUP BY id_provincia, id_departamento
               ORDER BY id_provincia ASC, id_departamento ASC
              """

imprimirEjercicio(sql^consultaSQL)

#%%

#k)

consultaSQL = """
               SELECT DISTINCT id_tipoevento,id_departamento,id_provincia, SUM(CASE WHEN anio=2019 THEN cantidad ELSE 0 END) AS 2019, SUM(CASE WHEN anio=2020 THEN cantidad ELSE 0 END)
               FROM casos
               WHERE anio = 2019 OR anio=2020
               GROUP BY id_tipoevento,id_departamento,id_provincia
               ORDER BY id_provincia ASC, id_departamento ASC
              """

imprimirEjercicio(sql^consultaSQL)

#%%

# ====================================================================
# EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
#=====================================================================

#%%

#a)

consultaSQL = """
               SELECT DISTINCT dep.descripcion,ca.cantidad
               FROM casos AS ca1
               WHERE dep.descripcion>= ALL (
                    SELECT ca2.cantidad
                    FROM casos AS ca2
               )
              INNER JOIN departamento
              ON dep.descripcion = ca1.id_departamento
              """

imprimirEjercicio(sql^consultaSQL)

#%%

#b)

consultaSQL = """
               SELECT DISTINCT dep.descripcion,ca.cantidad
               FROM casos AS ca1
               WHERE dep.descripcion>= ALL (
                    SELECT ca2.cantidad
                    FROM casos AS ca2
               )
              INNER JOIN departamento
              ON dep.descripcion = ca1.id_departamento
              """

imprimirEjercicio(sql^consultaSQL)